import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.backend.game import Room
from encoder import encode


def test_hit_and_win():
    room = Room()
    first_player = room.player_first
    second_player = room.player_second

    if True:
        room.place_ship(first_player, [(10, 10), (10, 9), (10, 8), (10, 7)])
        room.place_ship(first_player, [(10, 5), (10, 4), (10, 3)])
        room.place_ship(first_player, [(10, 1), (9, 1), (8, 1)])
        room.place_ship(first_player, [(8, 3), (8, 4)])
        room.place_ship(first_player, [(8, 6), (8, 7)])
        room.place_ship(first_player, [(8, 9), (8, 10)])

        assert room.ship_count(first_player) == 6
        assert room.ship_count(second_player) == 0

        room.place_ship(first_player, [(6, 10)])
        room.place_ship(first_player, [(6, 8)])
        room.place_ship(first_player, [(6, 6)])

        assert room.ship_count(first_player) == 9
        assert room.ship_count(second_player) == 0
        assert not room.ready(first_player)
        assert not room.ready(second_player)
        assert not room.is_both_ready()

        room.place_ship(first_player, [(6, 4)])

        assert encode(room.get_field(first_player)) == [
            [-1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, 0, 1, 1, 1, 0],
            [-1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, 0, 0, 0, 1, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 1, 0, 1, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 1, 0, 1, 0, 0, 0],
            [-1, -1, -1, -1, -1, 0, 0, 0, 1, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 1, 0, 0, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 0, 0, 1, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 1, 0, 1, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0]
        ]

        assert room.ship_count(first_player) == 10
        assert room.ship_count(second_player) == 0
        assert room.ready(first_player)
        assert not room.ready(second_player)
        assert not room.is_both_ready()

    if True:
        room.place_ship(second_player, [(1, 10), (1, 9), (1, 8), (1, 7)])
        room.place_ship(second_player, [(1, 5), (1, 4), (1, 3)])
        room.place_ship(second_player, [(1, 1), (2, 1), (3, 1)])
        room.place_ship(second_player, [(3, 3), (3, 4)])
        room.place_ship(second_player, [(3, 6), (3, 7)])
        room.place_ship(second_player, [(3, 9), (3, 10)])

        assert room.ship_count(first_player) == 10
        assert room.ship_count(second_player) == 6

        room.place_ship(second_player, [(5, 10)])
        room.place_ship(second_player, [(5, 8)])
        room.place_ship(second_player, [(5, 6)])

        assert room.ship_count(first_player) == 10
        assert room.ship_count(second_player) == 9
        assert room.ready(first_player)
        assert not room.ready(second_player)
        assert not room.is_both_ready()

        room.place_ship(second_player, [(5, 4)])

        assert encode(room.get_field(second_player)) == [
            [0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 1, 1, 0, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 0, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 1, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1],
            [0, 0, 0, 1, 0, 1, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 0, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 0, 0, 1, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 0, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 1, 0, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1]
        ]

        assert room.ship_count(first_player) == 10
        assert room.ship_count(second_player) == 10
        assert room.ready(first_player)
        assert room.ready(second_player)
        assert room.is_both_ready()

    if True:
        room.start(1)
        assert room.who_playing_now() == first_player
        assert room.who_isnt_playing_now() == second_player

        room.start(2)
        assert room.who_playing_now() == second_player
        assert room.who_isnt_playing_now() == first_player

    if True:
        with pytest.raises(Exception) as excinfo:
            room.hit(first_player, (1, 1))
        assert "Not your turn!" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            room.hit(second_player, (12, 1))
        assert "Error: indexes of the place of the hit are invalid" in str(excinfo.value)

        room.hit(second_player, (1, 1))
        assert encode(room.get_field(first_player)) == [
            [-1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, 0, 1, 1, 1, 0],
            [-1, -1, -2, -1, -1, -1, -1, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, 0, 0, 0, 1, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 1, 0, 1, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 1, 0, 1, 0, 0, 0],
            [-1, -1, -1, -1, -1, 0, 0, 0, 1, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 1, 0, 0, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 0, 0, 1, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 1, 0, 1, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0]
        ]

        assert room.who_playing_now() == first_player
        assert room.who_isnt_playing_now() == second_player

        room.hit(first_player, (9, 0))

        assert encode(room.get_field(second_player)) == [
            [0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 1, 1, 0, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 0, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 1, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1],
            [0, 0, 0, 1, 0, 1, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 0, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 0, 0, 1, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 0, 0, -1, -1, -1, -1, -1],
            [0, 2, 0, 1, 0, 1, 0, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1]
        ]

        room.hit(first_player, (6, 0))

        assert encode(room.get_field(second_player)) == [
            [0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 1, 1, 0, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 0, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 1, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1],
            [0, 0, 0, 1, 0, 1, 0, -1, -1, -1, -1, -1],
            [0, 2, 0, 1, 0, 0, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 0, 0, 1, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 0, 0, -1, -1, -1, -1, -1],
            [0, 2, 0, 1, 0, 1, 0, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1]
        ]

        room.hit(first_player, (7, 0))
        room.hit(first_player, (8, 0))

        assert encode(room.get_field(second_player)) == [
            [0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 1, 1, 0, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 0, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 1, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1],
            [-2, -2, -2, 1, 0, 1, 0, -1, -1, -1, -1, -1],
            [-2, 3, -2, 1, 0, 0, 0, -1, -1, -1, -1, -1],
            [-2, 3, -2, 0, 0, 1, 0, -1, -1, -1, -1, -1],
            [-2, 3, -2, 1, 0, 0, 0, -1, -1, -1, -1, -1],
            [-2, 3, -2, 1, 0, 1, 0, -1, -1, -1, -1, -1],
            [-2, -2, -2, 0, 0, 0, 0, -1, -1, -1, -1, -1]
        ]

        room.hit(first_player, (9, 9))
        assert encode(room.get_field(second_player)) == [
            [0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 1, 1, 0, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 0, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 1, 0, 1, 0, -1, -1, -1, -1, -1],
            [0, 1, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1],
            [-2, -2, -2, 1, 0, 1, 0, -1, -1, -1, -1, -1],
            [-2, 3, -2, 1, 0, 0, 0, -1, -1, -1, -1, -1],
            [-2, 3, -2, 0, 0, 1, 0, -1, -1, -1, -1, -1],
            [-2, 3, -2, 1, 0, 0, 0, -1, -1, -1, -1, -1],
            [-2, 3, -2, 1, 0, 1, 0, -1, -1, -1, -2, -1],
            [-2, -2, -2, 0, 0, 0, 0, -1, -1, -1, -1, -1]
        ]

        assert room.who_playing_now() == second_player
        assert room.who_isnt_playing_now() == first_player

        room.hit(second_player, (0, 0))

        assert room.who_playing_now() == first_player
        assert room.who_isnt_playing_now() == second_player

        with pytest.raises(Exception) as excinfo:
            room.hit(first_player, (9, 9))
        assert "Error: you hit there" in str(excinfo.value)

        room.hit(first_player, (4, 0))
        room.hit(first_player, (3, 0))
        room.hit(first_player, (2, 0))
        room.hit(first_player, (0, 0))
        room.hit(first_player, (0, 1))
        room.hit(first_player, (0, 2))
        room.hit(first_player, (2, 2))
        room.hit(first_player, (3, 2))
        room.hit(first_player, (5, 2))
        room.hit(first_player, (6, 2))
        room.hit(first_player, (8, 2))
        room.hit(first_player, (9, 2))
        room.hit(first_player, (9, 4))
        room.hit(first_player, (7, 4))
        room.hit(first_player, (5, 4))

        assert not room.is_win(first_player)
        assert not room.is_win(second_player)

        assert encode(room.get_field(second_player)) == [
            [-2, -2, -2, -2, -2, -1, -1, -1, -1, -1, -1, -1],
            [-2, 3, 3, 3, -2, -1, -1, -1, -1, -1, -1, -1],
            [-2, -2, -2, -2, -2, -1, -1, -1, -1, -1, -1, -1],
            [-2, 3, -2, 3, -2, 0, 0, -1, -1, -1, -1, -1],
            [-2, 3, -2, 3, -2, 1, 0, -1, -1, -1, -1, -1],
            [-2, 3, -2, -2, -2, -2, -2, -1, -1, -1, -1, -1],
            [-2, -2, -2, 3, -2, 3, -2, -1, -1, -1, -1, -1],
            [-2, 3, -2, 3, -2, -2, -2, -1, -1, -1, -1, -1],
            [-2, 3, -2, -2, -2, 3, -2, -1, -1, -1, -1, -1],
            [-2, 3, -2, 3, -2, -2, -2, -1, -1, -1, -1, -1],
            [-2, 3, -2, 3, -2, 3, -2, -1, -1, -1, -2, -1],
            [-2, -2, -2, -2, -2, -2, -2, -1, -1, -1, -1, -1]
        ]

        assert encode(room.get_field(first_player)) == [
            [-1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0],
            [-1, -2, -1, -1, -1, -1, -1, 0, 1, 1, 1, 0],
            [-1, -1, -2, -1, -1, -1, -1, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, 0, 0, 0, 1, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 1, 0, 1, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 1, 0, 1, 0, 0, 0],
            [-1, -1, -1, -1, -1, 0, 0, 0, 1, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 1, 0, 0, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 0, 0, 1, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 1, 0, 1, 0, 1, 0],
            [-1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0]
        ]

        room.hit(first_player, (3, 4))

        assert room.is_win(first_player)
        assert not room.is_win(second_player)

        assert encode(room.get_field(second_player)) == [
            [-2, -2, -2, -2, -2, -1, -1, -1, -1, -1, -1, -1],
            [-2, 3, 3, 3, -2, -1, -1, -1, -1, -1, -1, -1],
            [-2, -2, -2, -2, -2, -1, -1, -1, -1, -1, -1, -1],
            [-2, 3, -2, 3, -2, -2, -2, -1, -1, -1, -1, -1],
            [-2, 3, -2, 3, -2, 3, -2, -1, -1, -1, -1, -1],
            [-2, 3, -2, -2, -2, -2, -2, -1, -1, -1, -1, -1],
            [-2, -2, -2, 3, -2, 3, -2, -1, -1, -1, -1, -1],
            [-2, 3, -2, 3, -2, -2, -2, -1, -1, -1, -1, -1],
            [-2, 3, -2, -2, -2, 3, -2, -1, -1, -1, -1, -1],
            [-2, 3, -2, 3, -2, -2, -2, -1, -1, -1, -1, -1],
            [-2, 3, -2, 3, -2, 3, -2, -1, -1, -1, -2, -1],
            [-2, -2, -2, -2, -2, -2, -2, -1, -1, -1, -1, -1]
        ]
