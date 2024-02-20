from enum import Enum


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
