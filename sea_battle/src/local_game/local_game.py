import asyncio

from src.GUI.window import Window
from src.client.client import Client
from src.constants import GREEN_COLOR, RED_COLOR, TIMEOUT


class local_game:
    def __init__(self):
        self._client = Client()
        self._window = Window()

        self._destroyed = False
        self._placed = False
        self._started = False
        self._stopped = False

    def start(self):
        self._window.start()

    async def start_async(self):
        await self._client.connect()

        await asyncio.gather(
            self._client.read_incoming_messages(),
            self._client.handle_responses(),
            self._client.refresh_fields(),
            self.refreshing_fields(),
            self._check_cancel(),
            self.start_ship_placement()
        )

    async def refreshing_fields(self):
        while not self._destroyed:
            try:
                my_field = await asyncio.wait_for(self._client.get_my_field(), timeout=TIMEOUT)
            except asyncio.TimeoutError:
                if self._destroyed:
                    break
                continue

            self._window.refresh_my_field(my_field, self._placed, not self._started)

            try:
                other_field = await asyncio.wait_for(self._client.get_other_field(), timeout=TIMEOUT)
            except asyncio.TimeoutError:
                if self._destroyed:
                    break
                continue

            self._window.refresh_other_field(other_field)

            await asyncio.sleep(0.01)

    async def _check_cancel(self):
        while not self._window.destroyed:
            await asyncio.sleep(0.0001)

        await self._client.destroy()
        self._destroyed = True

    async def start_ship_placement(self):
        self._window.write_on_label("Place your ships", GREEN_COLOR)

        while not self._client.closed and not await self._client.is_ready():
            created, ship = self._window.is_ship_created()

            if created:
                if not ship:
                    self._window.reset_added_ship()
                    continue

                response = await self._client.add_ship(ship)

                if response and response != "ok":
                    self._window.show_alert(response)
                    self._window.reset_ship()

                self._window.reset_added_ship()

            else:
                await asyncio.sleep(0.5)

        if self._destroyed:
            return

        await asyncio.sleep(0.1)
        if not self._client.closed and not await self._client.is_both_ready():
            self._window.write_on_label("Waiting for opponent", RED_COLOR)

        self._placed = True

        while not self._client.closed and not await self._client.is_both_ready():
            await asyncio.sleep(0.1)

        if not self._destroyed:
            await self.start_main_game()

    async def start_main_game(self):
        self._window.write_on_label("Let's start!", GREEN_COLOR)
        self._window.rebind_other_field_to_hit()

        await asyncio.sleep(0.5)
        self._started = True

        await asyncio.gather(
            self._handle_hit(),
            self._handle_turn(),
            self._handle_win()
        )

    async def _handle_win(self):
        while not self._destroyed:
            try:
                response = await asyncio.wait_for(self._client.is_win(), timeout=2.0)
            except asyncio.TimeoutError:
                if self._destroyed:
                    break
                continue
            if response is not None:

                await asyncio.sleep(0.5)

                self._window.show_alert("You win!!!!" if response else "You lose(((")

                self._window.destroyed = True
                self._destroyed = True

                await asyncio.sleep(1)

                self._window.destroy()
            else:
                await asyncio.sleep(0.01)

    async def _handle_hit(self):
        while not self._destroyed:
            if self._window.hitted:
                response = await self._client.hit(self._window.hitted)
                self._window.hitted = None

                if response != "ok":
                    self._window.show_alert(response)

            await asyncio.sleep(0.01)

    async def _handle_turn(self):
        while not self._destroyed:
            if await self._client.is_my_turn():
                self._window.write_on_label("Your turn!", GREEN_COLOR)
            else:
                self._window.write_on_label("Opponent turn", RED_COLOR)
            await asyncio.sleep(0.1)
