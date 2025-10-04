from enum import Enum


class condition(Enum):
    miss = -2
    free = -1
    ban = 0
    alive = 1
    wound = 2
    kill = 3
