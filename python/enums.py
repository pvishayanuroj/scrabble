from enum import Enum, IntEnum


class Tile(Enum):
    NORMAL = "--"
    DOUBLE_LETTER = "DL"
    TRIPLE_LETTER = "TL"
    DOUBLE_WORD = "DW"
    TRIPLE_WORD = "TW"
    STAR = "ST"

    @staticmethod
    def from_string(value: str):
        for tile in Tile:
            if tile.value == value:
                return tile
        raise ValueError(f"Invalid tile enum value: |{value}|")


class Direction(Enum):
    LEFT = 1,
    RIGHT = 2,
    UP = 3,
    DOWN = 4,


class Shape(Enum):
    """The shape of the word that the current form is taking."""
    VERTICAL = 1,
    HORIZONTAL = 2,


class SolutionState(Enum):
    NO_LETTERS = 1,
    FIRST_LETTER = 2,
    VERTICAL = 3,
    HORIZONTAL = 4,


class MoveStatus(Enum):
    INVALID = 1,
    PARTIAL_WORD = 2,
    COMPLETE_WORD = 3,
    PARTIAL_AND_COMPLETE_WORD = 4,


class MenuSelection(IntEnum):
    LOAD_GAME = 1,
    LOAD_FROM_FILE = 2,
    UPDATE_BOARD = 3,
    QUIT = 4,

    def __str__(self):
        if self == MenuSelection.LOAD_GAME:
            return "Load game"
        if self == MenuSelection.LOAD_FROM_FILE:
            return "Load from file"
        if self == MenuSelection.UPDATE_BOARD:
            return "Update board"
        if self == MenuSelection.QUIT:
            return "Quit"
        return "Missing menu option description"
