import unittest
from position import Position
from turns import Placement, Turn


class TestTurns(unittest.TestCase):

    def test_placement_equality(self):
        self.assertEqual(Placement(Position(1, 1), 'A'), Placement(Position(1, 1), 'A'))
        self.assertEqual(Placement(Position(1, 2), 'A'), Placement(Position(1, 2), 'A'))
        self.assertEqual(Placement(Position(2, 2), 'A'), Placement(Position(2, 2), 'A'))

    def test_placement_inequality(self):
        self.assertNotEqual(Placement(Position(1, 1), 'A'), Placement(Position(2, 1), 'A'))
        self.assertNotEqual(Placement(Position(1, 1), 'A'), Placement(Position(1, 2), 'A'))
        self.assertNotEqual(Placement(Position(1, 1), 'A'), Placement(Position(2, 2), 'A'))
        self.assertNotEqual(Placement(Position(1, 1), 'A'), Placement(Position(1, 1), 'B'))

    def test_turn_equality(self):
        a = Turn([
            Placement(Position(1, 1), 'A'),
            Placement(Position(2, 2), 'B'),
            Placement(Position(3, 3), 'C'),
        ])
        b = Turn([
            Placement(Position(1, 1), 'A'),
            Placement(Position(2, 2), 'B'),
            Placement(Position(3, 3), 'C'),
        ])

        self.assertEqual(a, b)

    def test_turn_equality_by_sort(self):
        a = Turn([
            Placement(Position(1, 1), 'A'),
            Placement(Position(2, 2), 'B'),
            Placement(Position(3, 3), 'C'),
        ])
        b = Turn([
            Placement(Position(2, 2), 'B'),
            Placement(Position(1, 1), 'A'),
            Placement(Position(3, 3), 'C'),
        ])

        self.assertEqual(a, b)    

    def test_turn_inequality_by_letter(self):
        a = Turn([
            Placement(Position(1, 1), 'B'),
            Placement(Position(2, 2), 'B'),
            Placement(Position(3, 3), 'C'),
        ])
        b = Turn([
            Placement(Position(1, 1), 'A'),
            Placement(Position(2, 2), 'B'),
            Placement(Position(3, 3), 'C'),
        ])

        self.assertNotEqual(a, b) 

    def test_turn_inequality_by_length(self):
        a = Turn([
            Placement(Position(1, 1), 'A'),
            Placement(Position(2, 2), 'B'),
            Placement(Position(3, 3), 'C'),
        ])
        b = Turn([
            Placement(Position(1, 1), 'A'),
            Placement(Position(2, 2), 'B'),
        ])

        self.assertNotEqual(a, b)         


if __name__ == '__main__':
    unittest.main()
