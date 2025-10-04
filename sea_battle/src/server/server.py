import asyncio
import json

from src.backend.game import Room
from src.client.json_encoder import PersonEncoder
from src.constants import ENCODING


class Server:
    def __init__(self):
        self._reader, self._writer = None, None
        self._local_game = Room()
        self._server = None

        self._local_flag = False

    async def start(self, host, port):
        self._server = await asyncio.start_server(self._handle_client, host, port)

        addr = self._server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with self._server:
            try:
                await asyncio.gather(
                    self._server.serve_forever(),
                    self.handle_console_input()
                )
            except asyncio.CancelledError:
                print("Server has been closed.")

    async def handle_console_input(self):
        loop = asyncio.get_running_loop()
        while True:
            input_cmd = await loop.run_in_executor(None, input, "Server command (type 'quit' to stop): ")
            if input_cmd.strip() == 'quit':
                self._server.close()
                await self._server.wait_closed()
                break

    async def _handle_client(self, reader, writer):
        number_player = self._local_game.player_first if self._local_flag else self._local_game.player_second
        self._local_flag = True

        while True:
            try:
                data = await reader.readuntil(separator=b'\n')
            except asyncio.IncompleteReadError:
                break
            except ConnectionResetError:
                break
            if not data:
                break

            request = json.loads(data.decode(ENCODING).strip())

            response = await self.process_request(request, number_player)

            if response is not None:
                writer.write((response + '\n').encode(ENCODING))
                await writer.drain()

        writer.close()
        await writer.wait_closed()

    async def process_request(self, request, player):
        request_type = request["request"]
        request_id = request["id"]

        response = None

        if request_type == "get_my_field":
            my_field = self._local_game.get_field(player)

            response = json.dumps({"id": request_id, "response": my_field}, cls=PersonEncoder)

        elif request_type == "get_other_field":
            field = self._local_game.get_field(
                self._local_game.player_first
                if self._local_game.player_first != player else self._local_game.player_second
            )

            response = json.dumps({"id": request_id, "response": field}, cls=PersonEncoder)

        elif request_type == "hit":
            try:
                self._local_game.hit(player, request["value"])
            except Exception as e:
                response = json.dumps({"id": request_id, "response": str(e)}, cls=PersonEncoder)
            else:
                response = json.dumps({"id": request_id, "response": "ok"}, cls=PersonEncoder)

        elif request_type == "add_ship":
            try:
                self._local_game.place_ship(player, request["value"])
            except Exception as e:
                response = json.dumps({"id": request_id, "response": str(e)}, cls=PersonEncoder)
            else:
                response = json.dumps({"id": request_id, "response": "ok"}, cls=PersonEncoder)

        elif request_type == "is_ready":
            is_ready = self._local_game.ready(player)

            response = json.dumps({"id": request_id, "response": is_ready})

        elif request_type == "is_both_ready":
            response = self._local_game.is_both_ready()

            response = json.dumps({"id": request_id, "response": response})
        elif request_type == "is_my_turn":
            response = self._local_game.who_playing_now() == player

            response = json.dumps({"id": request_id, "response": response})
        elif request_type == "is_win":
            response = self._local_game.is_win(player)

            response = json.dumps({"id": request_id, "response": response})

        return response
