from __future__ import annotations
from position import Position


class Size:
    def __init__(self, num_rows: int, num_cols: int):
        self._num_rows = num_rows
        self._num_cols = num_cols

    def copy(self):
        return Size(self._num_rows, self._num_cols)

    def is_within_bounds(self, position: Position) -> bool:
        return (position.row >= 0
                and position.row < self._num_rows
                and position.col >= 0
                and position.col < self._num_cols)

    def __str__(self):
        return f"{self._num_rows} rows by {self._num_cols} cols"

    def __eq__(self, other: Size) -> bool:
        return self.num_cols == other.num_cols and self.num_rows == other.num_rows

    @property
    def num_rows(self) -> int:
        return self._num_rows

    @property
    def num_cols(self) -> int:
        return self._num_cols
