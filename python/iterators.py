from enums import Direction
from letter import Letter
from position import Position
from range import Range
from size import Size


class BoardIterator:
    """Iterator to return positions on a board going from left to right, top to bottom."""

    def __init__(self, size: Size) -> None:
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


class NextLetterIterator:
    """Iterator that returns a tuple of the Nth letter and the remaining letters after the Nth letter.

    If there are duplicate letters in the given list, only a single of
    the duplicates is returned in the letter portion of the tuple. The
    remaining letters will contain the duplicates.

    e.g. Given 'CATTO', this yields four iterations:
    ('C', 'ATTO')
    ('A', 'CTTO')
    ('T', 'CATO')
    ('O', 'CATT')
    """

    def __init__(self, letters: list[Letter]) -> None:
        self._letters = letters
        seen = set()
        self._unique_letters: list[Letter] = []
        for letter in letters:
            if letter.val not in seen:
                self._unique_letters.append(letter)
                seen.add(letter.val)
        self._index = 0

    def  __iter__(self):
        return self

    def __next__(self) -> tuple[Letter, list[Letter]]:
        if self._index == len(self._unique_letters):
            raise StopIteration

        curr_letter = self._unique_letters[self._index]
        next_letters = []
        first_occurrence_found = False
        # Remove the *first occurrence* of the letter being returned.
        for letter in self._letters:
            if curr_letter.val == letter.val and not first_occurrence_found:
                first_occurrence_found = True
            else:
                next_letters.append(letter)

        element = (curr_letter, next_letters)
        self._index += 1
        return element


class WildcardIterator:
    """Iterator that returns a list of letters based on the number of wildcards.

    For a two-wildcard iterator, this yields:
    (A, A)
    (A, B)
    (A, C)
    ...
    (A, Z)
    (B, A)
    (B, B)
    (B, C)
    ...
    (Z, X)
    (Z, Y)
    (Z, Z)

    Zero wildcards is a special case that yields a single iteration,
    with an empty list.
    """

    def __init__(self, num_wildcards: int) -> None:
        if num_wildcards < 0:
            raise ValueError('Cannot initialize WildcardIterator with a value less than 0.')
        self._num_wildcards = num_wildcards
        self._curr_letters = ['A'] *  num_wildcards
        # Indicates whether a wildcard flipped from Z back to A.
        self._did_flip = [False] * num_wildcards
        self._last_index = num_wildcards - 1
        self._signal_stop_iteration = False

    def __iter__(self):
        return self

    def __next__(self) -> list[Letter]:
        if self._signal_stop_iteration:
            raise StopIteration

        if self._num_wildcards == 0:
            self._signal_stop_iteration = True
            return []

        output = list(map(lambda x: Letter(x, True), self._curr_letters))

        if all(map(lambda x: x == 'Z', self._curr_letters)):
            self._signal_stop_iteration = True
            return output

        next_letter = WildcardIterator.next_letter(self._curr_letters[self._last_index])
        self._curr_letters[self._last_index] = next_letter
        if next_letter == 'A':
            self._did_flip[self._last_index] = True
        for index, curr_letter in enumerate(reversed(self._curr_letters)):
            if index == 0:
                continue
            actual_index = self._last_index - index
            if self._did_flip[actual_index + 1]:
                next_letter = WildcardIterator.next_letter(curr_letter)
                self._curr_letters[actual_index] = next_letter
                if next_letter == 'A':
                    self._did_flip[actual_index] = True
                self._did_flip[actual_index + 1] = False

        return output

    @staticmethod
    def next_letter(letter: str) -> str:
        if letter == 'Z':
            return 'A'
        return chr(ord(letter) + 1)


class ColIterator:
    """Iterator that returns positions up-to-down along a column for the given range."""

    def __init__(self, range_param: Range) -> None:
        if range_param.start.col != range_param.end.col:
            raise ValueError(f"Cannot initialize column iterator with different columns: {range_param.start.col} and {range_param.end.col}")
        self._curr = range_param.start
        self._end = range_param.end

    def __iter__(self):
        return self

    def __next__(self) -> Position:
        if self._curr.row > self._end.row:
            raise StopIteration
        element = self._curr
        self._curr = self._curr.move(Direction.DOWN)
        return element


class RowIterator:
    """Iterator that returns positions left-to-right along a row for the given range."""

    def __init__(self, range_param: Range) -> None:
        if range_param.start.row != range_param.end.row:
            raise ValueError(f"Cannot initialize row iterator with different rows: {range_param.start.row} and {range_param.end.row}")
        self._curr = range_param.start
        self._end = range_param.end

    def __iter__(self):
        return self

    def __next__(self) -> Position:
        if self._curr.col > self._end.col:
            raise StopIteration
        element = self._curr
        self._curr = self._curr.move(Direction.RIGHT)
        return element
