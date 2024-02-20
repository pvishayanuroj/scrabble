from enums import Tile
from size import Size


class Scoreboard:
    """The board without any letter tiles on it. Describes the scoring."""
    def __init__(self, filepath: str):
        self._board = []
        self._num_cols = None
        with open(filepath, 'r') as file:
            for line in file.readlines():
                if line == '':
                    continue
                row = [Tile.from_string(tile) for tile in line.strip().upper().split(' ')]
                if self._num_cols is None:
                    self._num_cols = len(row)
                elif self._num_cols != len(row):
                    raise ValueError(f"Mismatched number of columns. Expected {self._num_cols}, got {len(row)}")
                self._board.append(row)
        self._num_rows = len(self._board)
        print(f"Loaded scoreboard: {self._num_rows} rows by {self._num_cols} cols")

    def get_size(self) -> Size:
        return Size(self._num_rows, self._num_cols)
