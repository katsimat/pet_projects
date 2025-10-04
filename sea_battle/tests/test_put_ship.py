import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.backend.game import Room
from encoder import encode


def test_put_ship():
    r = Room()

    first_player = r.player_first
    second_player = r.player_second

    assert first_player != second_player

    assert encode(r.get_field(first_player)) == encode(r.get_field(second_player)) == [
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    ]

    if True:
        r.place_ship(first_player, [(1, 1), (1, 2), (1, 3)])

        assert encode(r.get_field(first_player)) == [
            [0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ]

        assert encode(r.get_field(second_player)) == [
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ]

    if True:
        with pytest.raises(Exception) as excinfo:
            r.place_ship(first_player, [(2, 3), (1, 3)])
        assert "Error: not free cell begin" in str(excinfo.value)

        assert encode(r.get_field(first_player)) == [
            [0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ]

        assert encode(r.get_field(second_player)) == [
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ]

    if True:
        r.place_ship(second_player, [(10, 3), (9, 3)])

        assert encode(r.get_field(second_player)) == [
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 1, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ]

        assert encode(r.get_field(first_player)) == [
            [0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [0, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        ]

    if True:
        with pytest.raises(Exception) as excinfo:
            r.place_ship(first_player, [(7, 5), (4, 5)])
        assert "Error: incorrect ship coordinates" in str(excinfo.value)

    if True:
        with pytest.raises(Exception) as excinfo:
            r.place_ship(first_player, [(7, 3), (7, 4), (7, 5), (7, 6), (7, 7)])
        assert "Error: so long ship" in str(excinfo.value)

    if True:
        r.place_ship(first_player, [(7, 3), (7, 4), (7, 5), (7, 6)])

        with pytest.raises(Exception) as excinfo:
            r.place_ship(first_player, [(8, 3), (8, 4), (8, 5), (8, 6)])
        assert "Error: you cant put this type ships" in str(excinfo.value)

        assert encode(r.get_field(second_player)) == [
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 1, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

        ]

    if True:
        r.place_ship(first_player, [(5, 5)])

        with pytest.raises(Exception) as excinfo:
            r.place_ship(first_player, [(8, 3), (7, 9)])
        assert "Error: incorrect ship coordinates" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            r.place_ship(first_player, [(8, 3), (8, 5), (8, 6)])
        assert "Error: incorrect ship coordinates" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            r.place_ship(first_player, [(8, 3), (8, 4), (9, 5)])
        assert "Error: incorrect ship coordinates" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            r.place_ship(first_player, [(3, 8), (4, 8), (5, 9)])
        assert "Error: incorrect ship coordinates" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            r.place_ship(first_player, [(3, 8), (5, 8), (6, 8)])
        assert "Error: incorrect ship coordinates" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            r.place_ship(first_player, [(10, 8), (11, 8)])
        assert "Error: long ship" in str(excinfo.value)

        with pytest.raises(Exception) as excinfo:
            r.place_ship(first_player, [(3, 5), (4, 5), (5, 5)])
        assert "Error: not free cells on way" in str(excinfo.value)

    for row in encode(r.get_field(second_player)):
        print(row, ',', sep='')
