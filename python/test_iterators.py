import unittest

from constants import ALPHABET
from iterators import ColIterator, NextLetterIterator, RowIterator, WildcardIterator
from letter import Letter
from position import Position
from range import Range


class TestIterators(unittest.TestCase):

    def test_next_move_iterator(self):
        letters = [
            Letter("C"),
            Letter("A"),
            Letter("T"),
            Letter("T"),
            Letter("O"),
        ]
        result = [
            (letter, next_letters)
            for (letter, next_letters) in NextLetterIterator(letters)
        ]

        expected = [
            (Letter("C"), [Letter("A"), Letter("T"), Letter("T"), Letter("O")]),
            (Letter("A"), [Letter("C"), Letter("T"), Letter("T"), Letter("O")]),
            (Letter("T"), [Letter("C"), Letter("A"), Letter("T"), Letter("O")]),
            (Letter("O"), [Letter("C"), Letter("A"), Letter("T"), Letter("T")]),
        ]
        self.assertEqual(result, expected)

    def test_wildcard_iterator(self):
        result = [letters for letters in WildcardIterator(2)]

        expected = []
        for first_letter in ALPHABET:
            for second_letter in ALPHABET:
                expected.append(
                    [Letter(first_letter, True), Letter(second_letter, True)]
                )

        self.assertEqual(result, expected)

    def test_row_iterator(self):
        range = Range(Position(0, 1), Position(0, 3))

        result = [position for position in RowIterator(range)]

        expected = [
            Position(0, 1),
            Position(0, 2),
            Position(0, 3),
        ]
        self.assertEqual(result, expected)

    def test_col_iterator(self):
        range = Range(Position(1, 0), Position(3, 0))

        result = [position for position in ColIterator(range)]

        expected = [
            Position(1, 0),
            Position(2, 0),
            Position(3, 0),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
