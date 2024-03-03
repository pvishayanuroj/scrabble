from __future__ import annotations
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

    @property
    def reverse(self) -> Direction:
        if self == Direction.LEFT:
            return Direction.RIGHT
        if self == Direction.RIGHT:
            return Direction.LEFT
        if self == Direction.UP:
            return Direction.DOWN
        if self == Direction.DOWN:
            return Direction.UP
        raise ValueError(f"Invalid direction enum: {self}")


class Shape(Enum):
    """The shape of the word that the current form is taking."""
    UNSPECIFIED_SHAPE = 1,
    VERTICAL = 2,
    HORIZONTAL = 3,

    @property
    def start_direction(self) -> Direction:
        """Returns the direction associated with the start of this shape word."""
        if self == Shape.VERTICAL:
            return Direction.UP
        if self == Shape.HORIZONTAL:
            return Direction.LEFT
        raise ValueError(f"Invalid shape enum: {self}")

    @property
    def end_direction(self) -> Direction:
        """Returns the direction associated with the end of this shape word."""
        if self == Shape.VERTICAL:
            return Direction.DOWN
        if self == Shape.HORIZONTAL:
            return Direction.RIGHT
        raise ValueError(f"Invalid shape enum: {self}")

    @property
    def opposite(self) -> Shape:
        """Returns the opposite shape."""
        if self == Shape.VERTICAL:
            return Shape.HORIZONTAL
        if self == Shape.HORIZONTAL:
            return Shape.VERTICAL
        raise ValueError(f"Invalid shape enum: {self}")

class SolutionState(Enum):
    NO_LETTERS = 1,
    FIRST_LETTER = 2,
    VERTICAL = 3,
    HORIZONTAL = 4,


class TurnStateValue(Enum):
    NO_PLACEMENTS = 1,
    FIRST_PLACEMENT = 2,
    MID_TURN = 3,


class MoveStatus(Enum):
    INVALID = 1,
    PARTIAL_WORD = 2,
    COMPLETE_WORD = 3,
    PARTIAL_AND_COMPLETE_WORD = 4,


class MenuSelection(IntEnum):
    NEW_GAME = 1,
    LOAD_GAME = 2,
    LOAD_FROM_FILE = 3,
    QUIT = 4,

    def __str__(self):
        if self == MenuSelection.NEW_GAME:
            return "New game"
        if self == MenuSelection.LOAD_GAME:
            return "Load game"
        if self == MenuSelection.LOAD_FROM_FILE:
            return "Load from file"
        if self == MenuSelection.QUIT:
            return "Quit"
        return "Missing menu option description"
