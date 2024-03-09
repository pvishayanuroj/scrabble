from __future__ import annotations
import copy
from constants import CYAN, ENDC, RED
from dictionary import Dictionary
from enums import Direction, Shape
from iterators import BoardIterator
from letter import Letter
from placement import Placement
from position import Position
from range import Range
from size import Size
from typing import Optional, Union


def get_chunks(value: list[Optional[Letter]]) -> list[str]:
    chunks = ''.join(map(lambda x: '-' if x is None else x.val, value)).split('-')
    return list(filter(lambda x: len(x) > 1, chunks))


class Board:
    def __init__(self, size: Size, dictionary: Dictionary, state: Optional[list[list[Optional[Letter]]]] = None):
        self._size = size
        self._dictionary = dictionary
        self._state: list[list[Optional[Letter]]] = [[None] * self._size.num_cols for _ in range(self._size.num_rows)]
        if state:
            self._state = state

    def __str__(self):
        output = ''
        for row in self._state:
            output += ' '.join(map(lambda x: '-' if x is None else x.serialize(), row))
            output += '\n'
        return output

    def __copy__(self):
        return Board(self._size.copy(), self._dictionary, copy.deepcopy(self._state))

    @property
    def size(self) -> Size:
        return self._size

    def is_empty(self) -> bool:
        """Returns whether or not there are no letter tiles on the board."""
        for position in BoardIterator(self._size):
            if self.get_tile(position) != '':
                return False
        return True

    def copy_and_apply_placements(self, placements: list[Placement]) -> Board:
        new_board = copy.copy(self)
        for placement in placements:
            new_board.set_tile(placement)
        return new_board

    def load_state(self, filepath: str):
        self._state = []
        with open(filepath, 'r') as file:
            for line in file.readlines():
                if line == '':
                    continue
                row: list[Optional[Letter]] = []
                for letter in line.strip().split(' '):
                    if letter == '-':
                        row.append(None)
                    elif letter.isupper():
                        row.append(Letter(letter))
                    elif letter.islower():
                        row.append(Letter(letter, True))
                    else:
                        raise ValueError(f'Invalid input letter: {letter}')
                if len(row) != self._size.num_cols:
                    raise ValueError(f'Expected {self._size.num_cols} columns, got {len(row)}')
                self._state.append(row)
            if len(self._state) != self._size.num_rows:
                raise ValueError(f'Expected {self._size.num_rows} rows, got {len(self._state)}')
        print(f'Successfully loaded {filepath}')

    def get_tile(self, position: Position) -> str:
        tile = self._state[position.row][position.col]
        if tile is None:
            return ''
        return tile.val

    def get_tile_checked(self, position: Position) -> Union[None, str]:
        """Checks if the tile is within bounds, returning None if not. Otherwise returns the tile."""
        if self._size.is_within_bounds(position):
            return self.get_tile(position)
        return None

    def get_letter(self, position: Position) -> Optional[Letter]:
        return self._state[position.row][position.col]

    def get_letter_checked(self, position: Position) -> Optional[Letter]:
        """Checks if the tile is within bounds or is populated, returning None if not. Otherwise returns the Letter."""
        if self._size.is_within_bounds(position):
            return self.get_letter(position)
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

        This is EXCLUSIVE of the given position. i.e. The returned string starts from the
        adjacent tile.
        """
        output = ''
        curr_position = position.move(direction)
        while True:
            curr_tile = self.get_tile_checked(curr_position)
            if curr_tile is None or curr_tile == '':
                break
            output += curr_tile
            curr_position = curr_position.move(direction)
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

    def is_state_valid(self) -> tuple[bool, list[str]]:
        # Check that all tiles are next to at least one other tile.
        for position in BoardIterator(self._size):
            if self.is_tile_filled(position) and self.are_adjacent_tiles_empty(position):
                return (False, [])
        chunks = []
        # Check rows.
        for row in self._state:
            chunks.extend(get_chunks(row))
        # Check columns.
        for col_num in range(self._size.num_cols):
            chunks.extend(get_chunks(self.get_column(col_num)))

        invalid_words = list(filter(lambda x: not self._dictionary.is_word(x), chunks))
        if len(invalid_words) > 0:
            return (False, invalid_words)
        return (True, [])

    def get_first_tile_positions(self) -> list[Position]:
        """The possible tiles that a letter can be placed to start the turn.

        This assumes a non-empty board.
        Returns a list of all empty tile positions that are next to non-empty tile positions.
        """
        positions = []
        for position in BoardIterator(self._size):
            if self.is_tile_empty(position) and self.is_any_adjacent_tile_filled(position):
                positions.append(position)
        return positions

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
                    word += placement.letter.val
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
                    word += placement.letter.val
                else:
                    word += tile
            return (word, Range(start, end))
        raise RuntimeError(f'Invalid shape: {shape}')

    def get_column(self, index) -> list[Optional[Letter]]:
        col = []
        for row in self._state:
            col.append(row[index])
        return col

    def save(self, filepath: str):
        with open(filepath, 'w') as file:
            file.write(str(self))
        print(f'Wrote {filepath}')

    def get_diff(self, other: Board) -> str:
        if self._size != other.size:
            raise ValueError(f'Cannot print diff of different sized boards.')
        output = ''
        for position in BoardIterator(self._size):
            letter = self.get_letter(position)
            tile = '-' if letter is None else letter.serialize()
            other_letter = other.get_letter(position)
            other_tile = '-' if other_letter is None else other_letter.serialize()
            if tile != other_tile:
                output += f'{RED}{tile}{ENDC} '
            elif tile.islower():
                output += f'{CYAN}{tile} {ENDC}'
            else:
                output += f'{tile} '
            if position.col == (self._size.num_cols - 1):
                output += '\n'
        return output
