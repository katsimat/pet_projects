import random

from src.backend.field import Field
from src.backend.player_game import PlayerGame
from src.enums import condition


class Room:
    player_first = PlayerGame()
    player_second = PlayerGame()

    def __init__(self, size_field=10) -> None:
        self.size_field = size_field
        self.player_first.field = Field(size_field)
        self.player_first.number = 1

        self.player_second.field = Field(size_field)
        self.player_second.number = 2

        # в начале первый игрок выбирается рандомно
        number_start = random.randrange(1, 3)

        if number_start == 1:
            self.active_game = self.player_first
            self.active_field = self.player_second.field
        else:
            self.active_game = self.player_second
            self.active_field = self.player_first.field

    @staticmethod
    def get_field(player_num: PlayerGame) -> list[list]:
        """return field: list[list[condition]] \n field[y][x]"""
        big_field = player_num.field.get_field()
        size_field = player_num.field.field_size()
        field = [[condition] * size_field for _ in range(size_field)]

        for y in range(size_field):
            for x in range(size_field):
                field[y][x] = big_field[y][x][0]

        return field

    def who_isnt_playing_now(self) -> PlayerGame:
        return self.player_second if self.active_game.number == 1 else self.player_first

    def who_playing_now(self) -> PlayerGame:
        return self.active_game

    def __active_player(self, number_player: PlayerGame):
        self.active_game = number_player
        self.active_field = self.who_isnt_playing_now().field

    def hit(self, player: PlayerGame, coordinates: tuple):
        """coordinates in [0, field_size-1]\n
        Error:\n
        1) indexes of the place of the hit are invalid\n
        2) you hited there\n
        3) if you cant hit: player isnt playing now\n
        4) if all ships killed: End Game"""

        if player.number != self.who_playing_now().number:
            raise Exception("Not your turn!")

        condit = self.active_field.make_hit(tuple(elem + 1 for elem in coordinates))

        # проверка на конец игры 
        if self.active_field.end_game():
            self.active_game.win = True
            if self.active_game == self.player_second:
                self.player_first.win = False
            else:
                self.player_second.win = False

        if condit == condition.miss:
            self.__active_player(self.who_isnt_playing_now())

    @staticmethod
    def is_win(player: PlayerGame) -> bool:
        return player.win

    def place_ship(self, number_player: PlayerGame, coordinates: list[tuple]) -> None:
        """coordinates in [1, field_size]\n
        field[x][y]\n
        errors: \n
        1) if x and y index out of field or field[y][x] not free - Exception: not free cell begin \n
        2) if the ship does not fit into the field - Exception: long ship"""

        if number_player.number == 1:
            self.player_first.field.put_ship(
                [(elem[1], elem[0]) for elem in coordinates])
        else:
            self.player_second.field.put_ship(
                [(elem[1], elem[0]) for elem in coordinates])

    def remove_ship(self, number_player: PlayerGame, coordinates: list[tuple]) -> None:
        """coordinates[[y][x]] \n
        coordinates in [1, field_size]"""

        if number_player.number == 1:
            self.player_first.field.remove_ship(coordinates)
        else:
            self.player_second.field.remove_ship(coordinates)

    def start(self, number_start=random.randrange(1, 2)):
        """start game"""

        if number_start == 1:
            self.active_game = self.player_first
            self.active_field = self.player_second.field
        else:
            self.active_game = self.player_second
            self.active_field = self.player_first.field

    @staticmethod
    def ship_count(number_player: PlayerGame) -> int:
        return number_player.field.ship_count()

    @staticmethod
    def ready(number_player: PlayerGame) -> bool:
        return number_player.field.all_ships_put()

    def is_both_ready(self):
        return Room.ready(self.player_first) and Room.ready(self.player_second)
