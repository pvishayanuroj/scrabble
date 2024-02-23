from __future__ import annotations
import copy
import os
import time
from enums import Direction, Shape
from position import Position
from dictionary import Dictionary
from iterators import NextLetterIterator
from word_position import WordPosition
from scoreboard import Scoreboard
from size import Size
from typing import List, Union


RED = '\033[91m'
ENDC = '\033[0m'


class BoardIterator:
    """Iterator to return positions on a board going from left to right, top to bottom."""

    def __init__(self, size: Size):
        self._curr_row = 0
        self._curr_col = 0
        self._size = size

    def __iter__(self):
        return self

    def __next__(self) -> Position:
        position = Position(self._curr_row, self._curr_col)
        self._curr_col += 1
        if self._curr_col == self._size.num_cols:
            self._curr_col = 0
            self._curr_row += 1
        if position.row == self._size.num_rows:
            raise StopIteration
        return position


class Turn:
    def __init__(self, position: Position, letter: str):
        self._position = position
        self._letter = letter

    @property
    def position(self) -> Position:
        return self._position

    @property
    def letter(self) -> str:
        return self._letter


class Solution:
    def __init__(self, turns: List[Turn]):
        self._turns = turns

    @property
    def turns(self) -> List[Turn]:
        return self._turns


class Board:
    def __init__(self, size: Size, state = None):
        self._size = size
        if state:
            self._state = state
        else:
            self._state = [[''] * self._size.num_cols for _ in range(self._size.num_rows)]

    @property
    def size(self) -> Size:
        return self._size

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
        if self.is_tile_filled(position):
            raise ValueError(f"Cannot set non-empty tile: {position}.")
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

    def is_first_move_valid(self, dictionary: Dictionary, position: Position, letter: str) -> Union[None, Board]:
        new_board = self.copy()
        new_board.set_tile(position, letter)
        horizontal_chunk = new_board.get_chunk(position, Shape.HORIZONTAL)
        vertical_chunk = new_board.get_chunk(position, Shape.VERTICAL)
        is_valid = dictionary.is_substring(horizontal_chunk.word) or dictionary.is_substring(vertical_chunk.word)
        if is_valid:
            return new_board
        return None

    def is_next_move_valid(self, dictionary: Dictionary, position: Position, letter: str) -> Union[None, Board]:
        new_board = self.copy()
        new_board.set_tile(position, letter)


    def get_chunk(self, position: Position, shape: Shape) -> WordPosition:
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
                max_col += 1
            word = ''.join(self._state[position.row][min_col:max_col + 1])
            return WordPosition(Position(position.row, min_col), word, shape)
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
            word = ''.join(self.get_column(position.col)[min_row:max_row + 1])
            return WordPosition(Position(min_row, position.col), word, shape)
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

    def get_diff(self, other: Board) -> str:
        if self._size != other.size:
            raise ValueError(f"Cannot print diff of different sized boards.")
        output = ''
        for position in BoardIterator(self._size):
            tile = self.get_tile(position)
            tile = '-' if tile == '' else tile
            other_tile = other.get_tile(position)
            other_tile = '-' if other_tile == '' else other_tile
            if tile != other_tile:
                output += f"{RED}{tile}{ENDC} "
            else:
                output += f"{tile} "
            if position.col == (self._size.num_cols - 1):
                output += "\n"
        return output

    def get_solution_from_diff(self, other: Board) -> Solution:
        turns = []
        for position in BoardIterator(self._size):
            tile = self.get_tile(position)
            other_tile = other.get_tile(position)
            if tile != other_tile:
                turns.append(Turn(position, tile))
        return Solution(turns)

    def get_score(self, solution: Solution, scoreboard: Scoreboard) -> int:
        turns = solution.turns
        active_tiles = [turn.position for turn in turns]
        if len(turns) == 1:
            score = 0
            horizontal_word = self.get_chunk(turns[0].position, Shape.HORIZONTAL)
            if len(horizontal_word.word) > 1:
                score += scoreboard.score_word(horizontal_word, active_tiles)
            vertical_word = self.get_chunk(turns[0].position, Shape.VERTICAL)
            if len(vertical_word.word) > 1:
                score += scoreboard.score_word(vertical_word, active_tiles)
            if score == 0:
                raise ValueError(f"Single turn solution does not form a word at least two letters long.")
            return score
        else:
            is_horizontal = len(set(map(lambda x: x.position.row, turns))) == 1
            shape = Shape.HORIZONTAL if is_horizontal else Shape.VERTICAL
            cross_shape = Shape.VERTICAL if is_horizontal else Shape.HORIZONTAL
            word_position = self.get_chunk(turns[0].position, shape)
            score = scoreboard.score_word(word_position, active_tiles)
            for turn in turns:
                word_position = self.get_chunk(turn.position, cross_shape)
                if len(word_position.word) > 1:
                    score += scoreboard.score_word(word_position, active_tiles)
            return score

    def get_score_temp(self, other_board: Board, scoreboard: Scoreboard) -> int:
        solution = self.get_solution_from_diff(other_board)
        return self.get_score(solution, scoreboard)

def get_chunks(value: List[str]) -> List[str]:
    chunks = ''.join(map(lambda x: '-' if x == '' else x, value)).split('-')
    return list(filter(lambda x: len(x) > 1, chunks))

