from tkinter import *
from tkinter.messagebox import showerror

from src.GUI.square import Square
from src.constants import *
from src.enums import condition


class Window:
    def __init__(self):
        self._root = Tk()
        self._root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self._root.title("The best Sea Battle")

        self._my_squares = [[Square(self._root, bg=PLAYGROUND_COLOR) for _ in range(SQUARE_COUNT)]
                            for __ in range(SQUARE_COUNT)]
        self._other_squares = [[Square(self._root, bg=PLAYGROUND_COLOR) for _ in range(SQUARE_COUNT)]
                               for __ in range(SQUARE_COUNT)]

        Window._draw_play_square(self._my_squares, PLAYGROUND_INDENT_W, PLAYGROUND_INDENT_H)
        Window._draw_play_square(self._other_squares,
                                 WINDOW_WIDTH - SQUARE_COUNT * Window._get_small_square_size() -
                                 (SQUARE_COUNT - 1) * INDENT - PLAYGROUND_INDENT_W,
                                 PLAYGROUND_INDENT_H)

        self._ship_created = None
        self._current_ship = None
        self.destroyed = None
        self.hitted = None
        self._label = None

        self._add_label()

        self._add_field_names()

        self._adding_ships()

        self._check_cancel()

        self._root.bind('<Destroy>', lambda event: setattr(self, 'destroyed', True))
        self._root.bind('<Control-z>', lambda event: self._remove_last_added())

    def _check_cancel(self):
        self._should_close = BooleanVar(value=False)
        self._should_close.trace("w", self._destroy)

    def _destroy(self, *args):
        self._root.destroy()

    def destroy(self):
        self._should_close.set(True)

    def _add_field_names(self):
        own_label = Label(
            self._root,
            text="Your ships",
            font=(FONT_NAME, FONT_SIZE),
            foreground=GREEN_COLOR
        )
        own_label.place(relx=OUR_FIELD_NAME_RELX, rely=FIELD_NAME_RELY, anchor='sw')

        other_label = Label(
            self._root,
            text="Opponent ships",
            font=(FONT_NAME, FONT_SIZE),
            foreground=RED_COLOR
        )
        other_label.place(relx=OTHER_FIELD_NAME_RELX, rely=FIELD_NAME_RELY, anchor='se')

    def _add_label(self):
        self._label = Label(self._root)
        self._label.pack(pady=20)

    def write_on_label(self, text: str, color: str):
        self._label.config(text=text, foreground=color, font=(FONT_NAME, FONT_SIZE))

    def start(self):
        self._root.mainloop()

    @staticmethod
    def do_nothing():
        pass

    def _remove_last_added(self):
        if self._current_ship:
            self.rebind_square_on_adding(self._current_ship[-1][1] - 1, self._current_ship[-1][0] - 1)
            self._current_ship.pop()

    def reset_added_ship(self):
        self._current_ship = []
        self._ship_created = None

    def _rebind_on_adding(self, _i, _j):
        self._current_ship.append((self._my_squares[_i][_j].x + 1, self._my_squares[_i][_j].y + 1)) \
            if (self._my_squares[_i][_j].x + 1, self._my_squares[_i][_j].y + 1) not in self._current_ship else None

        self._my_squares[_i][_j].configure(bg=TARGET_COLOR)

    def rebind_square_on_adding(self, i, j):
        self._my_squares[i][j].configure(
            command=lambda _i=i, _j=j: self._rebind_on_adding(_i, _j),
            background=PLAYGROUND_COLOR)

    def reset_ship(self):
        for elem in self._current_ship:
            self.rebind_square_on_adding(elem[1] - 1, elem[0] - 1)

    def refresh_my_field(self, squares: list[list[int]], do_nothing=False, border=True):
        for i in range(1, len(squares) - 1):
            for j in range(1, len(squares[i]) - 1):
                if squares[i][j] == condition.miss.value:
                    self._my_squares[i - 1][j - 1].configure(command=Window.do_nothing, bg=MISSED_COLOR)
                elif squares[i][j] == condition.free.value and do_nothing:
                    self._my_squares[i - 1][j - 1].configure(command=Window.do_nothing)
                elif squares[i][j] == condition.ban.value:
                    self._my_squares[i - 1][j - 1].configure(command=Window.do_nothing,
                                                             bg=(BANNED_COLOR if border else PLAYGROUND_COLOR))
                elif squares[i][j] == condition.alive.value:
                    self._my_squares[i - 1][j - 1].configure(command=Window.do_nothing, bg=ALIVE_COLOR)
                elif squares[i][j] == condition.wound.value:
                    self._my_squares[i - 1][j - 1].configure(command=Window.do_nothing, bg=WOUNDED_COLOR)
                elif squares[i][j] == condition.kill.value:
                    self._my_squares[i - 1][j - 1].configure(command=Window.do_nothing, bg=KILLED_COLOR)

    def refresh_other_field(self, squares: list[list[int]]):
        if not squares:
            return
        for i in range(1, len(squares) - 1):
            for j in range(1, len(squares[i]) - 1):
                if squares[i][j] == condition.miss.value:
                    self._other_squares[i - 1][j - 1].configure(command=Window.do_nothing, bg=MISSED_COLOR)
                elif squares[i][j] == condition.wound.value:
                    self._other_squares[i - 1][j - 1].configure(command=Window.do_nothing, bg=WOUNDED_COLOR)
                elif squares[i][j] == condition.kill.value:
                    self._other_squares[i - 1][j - 1].configure(command=Window.do_nothing, bg=KILLED_COLOR)

    def is_ship_created(self) -> tuple[bool, list[list[(int, int)]]]:
        return bool(self._ship_created), self._current_ship if self._ship_created else None

    def _adding_ships(self):
        # rebind 'enter' to confirm ship squares
        self._root.bind('<Return>', lambda event: setattr(self, '_ship_created', True))

        self._ship_created = False
        self._current_ship = []

        # rebind every square of our field to add this one to our current ship
        for i in range(SQUARE_COUNT):
            for j in range(SQUARE_COUNT):
                self.rebind_square_on_adding(i, j)

    @staticmethod
    def _get_small_square_size() -> int:
        return (PLAYGROUND_SIZE - INDENT * (SQUARE_COUNT - 1)) / SQUARE_COUNT

    @staticmethod
    def _get_pos_from_index(_x: int) -> int:
        return _x * Window._get_small_square_size() + _x * INDENT

    @staticmethod
    def _draw_small_square(obj: Square, left: int, top: int) -> None:
        obj.place(x=left, y=top, width=Window._get_small_square_size(), height=Window._get_small_square_size())

    @staticmethod
    def _draw_play_square(squares: list[list[Square]], left: int, top: int) -> None:
        for i in range(SQUARE_COUNT):
            for j in range(SQUARE_COUNT):
                Window._draw_small_square(squares[i][j], left + Window._get_pos_from_index(j), top +
                                          Window._get_pos_from_index(i))

                squares[i][j].x = j
                squares[i][j].y = i

    @staticmethod
    def show_alert(message: str):
        showerror(title="Warning!", message=message)

    def rebind_other_field_to_hit(self):
        for i in range(SQUARE_COUNT):
            for j in range(SQUARE_COUNT):
                self._other_squares[i][j].configure(command=lambda _i=i, _j=j: setattr(self, "hitted", (_i, _j)))
