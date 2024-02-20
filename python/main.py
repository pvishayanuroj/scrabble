import os
from enum import Enum
from typing import List, Union


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


class Dictionary:
    def __init__(self):
        self.words = set()
        self.substrings = set()

    def load(self, filepath: str):
        with open(filepath, 'r') as file:
            for line in file.readlines():
                if line == '':
                    continue
                self.words.add(line.strip().upper())
        self.preprocess()
        print(f"Loaded {len(self.words)} words")
        print(f"Preprocessed {len(self.substrings)} substrings")

    def preprocess(self):
        for word in self.words:
            for substring in get_all_substrings(word):
                self.substrings.add(substring)

    def is_word(self, value: str) -> bool:
        return value in self.words


class Position:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __str__(self):
        return f"[{self.row}, {self.col}]"

    def __repr__(self):
        return f"[{self.row}, {self.col}]"

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


class Size:
    def __init__(self, num_rows: int, num_cols: int):
        self._num_rows = num_rows
        self._num_cols = num_cols

    def is_within_bounds(self, position: Position) -> bool:
        return (position.row >= 0
                and position.row < self._num_rows
                and position.col >= 0
                and position.col < self._num_cols)

    @property
    def num_rows(self) -> int:
        return self._num_rows

    @property
    def num_cols(self) -> int:
        return self._num_cols


class BoardIterator:
    """Iterator to return positions on a board going from left to right, top to bottom."""

    def __init__(self, size: Size):
        self._curr_row = 0
        self._curr_col = 0
        self._size = size

    def __iter__(self):
        return self

    def __next__(self) -> Position:
        self._curr_col += 1
        if self._curr_col == self._size.num_cols:
            self._curr_col = 0
            self._curr_row += 1
        if self._curr_row == self._size.num_rows:
            raise StopIteration
        return Position(self._curr_row, self._curr_col)


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


def get_nth_most_position(positions: List[Position], direction: Direction) -> Position:
    """Of the given tiles, returns the tile in the most ."""
    if len(positions) == 0:
        raise ValueError("Positions cannot be empty")