def read_directory_files(path):
    files = set()
    for filename in os.listdir(path):
        files.add(filename)
    return files

def get_shape(previous_move: Position, current_move: Position) -> Shape:
    if previous_move.col == current_move.col:
        return Shape.VERTICAL
    elif previous_move.row == current_move.row:
        return Shape.HORIZONTAL
    else:
        raise ValueError(f"Cannot get shape of previous move {previous_move} and current move {current_move}")

#DICTIONARIES_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries'
#DICTIONARY_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries/10k-dictionary.txt'
#DICTIONARY_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries/178k-dictionary.txt'
DICTIONARY_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries/279k-dictionary.txt'
BOARD_PATH = '/Users/pvishayanuroj/projects/scrabble/boards/official.txt'
#STATE_PATH = '/Users/pvishayanuroj/projects/scrabble/states/test.txt'
#STATE_PATH = '/Users/pvishayanuroj/projects/scrabble/states/test2.txt'
#STATE_PATH = '/Users/pvishayanuroj/projects/scrabble/states/test3.txt'
STATE_PATH = '/Users/pvishayanuroj/projects/scrabble/states/test4.txt'
POINTS_PATH = '/Users/pvishayanuroj/projects/scrabble/points.txt'

scoreboard = Scoreboard(BOARD_PATH, POINTS_PATH)

board = Board(scoreboard.get_size())
board.load_state(STATE_PATH)

# turns = [
#     Turn(Position(11, 7), 'O'),
#     Turn(Position(12, 7), 'G'),
#     Turn(Position(13, 7), 'U'),
#     Turn(Position(14, 7), 'E'),
# ]
# solution = Solution(turns)
# for turn in turns:
#     board.set_tile(turn.position, turn.letter)
# print(board)
# print(board.get_score(solution, scoreboard))

#files = read_directory_files(PATH)
dictionary = Dictionary()
dictionary.load(DICTIONARY_PATH)

if not board.is_state_valid(dictionary):
    print("Invalid board state")

# is_valid = board.is_state_valid(dictionary)
# print(f"is board valid: {is_valid}")
#first_moves = board.get_first_tile_moves()
#print(first_moves)
#next_moves = board.get_next_tile_moves([Position(6, 6)])
#next_moves = board.get_next_tile_moves([Position(6, 6), Position(7, 6)])
#print(next_moves)
#print(board.get_chunk(Position(7, 7), Shape.VERTICAL))
#print(board.get_chunk(Position(7, 7), Shape.HORIZONTAL))

def solver(dictionary: Dictionary, board: Board, letters: List[str]):
    start_time = time.time()
    boards = solver_helper(dictionary, board, letters, [])
    board_generation_time = time.time()
    print(f"Generated {len(boards)} boards in {(board_generation_time - start_time):.2f} secs")
    valid_boards: List[Board] = list(filter(lambda x: x.is_state_valid(dictionary), boards))
    board_pruning_time = time.time()
    print(f"Prune down to {len(valid_boards)} boards in {(board_pruning_time - board_generation_time):.2f} secs")

    scored_boards = list(map(lambda x: (x, x.get_score_temp(board, scoreboard)), valid_boards))
    scored_boards.sort(key=lambda x: x[1], reverse = True)
    final_boards = scored_boards[:20]

    for index, (final_board, score) in enumerate(final_boards):
        print(f"Board {index}, Score {score}")
        print(final_board.get_diff(board))

def solver_helper(dictionary: Dictionary, board: Board, letters: List[str], moves: List[Position]):
    """Recursive solver method."""
    #print("------ SOVLER HELPER CALL -----")
    #print(letters)
    #print(moves)
    #print(board)
    boards = []
    if len(moves) == 0:
        next_moves = board.get_first_tile_moves()
        for (letter, next_letters) in NextLetterIterator(letters):
            #for letter in letters:
            #next_letters = list(filter(lambda x: x != letter, letters))
            for next_move in next_moves:
                maybe_board = board.is_first_move_valid(dictionary, next_move, letter)
                if maybe_board:
                    boards.append(maybe_board)
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(next_move)
                    boards.extend(solver_helper(dictionary, maybe_board, next_letters, new_moves))
    # elif len(moves) == 1:
    #     previous_move = moves[0]
    #     next_moves = board.get_next_tile_moves(moves)
    #     for letter in letters:
    #         new_letters = list(filter(lambda x: x != letter, letters))
    #         for next_move in next_moves:
    #             shape = get_shape(previous_move, next_move)
    else:
        next_moves = board.get_next_tile_moves(moves)
        for (letter, next_letters) in NextLetterIterator(letters):
            #for letter in letters:
            #next_letters = list(filter(lambda x: x != letter, letters))
            for next_move in next_moves:
                maybe_board = board.is_first_move_valid(dictionary, next_move, letter)
                if maybe_board:
                    boards.append(maybe_board)
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(next_move)
                    boards.extend(solver_helper(dictionary, maybe_board, next_letters, new_moves))

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

#letters = 'GETHUTO'
letters = 'NRALEFI'
letters = [letter for letter in letters]

solver(dictionary, board, letters)
