from __future__ import annotations
import copy
from constants import ENDC, RED
from dictionary import Dictionary
from enums import Direction, MoveStatus, Shape, SolutionState
from iterators import BoardIterator
from placement import Placement
from position import Position
from range import Range
from scoreboard import Scoreboard
from size import Size
from typing import List, Union
from turns import Turn
from turns2 import Turn as Turn2
from word_position import WordPosition


def get_chunks(value: List[str]) -> List[str]:
    chunks = ''.join(map(lambda x: '-' if x == '' else x, value)).split('-')
    return list(filter(lambda x: len(x) > 1, chunks))


class MoveResult:
    def __init__(self, board: Board, status: MoveStatus):
        self._board = board
        self._status = status


class Board:
    def __init__(self, size: Size, dictionary: Dictionary, state = None):
        self._size = size
        self._dictionary = dictionary
        if state:
            self._state = state
        else:
            self._state = [[''] * self._size.num_cols for _ in range(self._size.num_rows)]

    def __str__(self):
        output = ''
        for row in self._state:
            output += ' '.join(map(lambda x: '-' if x == '' else x, row))
            output += '\n'
        return output

    @property
    def size(self) -> Size:
        return self._size

    def is_empty(self) -> bool:
        """Returns whether or not there are no letter tiles on the board."""
        for position in BoardIterator(self._size):
            if self.get_tile(position) != '':
                return False
        return True

    def copy(self):
        return Board(self._size.copy(), self._dictionary, copy.deepcopy(self._state))

    def copy_and_apply_turn(self, turn: Turn) -> Board:
        new_board = self.copy()
        for placement in turn.placements:
            new_board.set_tile(placement)
        return new_board

    def copy_and_apply_turn2(self, turn: Turn2) -> Board:
        new_board = self.copy()
        for placement in turn.placements:
            new_board.set_tile(placement)
        return new_board

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
        print(f"Successfully loaded {filepath}")

    def get_tile(self, position: Position) -> str:
        return self._state[position.row][position.col]

    def get_tile_checked(self, position: Position) -> Union[None, str]:
        """Checks if the tile is within bounds, returning None if not. Otherwise returns the tile."""
        if self._size.is_within_bounds(position):
            return self.get_tile(position)
        return None

    def set_tile(self, placement: Placement):
        if self.is_tile_filled(placement.position):
            raise ValueError(f"Cannot set non-empty tile: {placement.position}.")
        self._state[placement.position.row][placement.position.col] = placement.letter

    def get_adjacent_tile(self, position: Position, direction: Direction) -> Union[None, str]:
        """Returns the value of the adjacent tile or None if the tile is out of bounds."""
        adjacent_position = position.move(direction)
        if self._size.is_within_bounds(adjacent_position):
            return self.get_tile(adjacent_position)
        return None

    def get_adjacent_tiles_until_empty(self, position: Position, direction: Direction) -> str:
        """Traverses in the given direction until the end of the board or an empty tile.

        Returns the string formed by this traversal. Note that the returned string is in always
        left-to-right or up-to-down order even if the traversal direction is left or up.
        """
        output = ''
        curr_position = position
        while True:
            curr_tile = self.get_tile_checked(curr_position)
            if curr_tile == None or curr_tile == '':
                break
            output += curr_tile
        if direction == Direction.LEFT or direction == Direction.UP:
            return output[::-1]
        return output

    def get_last_non_empty_tile(self, position: Position, direction: Direction) -> Position:
        """Gets the N-most tile that is non-empty and contiguous from the given position."""
        curr_position = position
        while True:
            next_position = curr_position.move(direction)
            if not self._size.is_within_bounds(next_position) or self.is_tile_empty(next_position):
                return curr_position
            curr_position = next_position

    def get_next_empty_tile(self, position: Position, direction: Direction) -> None | Position:
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

    def is_state_valid(self, dictionary: Dictionary) -> tuple[bool, List[str]]:
        # Check that all tiles are next to at least one other tile.
        for position in BoardIterator(self._size):
            if self.is_tile_filled(position) and self.are_adjacent_tiles_empty(position):
                print("FOOO")
                return (False, [])
        chunks = []
        # Check rows.
        for row in self._state:
            chunks.extend(get_chunks(row))
        # Check columns.
        for col_num in range(self._size.num_cols):
            chunks.extend(get_chunks(self.get_column(col_num)))

        invalid_words = list(filter(lambda x: not dictionary.is_word(x), chunks))
        if len(invalid_words) > 0:
            return (False, invalid_words)
        return (True, [])

    def get_first_tile_positions(self) -> List[Position]:
        """The possible tiles that a letter can be placed to start the turn.

        This assumes a non-empty board.
        Returns a list of all empty tile positions that are next to non-empty tile positions.
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

    def is_first_move_valid(self, dictionary: Dictionary, position: Position, letter: str) -> tuple[MoveStatus, Board]:
        new_board = self.copy()
        new_board.set_tile(Placement(position, letter))
        horizontal_chunk = new_board.get_chunk(position, Shape.HORIZONTAL)
        vertical_chunk = new_board.get_chunk(position, Shape.VERTICAL)
        is_substring = dictionary.is_substring(horizontal_chunk.word) or dictionary.is_substring(vertical_chunk.word)
        is_word = dictionary.is_word(horizontal_chunk.word) or dictionary.is_word(vertical_chunk.word)
        if not is_word and not is_substring:
            return (MoveStatus.INVALID, new_board)
        if is_word and is_substring:
            return (MoveStatus.PARTIAL_AND_COMPLETE_WORD, new_board)
        if is_word:
            return (MoveStatus.COMPLETE_WORD, new_board)
        if is_substring:
            return (MoveStatus.PARTIAL_WORD, new_board)

    def is_move_valid(self, dictionary: Dictionary, position: Position, letter: str, solution_state: SolutionState) -> tuple[MoveStatus, Board]:
        new_board = self.copy()
        new_board.set_tile(Placement(position, letter))
        if solution_state == SolutionState.HORIZONTAL:
            vertical_chunk = new_board.get_chunk(position, Shape.VERTICAL)
            if len(vertical_chunk.word) > 1 and not dictionary.is_word(vertical_chunk.word):
                return (MoveStatus.INVALID, new_board)
            horizontal_chunk = new_board.get_chunk(position, Shape.HORIZONTAL)
            is_word = dictionary.is_word(horizontal_chunk.word)
            is_substring = dictionary.is_substring(horizontal_chunk.word)
            if not is_word and not is_substring:
                return (MoveStatus.INVALID, new_board)
            if is_word and is_substring:
                return (MoveStatus.PARTIAL_AND_COMPLETE_WORD, new_board)
            if is_word:
                return (MoveStatus.COMPLETE_WORD, new_board)
            if is_substring:
                return (MoveStatus.PARTIAL_WORD, new_board)
            raise ValueError("Invalid state")
        elif solution_state == SolutionState.VERTICAL:
            horizontal_chunk = new_board.get_chunk(position, Shape.HORIZONTAL)
            if len(horizontal_chunk.word) > 1 and not dictionary.is_word(horizontal_chunk.word):
                return (MoveStatus.INVALID, new_board)
            vertical_chunk = new_board.get_chunk(position, Shape.VERTICAL)
            is_word = dictionary.is_word(vertical_chunk.word)
            is_substring = dictionary.is_substring(vertical_chunk.word)
            if not is_word and not is_substring:
                return (MoveStatus.INVALID, new_board)
            if is_word and is_substring:
                return (MoveStatus.PARTIAL_AND_COMPLETE_WORD, new_board)
            if is_word:
                return (MoveStatus.COMPLETE_WORD, new_board)
            if is_substring:
                return (MoveStatus.PARTIAL_WORD, new_board)
        else:
            raise ValueError(f"Unsupported solution state {solution_state}")

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

    def get_word_from_placement(self, placement: Placement, shape: Shape) -> tuple[str, Range]:
        """Assumes the given placement and returns the word formed with the given shape."""
        if shape == Shape.HORIZONTAL:
            start = self.get_last_non_empty_tile(placement.position, Direction.LEFT)
            end = self.get_last_non_empty_tile(placement.position, Direction.RIGHT)
            word = ''
            for col in range(start.col, end.col + 1):
                position = Position(placement.position.row, col)
                tile = self.get_tile(position)
                if tile == '':
                    word += placement.letter
                else:
                    word += tile
            return (word, Range(start, end))
        if shape == Shape.VERTICAL:
            start = self.get_last_non_empty_tile(placement.position, Direction.UP)
            end = self.get_last_non_empty_tile(placement.position, Direction.DOWN)
            word = ''
            for row in range(start.row, end.row + 1):
                position = Position(row, placement.position.col)
                tile = self.get_tile(position)
                if tile == '':
                    word += placement.letter
                else:
                    word += tile
            return (word, Range(start, end))
        raise RuntimeError(f"Invalid shape: {shape}")

    def get_column(self, index) -> List[str]:
        col = []
        for row in self._state:
            col.append(row[index])
        return col

    def save(self, filepath: str):
        with open(filepath, 'w') as file:
            file.write(str(self))
        print(f"Wrote {filepath}")

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

    def get_placements_from_diff(self, other: Board) -> List[Placement]:
        placements = []
        for position in BoardIterator(self._size):
            tile = self.get_tile(position)
            other_tile = other.get_tile(position)
            if tile != other_tile:
                placements.append(Placement(position, tile))
        return placements

    def get_score(self, turn: Turn, scoreboard: Scoreboard) -> int:
        active_tiles = [placement.position for placement in turn.placements]
        if turn.len == 1:
            score = 0
            horizontal_word = self.get_chunk(turn.placements[0].position, Shape.HORIZONTAL)
            if len(horizontal_word.word) > 1:
                score += scoreboard.score_word(horizontal_word, active_tiles)
            vertical_word = self.get_chunk(turn.placements[0].position, Shape.VERTICAL)
            if len(vertical_word.word) > 1:
                score += scoreboard.score_word(vertical_word, active_tiles)
            if score == 0:
                raise ValueError(f"Single turn solution does not form a word at least two letters long.")
            return score
        else:
            is_horizontal = len(set(map(lambda x: x.position.row, turn.placements))) == 1
            shape = Shape.HORIZONTAL if is_horizontal else Shape.VERTICAL
            cross_shape = Shape.VERTICAL if is_horizontal else Shape.HORIZONTAL
            word_position = self.get_chunk(turn.placements[0].position, shape)
            score = scoreboard.score_word(word_position, active_tiles)
            for placement in turn.placements:
                word_position = self.get_chunk(placement.position, cross_shape)
                if len(word_position.word) > 1:
                    score += scoreboard.score_word(word_position, active_tiles)
            return score

    def get_score_temp(self, other_board: Board, scoreboard: Scoreboard) -> int:
        placements = self.get_placements_from_diff(other_board)
        return self.get_score(Turn(placements), scoreboard)
