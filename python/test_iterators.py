import unittest

from python.iterators import NextLetterIterator


class TestIterators(unittest.TestCase):

    def test_next_move_iterator(self):
        result = [(letter, next_letters) for (letter, next_letters) in NextLetterIterator(list('GETHUTO'))]

        expected = [
            ('G', ['E', 'T', 'H', 'U', 'T', 'O']),
            ('E', ['G', 'T', 'H', 'U', 'T', 'O']),
            ('T', ['G', 'E', 'H', 'U', 'T', 'O']),
            ('H', ['G', 'E', 'T', 'U', 'T', 'O']),
            ('U', ['G', 'E', 'T', 'H', 'T', 'O']),
            ('O', ['G', 'E', 'T', 'H', 'U', 'T']),
        ]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
