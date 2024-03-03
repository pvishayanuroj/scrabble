import unittest

from iterators import ColIterator, NextLetterIterator, RowIterator
from position import Position
from range import Range


class TestIterators(unittest.TestCase):

    def test_next_move_iterator(self):
        result = [
            (letter, next_letters)
            for (letter, next_letters) in NextLetterIterator(list("GETHUTO"))
        ]

        expected = [
            ("G", ["E", "T", "H", "U", "T", "O"]),
            ("E", ["G", "T", "H", "U", "T", "O"]),
            ("T", ["G", "E", "H", "U", "T", "O"]),
            ("H", ["G", "E", "T", "U", "T", "O"]),
            ("U", ["G", "E", "T", "H", "T", "O"]),
            ("O", ["G", "E", "T", "H", "U", "T"]),
        ]
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
