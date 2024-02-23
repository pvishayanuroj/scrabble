from typing import List
from position import Position
from size import Size


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


class NextLetter:

    def __init__(self, letter, next_letters: List[str]):
        self._letter = letter
        self._next_letters = next_letters

    @property
    def letter(self) -> str:
        return self._letter

    @property
    def next_letters(self) -> List[str]:
        return self._next_letters


class NextLetterIterator:

    def __init__(self, letters: List[str]):
        self._letters = letters
        seen = set()
        self._unique_letters = []
        for letter in letters:
            if letter not in seen:
                self._unique_letters.append(letter)
                seen.add(letter)
        self._index = 0

    def  __iter__(self):
        return self

    def __next__(self) -> NextLetter:
        if self._index == len(self._unique_letters):
            raise StopIteration
        next_letters = self._letters.copy()
        # Remove the *first occurrence* of the letter being returned.
        next_letters.remove(self._unique_letters[self._index])
        element = (self._unique_letters[self._index], next_letters)
        self._index += 1
        return element
