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
                    if letter == '-' or letter.isupper():
                        row.append(letter)
                    else:
                        raise ValueError(f"Invalid input letter: {letter}")
                if len(row) != self.num_cols:
                    raise ValueError(f"Expected {self.num_cols} columns, got {len(row)}")
                self.state.append(row)
            if len(self.state) != self.num_rows:
                raise ValueError(f"Expected {self.num_rows} rows, got {len(self.state)}")

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

def read_directory_files(path):
    files = set()
    for filename in os.listdir(path):
        files.add(filename)
    return files

def read_state(path):
    state = []
    return state

PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries'

#DICTIONARY_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries/10k-dictionary.txt'
DICTIONARY_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries/178k-dictionary.txt'
BOARD_PATH = '/Users/pvishayanuroj/projects/scrabble/boards/official.txt'
STATE_PATH = '/Users/pvishayanuroj/projects/scrabble/states/test.txt'

board = Board()
board.init_board(BOARD_PATH)
board.load_state(STATE_PATH)
print(board)
#files = read_directory_files(PATH)
#dictionary = Dictionary()
#dictionary.load(DICTIONARY_PATH)
