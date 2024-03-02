from enums import Shape
from position import Position
from turns import Placement


class Turn:

    def __init__(self, placements, first_position: Position, last_position: Position, shape: Shape):
        self._placements = placements
        self._first_position = first_position
        self._last_position = last_position
        self._shape = shape

    def add_placement(self, placement: Placement):
        self._placements[placement.position] = placement.letter
    
    def __copy__(self):
        return Turn(self._placements.copy(), self._first_position, self._last_position, self._shape)

    def __str__(self):
        return f"{self._shape}\nFirst: {self._first_position}\nLast: {self._last_position}\n{self._placements}, "

    @property
    def first_position(self) -> Position:
        return self._first_position

    @property
    def last_position(self) -> Position:
        return self._last_position

    @property
    def shape(self) -> Shape:
        return self._shape
    
    def get_tile_unchecked(self, position) -> str:
        return self._placements[position]