from __future__ import annotations
from constants import MAX_BOARD_SIZE
from enums import Direction


class Position:
    def __init__(self, row: int, col: int):
        self._row = row
        self._col = col

    def __copy__(self):
        return Position(self._row, self._col)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            return NotImplemented
        return self.row == other.row and self.col == other.col

    def __lt__(self, other: Position):
        if self.row != other.row:
            return self.row < other.row
        return self.col < other.col

    def __hash__(self):
        return self.row * MAX_BOARD_SIZE + self.col

    def __str__(self):
        return f"[{self.row}, {self.col}]"

    def __repr__(self):
        return f"[{self.row}, {self.col}]"

    @property
    def row(self) -> int:
        return self._row

    @property
    def col(self) -> int:
        return self._col

    def move(self, direction: Direction, steps: int = 1) -> Position:
        """Moves N steps in the given direction."""
        if direction == Direction.UP:
            return Position(self.row - steps, self.col)
        if direction == Direction.DOWN:
            return Position(self.row + steps, self.col)
        if direction == Direction.LEFT:
            return Position(self.row, self.col - steps)
        if direction == Direction.RIGHT:
            return Position(self.row, self.col + steps)
        raise ValueError(f"Invalid direction: {direction}")
