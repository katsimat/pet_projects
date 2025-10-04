from src.backend.ship import Ship
from src.enums import condition


class Field:
    @staticmethod
    def __initial_def_ship(size_field=10) -> dict[int, int]:
        return {4: 1, 3: 2, 2: 3, 1: 4}

    def __init__(self, size_field=10):
        self.ships = []  # list[Ship]
        self.field = [[]]  # [[condition, Ship]]
        self.def_ships = {}  # {size : cnt_ships}

        size_field += 2
        self.field = [[[condition.free, None] for __ in range(size_field)] for _ in range(size_field)]
        self.def_ships = self.__initial_def_ship(size_field)

    def __pun_condition(self, y_ord: int, x_ord: int, condit: condition):
        self.field[y_ord][x_ord] = [condit, None]

    def __coordinate_in_range(self, index: tuple) -> bool:
        return -1 < index[0] < len(self.field) and 1 < index[1] < len(self.field)

    def __coordinate_in_range_real_field(self, index: tuple) -> bool:
        return 0 < index[0] < len(self.field) - 1 and 0 < index[1] < len(self.field) - 1

    def __replacing_condition_border_ship(self, condit: condition, coord: tuple):
        x = coord[1]
        y = coord[0]

        if not self.field[y][x][0] in [condition.alive, condition.wound, condition.kill]:
            self.__pun_condition(y, x, condit)

        if not self.field[y - 1][x][0] in [condition.alive, condition.wound, condition.kill]:
            self.__pun_condition(y - 1, x, condit)

        if not self.field[y + 1][x][0] in [condition.alive, condition.wound, condition.kill]:
            self.__pun_condition(y + 1, x, condit)

        if not self.field[y - 1][x - 1][0] in [condition.alive, condition.wound, condition.kill]:
            self.__pun_condition(y - 1, x - 1, condit)

        if not self.field[y + 1][x - 1][0] in [condition.alive, condition.wound, condition.kill]:
            self.__pun_condition(y + 1, x - 1, condit)

        if not self.field[y - 1][x + 1][0] in [condition.alive, condition.wound, condition.kill]:
            self.__pun_condition(y - 1, x + 1, condit)

        if not self.field[y + 1][x + 1][0] in [condition.alive, condition.wound, condition.kill]:
            self.__pun_condition(y + 1, x + 1, condit)

        if not self.field[y][x - 1][0] in [condition.alive, condition.wound, condition.kill]:
            self.__pun_condition(y, x - 1, condit)

        if not self.field[y][x + 1][0] in [condition.alive, condition.wound, condition.kill]:
            self.__pun_condition(y, x + 1, condit)

    @staticmethod
    def __check_correct_ship(ship: list[tuple]) -> bool:
        sorted_ship = sorted(ship)
        if len(ship) <= 1:
            return True
        x_same = sorted_ship[0][1] == sorted_ship[1][1]
        y_same = sorted_ship[0][0] == sorted_ship[1][0]

        if not (x_same or y_same):
            return False

        if x_same:
            for i in range(len(ship) - 1):
                if abs(sorted_ship[i][1] - sorted_ship[i + 1][1]) != 0:
                    return False
                if abs(sorted_ship[i][0] - sorted_ship[i + 1][0]) > 1:
                    return False
        if y_same:
            for i in range(len(ship) - 1):
                if abs(sorted_ship[i][0] - sorted_ship[i + 1][0]) != 0:
                    return False
                if abs(sorted_ship[i][1] - sorted_ship[i + 1][1]) > 1:
                    return False
        return True

    @staticmethod
    def __coord_in_ship(coord: tuple, ship: list[tuple]) -> bool:
        return coord in ship

    def put_ship(self, coordinates: list[tuple]):
        """index belong [1, size_ship] \n
        field[y][x] \n
        numbering from the upper left corner to the lower right \n
        begin_x, begin_y = indexes started ship; direct = direction.something; size_ship = cnt decks of the ship"""

        if not self.__check_correct_ship(coordinates):
            raise Exception("Error: incorrect ship coordinates")

        try: 
            self.def_ships[len(coordinates)]
        except:
            raise Exception("Error: so long ship")
        
        if self.def_ships[len(coordinates)] <= 0:
            raise Exception("Error: you cant put this type ships")

        this_ship = Ship()
        this_ship.size_ship = len(coordinates)
        this_ship.coordinates = []
        x = coordinates[0][1]
        y = coordinates[0][0]

        if (not (self.__coordinate_in_range_real_field((x, y))) or
                self.field[y][x][0] != condition.free):
            raise Exception("Error: not free cell begin")

        for i in range(len(coordinates)):
            y_ord, x_ord = coordinates[i]
            if not (self.__coordinate_in_range_real_field((y_ord, x_ord))):
                raise Exception("Error: long ship")
            if self.field[y_ord][x_ord][0] != condition.free:
                raise Exception("Error: not free cells on way")

            this_ship.coordinates.append((y_ord, x_ord))

            self.field[y_ord][x_ord] = [condition.alive, this_ship]

        for i in range(len(coordinates)):
            self.__replacing_condition_border_ship(condition.ban, coordinates[i])

        self.ships.append(this_ship)
        self.def_ships[len(coordinates)] -= 1

    def get_field(self) -> list[list[list[condition | None]]]:
        """indexes in [1, n]"""
        return self.field

    def make_hit(self, coordinate: tuple) -> condition:
        y = coordinate[0]
        x = coordinate[1]
        if not self.__coordinate_in_range_real_field((x, y)):
            raise Exception("Error: indexes of the place of the hit are invalid")

        # проверка что не ударили в ту же клетку
        if (self.field[y][x][0] == condition.miss or self.field[y][x][0] == condition.kill or
                self.field[y][x][0] == condition.wound):
            raise Exception("Error: you hit there")

        # удар по кораблю
        if self.field[y][x][0] == condition.alive or self.field[y][x][0] == condition.wound:
            self.field[y][x][1].wounded += 1
            if self.field[y][x][1].wounded < self.field[y][x][1].size_ship:
                self.field[y][x][0] = condition.wound
                return condition.wound
            else:
                self.field[y][x][0] = condition.kill
                size_ship = 0
                for y_i, x_i in self.field[y][x][1].coordinates:
                    self.field[y_i][x_i][0] = condition.kill
                    size_ship += 1
                for coord in self.field[y][x][1].coordinates:
                    self.__replacing_condition_border_ship(condition.miss, coord)

                for i in range(len(self.ships)):
                    if Field.__coord_in_ship(coordinate, self.ships[i].coordinates):
                        self.ships.pop(i)
                        break

                return condition.kill

        # удар по пустой или забаненной клетке
        self.field[y][x][0] = condition.miss
        return condition.miss

    def remove_ship(self, coordinates: list[tuple]):
        for coord in coordinates:
            self.__replacing_condition_border_ship(condition.free, coord)
            self.__pun_condition(coord[0], coord[1], condition.free)

        for i in range(len(self.ships)):
            if Field.__coord_in_ship(coordinates[0], self.ships[i].coordinates):
                self.ships.pop(i)
                break

        for ship in self.ships:
            for coord in ship.coordinates:
                self.__replacing_condition_border_ship(condition.ban, coord)

    def field_size(self) -> int:
        return len(self.field[0])

    def end_game(self) -> bool:
        return len(self.ships) == 0

    def ship_count(self) -> int:
        return len(self.ships)

    def all_ships_put(self) -> bool:
        for elem in self.def_ships:
            if self.def_ships[elem] != 0:
                return False
        return True
