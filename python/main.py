import os
from enum import Enum
from typing import List


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


class Board:
    def __init__(self):
        self.num_cols = 0
        self.num_rows = 0
        self.board = []
        self.state = []

    def init_board(self, filepath: str):
        self.num_cols = None
        self.board.clear()
        with open(filepath, 'r') as file:
            for line in file.readlines():
                if line == '':
                    continue
                row = [Tile.from_string(tile) for tile in line.strip().upper().split(' ')]
                if self.num_cols is None:
                    self.num_cols = len(row)
                elif self.num_cols != len(row):
                    raise ValueError(f"Mismatched number of columns. Expected {self.num_cols}, got {len(row)}")
                self.board.append(row)
        self.num_rows = len(self.board)
        self.init_state()
        print(f"Initialized board: {self.num_rows} rows by {self.num_cols} cols")

    def init_state(self):
        self.state = [[''] * self.num_cols for _ in range(self.num_rows)]

    def load_state(self, filepath: str):
        if self.num_cols == 0 or self.num_rows == 0:
            raise ValueError(f"Cannot load state without initializing the board.")
        self.state = []
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
                if len(row) != self.num_cols:
                    raise ValueError(f"Expected {self.num_cols} columns, got {len(row)}")
                self.state.append(row)
            if len(self.state) != self.num_rows:
                raise ValueError(f"Expected {self.num_rows} rows, got {len(self.state)}")

    def are_adjacent_tiles_empty(self, position: Position) -> bool:
        # Top
        if position.row != 0 and self.state[position.row - 1][position.col] != '':
            return False
        # Bottom
        if position.row != (self.num_rows - 1) and self.state[position.row + 1][position.col] != '':
            return False
        # Left
        if position.col != 0 and self.state[position.row][position.col - 1] != '':
            return False
        # Right
        if position.col != (self.num_cols - 1) and self.state[position.row][position.col + 1] != '':
            return False
        return True

    def is_state_valid(self, dictionary: Dictionary) -> bool:
        # Check that all tiles are next to at least one other tile.
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.state[row][col] != '' and self.are_adjacent_tiles_empty(Position(row, col)):
                    return False
        # Check rows.
        for row in self.state:
            chunks = ''.join(row).split('-')
            chunks = filter(lambda x: len(x) > 1, chunks)
            if not all(map(lambda x: dictionary.is_word(x), chunks)):
                return False
        # Check columns.
        for col_num in range(self.num_cols):
            chunks = ''.join(self.get_column(col_num)).split('-')
            chunks = filter(lambda x: len(x) > 1, chunks)
            if not all(map(lambda x: dictionary.is_word(x), chunks)):
                return False
        return True

    def get_column(self, index) -> List[str]:
        col = []
        for row in self.state:
            col.append(row[index])
        return col

    def save(self, filepath: str):
        pass

    def __str__(self):
        output = ''
        for row in self.state:
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

board = Board()
board.init_board(BOARD_PATH)
board.load_state(STATE_PATH)

#files = read_directory_files(PATH)
dictionary = Dictionary()
dictionary.load(DICTIONARY_PATH)

is_valid = board.is_state_valid(dictionary)
print(f"is board valid: {is_valid}")


def solver(dictionary: Dictionary, board: Board, tiles: List[str]):
    pass
