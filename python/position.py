from __future__ import annotations
from enums import Direction


class Position:
    def __init__(self, row: int, col: int):
        self._row = row
        self._col = col

    def __copy__(self):
        return Position(self._row, self._col)

    def __eq__(self, other: Position) -> bool:
        return self.row == other.row and self.col == other.col

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

    def move(self, direction: Direction):
        """Moves one unit in the given direction."""
        if direction == Direction.UP:
            return Position(self.row - 1, self.col)
        if direction == Direction.DOWN:
            return Position(self.row + 1, self.col)
        if direction == Direction.LEFT:
            return Position(self.row, self.col - 1)
        if direction == Direction.RIGHT:
            return Position(self.row, self.col + 1)
        raise ValueError(f"Invalid direction: {direction}")
