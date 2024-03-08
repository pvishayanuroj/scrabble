from enums import Tile
from iterators import BoardIterator
from position import Position
from size import Size


class Scoreboard:
    """The board without any letter tiles on it. Describes the scoring."""

    def __init__(self, board_filepath: str, letter_values_filepath: str):
        self._board = []
        self._letter_values = {}
        num_cols = 0
        with open(board_filepath, "r") as file:
            for line in file.readlines():
                if line == "":
                    continue
                row = [
                    Tile.from_string(tile) for tile in line.strip().upper().split(" ")
                ]
                if num_cols == 0:
                    num_cols = len(row)
                elif num_cols != len(row):
                    raise ValueError(
                        f"Mismatched number of columns. Expected {num_cols}, got {len(row)}"
                    )
                self._board.append(row)
        self._size = Size(len(self._board), num_cols)
        print(f"Loaded scoreboard: {self._size}")
        with open(letter_values_filepath, "r") as file:
            for line in file.readlines():
                if line == "":
                    continue
                elements = line.strip().split(" ")
                if len(elements) != 2:
                    raise ValueError(f"Invalid line for points: {line}")
                self._letter_values[elements[0]] = int(elements[1])
        if len(self._letter_values) != 26:
            raise ValueError(f"Expected 26 letters, got {len(self._letter_values)}")

    def get_letter_value(self, letter: str) -> int:
        return self._letter_values[letter]

    def get_tile(self, position: Position) -> Tile:
        return self._board[position.row][position.col]

    def get_word_multiplier(self, position: Position) -> int:
        tile = self.get_tile(position)
        if tile == Tile.DOUBLE_WORD or tile == Tile.STAR:
            return 2
        elif tile == Tile.TRIPLE_WORD:
            return 3
        else:
            return 1

    def get_letter_multiplier(self, position: Position) -> int:
        tile = self.get_tile(position)
        if tile == Tile.DOUBLE_LETTER:
            return 2
        elif tile == Tile.TRIPLE_LETTER:
            return 3
        else:
            return 1

    def get_star_position(self) -> Position:
        for position in BoardIterator(self._size):
            if self.get_tile(position) == Tile.STAR:
                return position
        raise ValueError("No star tile found.")

    @property
    def size(self) -> Size:
        return self._size
