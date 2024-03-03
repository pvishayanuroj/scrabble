from enums import Shape
from position import Position
from range import Range
from turns import Placement


class Turn:

    def __init__(self, placements, range: Range, shape: Shape):
        self._placements = placements
        self._range = range
        self._shape = shape

    def add_placement(self, placement: Placement):
        self._placements[placement.position] = placement.letter

    def __copy__(self):
        return Turn(self._placements.copy(), self._range, self._shape)

    def __str__(self):
        return f"{self._shape}\n{self._range}\n{self._placements}"

    @property
    def range(self) -> Range:
        return self._range

    @property
    def shape(self) -> Shape:
        return self._shape

    # Returns a list of placements in this turn, in random order.
    @property
    def placements(self) -> list[Placement]:
        return [
            Placement(position, letter) for position, letter in self._placements.items()
        ]

    def get_tile_unchecked(self, position) -> str:
        return self._placements[position]

    def update_range_start(self, start: Position):
        self._range = Range(start, self._range.end)

    def update_range_end(self, end: Position):
        self._range = Range(self._range.start, end)
