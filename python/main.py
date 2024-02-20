from __future__ import annotations
import copy
import os
from dictionary import Dictionary
from enums import Direction, Shape
from position import Position
from scoreboard import Scoreboard
from size import Size
from typing import List, Union


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


class TurnResult:
    def __init__(self, board: Board, is_word: bool, is_substring: bool):
        self._board = board
        self._is_word = is_word
        self._is_substring = is_substring


class Board:
    def __init__(self, size: Size, state = None):
        self._size = size
        if state:
            self._state = state
        else:
            self._state = [[''] * self._size.num_cols for _ in range(self._size.num_rows)]

    def copy(self):
        return Board(self._size.copy(), copy.deepcopy(self._state))

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

    def set_tile(self, position: Position, letter: str):
        self._state[position.row][position.col] = letter

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
                print("SINGLE TILE FOUND")
                return False
        chunks = []
        # Check rows.
        for row in self._state:
            chunks.extend(get_chunks(row))
        # Check columns.
        for col_num in range(self._size.num_cols):
            chunks.extend(get_chunks(self.get_column(col_num)))

        invalid_words = list(filter(lambda x: not dictionary.is_word(x), chunks))
        if len(invalid_words) > 0:
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

    def is_move_valid(self, position: Position, letter: str) -> Union[None, Board]:
        """Makes a copy of the board and adds the letter at the given position.

        Returns the copy of the board if the letter is valid, otherwise returns None.
        """
        new_board = self.copy()
        new_board.set_tile(position, letter)

    def get_chunk(self, position: Position, shape: Shape) -> str:
        if self.is_tile_empty(position):
            raise ValueError(f"Cannot get chunk from an empty tile at {position}")
        if shape == Shape.HORIZONTAL:
            min_col = position.col
            max_col = position.col
            while True:
                new_position = Position(position.row, min_col - 1)
                if not self._size.is_within_bounds(new_position) or self.is_tile_empty(new_position):
                    break
                min_col -= 1
            while True:
                new_position = Position(position.row, max_col + 1)
                if not self._size.is_within_bounds(new_position) or self.is_tile_empty(new_position):
                    break
                min_col += 1
            return ''.join(self._state[position.row][min_col:max_col + 1])
        elif shape == Shape.VERTICAL:
            min_row = position.row
            max_row = position.row
            while True:
                new_position = Position(min_row - 1, position.col)
                if not self._size.is_within_bounds(new_position) or self.is_tile_empty(new_position):
                    break
                min_row -= 1
            while True:
                new_position = Position(max_row + 1, position.col)
                if not self._size.is_within_bounds(new_position) or self.is_tile_empty(new_position):
                    break
                max_row += 1
            return ''.join(self.get_column(position.col)[min_row:max_row + 1])
        else:
            raise ValueError(f"Invalid shape: {shape}")

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


def get_chunks(value: List[str]) -> List[str]:
    chunks = ''.join(map(lambda x: '-' if x == '' else x, value)).split('-')
    return list(filter(lambda x: len(x) > 1, chunks))

def read_directory_files(path):
    files = set()
    for filename in os.listdir(path):
        files.add(filename)
    return files

#DICTIONARIES_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries'
#DICTIONARY_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries/10k-dictionary.txt'
#DICTIONARY_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries/178k-dictionary.txt'
DICTIONARY_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries/279k-dictionary.txt'
BOARD_PATH = '/Users/pvishayanuroj/projects/scrabble/boards/official.txt'
#STATE_PATH = '/Users/pvishayanuroj/projects/scrabble/states/test.txt'
STATE_PATH = '/Users/pvishayanuroj/projects/scrabble/states/test2.txt'

scoreboard = Scoreboard(BOARD_PATH)

board = Board(scoreboard.get_size())
board.load_state(STATE_PATH)

#files = read_directory_files(PATH)
dictionary = Dictionary()
dictionary.load(DICTIONARY_PATH)

is_valid = board.is_state_valid(dictionary)
print(f"is board valid: {is_valid}")
#first_moves = board.get_first_tile_moves()
#print(first_moves)
#next_moves = board.get_next_tile_moves([Position(6, 6)])
#next_moves = board.get_next_tile_moves([Position(6, 6), Position(7, 6)])
#print(next_moves)
#print(board.get_chunk(Position(7, 7), Shape.VERTICAL))
#print(board.get_chunk(Position(7, 7), Shape.HORIZONTAL))

def solver(dictionary: Dictionary, board: Board, letters: List[str]):
    boards = solver_helper(dictionary, board, letters, [])
    print(f"Generated {len(boards)} boards")

def solver_helper(dictionary: Dictionary, board: Board, letters: List[str], moves: List[Position]):
    """Recursive solver method."""
    #print("------ SOVLER HELPER CALL -----")
    #print(letters)
    #print(moves)
    #print(board)
    boards = []
    if len(moves) == 0:
        next_moves = board.get_first_tile_moves()
        for letter in letters:
            new_letters = list(filter(lambda x: x != letter, letters))
            for next_move in next_moves:
                new_board = board.copy()
                boards.append(new_board)
                new_board.set_tile(next_move, letter)
                new_moves = copy.deepcopy(moves)
                new_moves.append(next_move)
                boards.extend(solver_helper(dictionary, new_board, new_letters, new_moves))
    # else:
    #     next_moves = board.get_next_tile_moves(moves)
    #     for letter in letters:
    #         new_letters = list(filter(lambda x: x != letter, letters))
    #         for next_move in next_moves:
    #             new_board = board.copy()
    #             boards.append(new_board)
    #             new_board.set_tile(next_move, letter)
    #             new_moves = copy.deepcopy(moves)
    #             new_moves.append(next_move)
    #             boards.extend(solver_helper(dictionary, new_board, new_letters, new_moves))
    return boards

letters = 'GUQIDTS'
letters = [letter for letter in letters]

#solver(dictionary, board, letters)
