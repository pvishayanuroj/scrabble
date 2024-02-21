from enums import Shape, Tile
from position import Position
from size import Size


class Scoreboard:
    """The board without any letter tiles on it. Describes the scoring."""
    def __init__(self, board_filepath: str, points_filepath: str):
        self._board = []
        self._points = {}
        self._num_cols = None
        with open(board_filepath, 'r') as file:
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
        with open(points_filepath, 'r') as file:
            for line in file.readlines():
                if line == '':
                    continue
                elements = line.strip().split(' ')
                if len(elements) != 2:
                    raise ValueError(f"Invalid line for points: {line}")
                self._points[elements[0]] = int(elements[1])
        if len(self._points) != 26:
            raise ValueError(f"Expected 26 letters, got {len(self._points)}")

    def score_word(self, word: str, position: Position, shape: Shape) -> int:
        """Returns the point value of the word starting at the given position."""
        pass


    def get_size(self) -> Size:
        return Size(self._num_rows, self._num_cols)