class Board:
    def __init__(self, size: Size):
        self._size = size
        self._state = [[''] * self._size.num_cols for _ in range(self._size.num_rows)]

    def load_state(self, filepath: str):
        self._state = []
        with open(filepath, 'r') as file:
            for line in file.readlines():
                if line == '':
                    continue
                row = []
                for letter in line.strip().upper().split(' '):
                    if letter == '-':
                        row.append('')
                    elif letter.isupper():
                        row.append(letter)
                    else:
                        raise ValueError(f"Invalid input letter: {letter}")
                if len(row) != self._size.num_cols:
                    raise ValueError(f"Expected {self._size.num_cols} columns, got {len(row)}")
                self._state.append(row)
            if len(self._state) != self._size.num_rows:
                raise ValueError(f"Expected {self._size.num_rows} rows, got {len(self.state)}")

    def get_tile(self, position: Position) -> str:
        return self._state[position.row][position.col]

    def get_adjacent_tile(self, position: Position, direction: Direction) -> Union[None, str]:
        """Returns the value of the adjacent tile or None if the tile is out of bounds."""
        adjacent_position = position.move(direction)
        if self._size.is_within_bounds(adjacent_position):
            return self.get_tile(adjacent_position)
        return None

    def get_next_empty_tile(self, position: Position, direction: Direction) -> Union[None, Position]:
        """Returns the next empty tile in the given direction. Returns None if no empty tiles exist."""
        curr_position = position
        while True:
            new_position = curr_position.move(direction)
            if not self._size.is_within_bounds(new_position):
                return None
            if self.is_tile_empty(new_position):
                return new_position
            curr_position = new_position

    def are_adjacent_tiles_empty(self, position: Position) -> bool:
        for direction in Direction:
            tile = self.get_adjacent_tile(position, direction)
            if tile is not None and tile != '':
                return False
        return True

    def is_tile_empty(self, position: Position) -> bool:
        return self.get_tile(position) == ''

    def is_tile_filled(self, position: Position) -> bool:
        return self.get_tile(position) != ''

    def is_any_adjacent_tile_filled(self, position: Position) -> bool:
        return not self.are_adjacent_tiles_empty(position)

    def is_state_valid(self, dictionary: Dictionary) -> bool:
        # Check that all tiles are next to at least one other tile.
        for position in BoardIterator(self._size):
            if self.is_tile_filled(position) and self.are_adjacent_tiles_empty(position):
                return False
        # Check rows.
        for row in self._state:
            chunks = ''.join(row).split('-')
            chunks = filter(lambda x: len(x) > 1, chunks)
            if not all(map(lambda x: dictionary.is_word(x), chunks)):
                return False
        # Check columns.
        for col_num in range(self._size.num_cols):
            chunks = ''.join(self.get_column(col_num)).split('-')
            chunks = filter(lambda x: len(x) > 1, chunks)
            if not all(map(lambda x: dictionary.is_word(x), chunks)):
                return False
        return True

    def get_first_tile_moves(self) -> List[Position]:
        """The possible tiles that a letter can be placed to start the turn.

        Possible tiles are empty but are next to existing letter tiles.
        """
        positions = []
        for position in BoardIterator(self._size):
            if self.is_tile_empty(position) and self.is_any_adjacent_tile_filled(position):
                positions.append(position)
        return positions

    def get_next_tile_moves(self, previous_moves: List[Position]) -> List[Position]:
        """The possible tiles that a second or later letter can be placed.

        Previous moves cannot be empty.
        Possible tiles will be within a straight line of previous moves.
        """
        if len(previous_moves) == 0:
            raise ValueError(f"Previous moves list cannot be empty.")

        positions = []
        # If this is the second tile, then it can be placed at any of the four directions
        # from the first tile.
        if len(previous_moves) == 1:
            position = previous_moves[0]
            for direction in Direction:
                next_empty_position = self.get_next_empty_tile(position, direction)
                if next_empty_position is not None:
                    positions.append(next_empty_position)
        else:
            # If this is the third or later tile, it must be placed within the same line formed
            # by the previous tiles.
            distinct_cols = set(map(lambda x: x.col, previous_moves))
            distinct_rows = set(map(lambda x: x.row, previous_moves))

            if len(distinct_cols) == 1:
                # Previous tiles form a vertical line.
                col = distinct_cols.pop()
                rows = list(map(lambda x: x.row, previous_moves))
                top = self.get_next_empty_tile(Position(min(rows), col), Direction.UP)
                bottom = self.get_next_empty_tile(Position(max(rows), col), Direction.DOWN)
                if top:
                    positions.append(top)
                if bottom:
                    positions.append(bottom)
            elif len(distinct_rows) == 1:
                # Previous tiles form a horizontal line.
                row = distinct_rows.pop()
                cols = list(map(lambda x: x.col, previous_moves))
                left = self.get_next_empty_tile(Position(row, min(cols)), Direction.LEFT)
                right = self.get_next_empty_tile(Position(row, min(cols)), Direction.RIGHT)
                if left:
                    positions.append(left)
                if right:
                    positions.append(right)
            else:
                raise ValueError(f"Previous moves must form a line: {previous_moves}")
        return positions


    def get_column(self, index) -> List[str]:
        col = []
        for row in self._state:
            col.append(row[index])
        return col

    def save(self, filepath: str):
        pass

    def __str__(self):
        output = ''
        for row in self._state:
            output += ' '.join(map(lambda x: '-' if x == '' else x, row))
            output += '\n'
        return output


def get_all_substrings(word: str) -> List[str]:
    substrings = []
    for substring_len in range(2, len(word)):
        for start_index in range(len(word) - substring_len + 1):
            substrings.append(word[start_index:(start_index + substring_len)])
    return substrings

def read_directory_files(path):
    files = set()
    for filename in os.listdir(path):
        files.add(filename)
    return files

#DICTIONARIES_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries'
DICTIONARY_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries/10k-dictionary.txt'
#DICTIONARY_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries/178k-dictionary.txt'
BOARD_PATH = '/Users/pvishayanuroj/projects/scrabble/boards/official.txt'
STATE_PATH = '/Users/pvishayanuroj/projects/scrabble/states/test.txt'

scoreboard = Scoreboard(BOARD_PATH)

board = Board(scoreboard.get_size())
board.load_state(STATE_PATH)

#files = read_directory_files(PATH)
dictionary = Dictionary()
dictionary.load(DICTIONARY_PATH)

#is_valid = board.is_state_valid(dictionary)
#print(f"is board valid: {is_valid}")
#first_moves = board.get_first_tile_moves()
#print(first_moves)
#next_moves = board.get_next_tile_moves([Position(6, 6)])
next_moves = board.get_next_tile_moves([Position(6, 6), Position(7, 6)])
print(next_moves)


def solver(dictionary: Dictionary, board: Board, tiles: List[str]):
    pass
