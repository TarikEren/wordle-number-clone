from enum import Enum, auto

# All available statuses for a given digit
class DigitStatus(Enum):
    CORRECT   =   auto()
    MISPLACED =   auto()
    WRONG     =   auto()

# All available statuses for a given game state
class GameStatus(Enum):
    WON     =   auto()
    ONGOING =   auto()
    LOST    =   auto()