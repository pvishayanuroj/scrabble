import os
from enum import Enum

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
    def __init__(self, board, state = None):
        self.board = board
        if state is None:
            self.state = []
            for x in len(self.board):
                self.state.append([''] * len(self.board))
        else:
            self.state = state


def read_directory_files(path):
    files = set()
    for filename in os.listdir(path):
        files.add(filename)
    return files


def read_dictionary(filepath):
    words = set()
    with open(filepath, 'r') as file:
        for line in file.readlines():
            if line == '':
                continue
            words.add(line.strip().upper())
    return words


def read_board(filepath):
    board = []
    with open(filepath, 'r') as file:
        for line in file.readlines():
            row = []
            for tile in line.strip().upper().split(' '):
                row.append(Tile.from_string(tile))
            board.append(row)
    return board

def read_state(path):
    state = []
    return state

PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries'

DICTIONARY_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries/10k-dictionary.txt'
BOARD_PATH = '/Users/pvishayanuroj/projects/scrabble/boards/official.txt'

#files = read_directory_files(PATH)
words = read_dictionary(DICTIONARY_PATH)
board = read_board(BOARD_PATH)
print(f"Board size: {len(board)}")
print(f"Dictionary length: {len(words)}")
