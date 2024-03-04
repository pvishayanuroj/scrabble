from typing import List
from constants import MAX_LENGTH_WORD_SCORE, MAX_PLAYER_TILES
from enums import Direction, Shape, Tile
from iterators import BoardIterator
from position import Position
from size import Size
from word_position import WordPosition


class Scoreboard:
    """The board without any letter tiles on it. Describes the scoring."""
    def __init__(self, board_filepath: str, points_filepath: str):
        self._board = []
        self._letter_values = {}
        num_cols = None
        with open(board_filepath, 'r') as file:
            for line in file.readlines():
                if line == '':
                    continue
                row = [Tile.from_string(tile) for tile in line.strip().upper().split(' ')]
                if num_cols is None:
                    num_cols = len(row)
                elif num_cols != len(row):
                    raise ValueError(f"Mismatched number of columns. Expected {num_cols}, got {len(row)}")
                self._board.append(row)
        self._size = Size(len(self._board), num_cols)
        print(f"Loaded scoreboard: {self._size}")
        with open(points_filepath, 'r') as file:
            for line in file.readlines():
                if line == '':
                    continue
                elements = line.strip().split(' ')
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

    def score_word(self, word_position: WordPosition, active_tiles: set[Position]) -> int:
        """Returns the point value of the word starting at the given position.

        The active_tiles list describes which tiles bonus tiles are allowed to be used.
        """
        curr_position = word_position.position
        direction = Direction.DOWN if word_position.shape == Shape.VERTICAL else Direction.RIGHT
        word_multipler = 1
        total = 0
        for letter in word_position.word:
            letter_value = self._letter_values[letter]
            tile = self.get_tile(curr_position)
            letter_multiplier = 1
            if curr_position in active_tiles:
                if tile == Tile.DOUBLE_WORD or tile == Tile.STAR:
                    word_multipler *= 2
                elif tile == Tile.TRIPLE_WORD:
                    word_multipler *= 3
                elif tile == Tile.DOUBLE_LETTER:
                    letter_multiplier = 2
                elif tile == Tile.TRIPLE_LETTER:
                    letter_multiplier = 3
            total += (letter_value * letter_multiplier)
            curr_position = curr_position.move(direction)
        total *= word_multipler
        if len(active_tiles) == MAX_PLAYER_TILES:
            total += MAX_LENGTH_WORD_SCORE
        return total

    @property
    def size(self) -> Size:
        return self._size
