import asyncio
import json
import uuid

from src.constants import HOST, PORT, ENCODING, TIMEOUT
from src.exception_catcher import catch_exception_async


class Client:
    def __init__(self):
        self._reader, self._writer = None, None

        self._incoming_queue = asyncio.Queue()
        self._pending_requests = {}

        self._my_field = asyncio.Queue()
        self._other_field = asyncio.Queue()

        self.closed = False

    async def connect(self):
        self._reader, self._writer = await asyncio.open_connection(HOST, PORT)

    async def read_incoming_messages(self):
        while not self.closed:
            try:
                data = await self._reader.readuntil(b'\n')
            except asyncio.IncompleteReadError:
                break

            if not data:
                break
            message = data.decode(ENCODING)
            await self._incoming_queue.put(message)

    async def send_request(self, request):
        self._writer.write(request.encode(ENCODING))
        try:
            await self._writer.drain()
        except ConnectionResetError:
            return

    async def process_request(self, request_type, value=None):
        request_id = str(uuid.uuid4())
        request = {"request": request_type, "id": request_id, "value": value}

        self._pending_requests[request_id] = asyncio.Future()

        await self.send_request(json.dumps(request) + '\n')

        try:
            response = await asyncio.wait_for(self._pending_requests[request_id], timeout=TIMEOUT)
            del self._pending_requests[request_id]
        except asyncio.TimeoutError:
            response = None

        return response

    @catch_exception_async(asyncio.exceptions.InvalidStateError)
    async def handle_responses(self):
        while not self.closed:
            try:
                response_data = await asyncio.wait_for(self._incoming_queue.get(), timeout=TIMEOUT)
                response_data = json.loads(response_data)
                request_id = response_data["id"]
            except asyncio.TimeoutError:
                if self.closed:
                    break
                continue

            if (request_id in self._pending_requests) and not self._pending_requests[request_id].done() and not \
                    self._pending_requests[request_id].cancelled():
                self._pending_requests[request_id].set_result(response_data["response"])

    async def _refresh_my_field(self):
        try:
            response = await self.process_request("get_my_field")
        except asyncio.CancelledError:
            return

        await self._my_field.put(response)

    async def _refresh_other_field(self):
        try:
            response = await self.process_request("get_other_field")
        except asyncio.CancelledError:
            return

        await self._other_field.put(response)

    async def destroy(self):
        self.closed = True
        self._writer.close()

        await self._writer.wait_closed()

    async def refresh_fields(self):
        while not self.closed:
            await asyncio.gather(self._refresh_my_field(),
                                 self._refresh_other_field())

            await asyncio.sleep(0.1)

    async def get_my_field(self) -> list[list[int]]:
        return await self._my_field.get()

    async def get_other_field(self) -> list[list[int]]:
        return await self._other_field.get()

    async def hit(self, coordinates) -> any:
        return await self.process_request("hit", coordinates)

    async def add_ship(self, coordinates) -> any:
        return await self.process_request("add_ship", coordinates)

    async def is_ready(self) -> bool:
        return await self.process_request("is_ready")

    async def is_both_ready(self) -> bool:
        return await self.process_request("is_both_ready")

    async def is_my_turn(self) -> bool:
        return await self.process_request("is_my_turn")

    async def is_win(self) -> bool:
        return await self.process_request("is_win")
