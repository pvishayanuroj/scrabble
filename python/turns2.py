from __future__ import annotations
from typing import Dict
from enums import Shape
from letter import Letter
from position import Position
from range import Range
from turns import Placement


class Turn:
    """Stores the tile placements made in a player's current turn."""

    def __init__(self, placements: Dict[Position, Letter], range: Range, shape: Shape):
        self._placements = placements
        self._range = range
        self._shape = shape

    def __eq__(self, other: Turn):
        if len(self._placements) != len(other._placements):
            return False
        for key, value in self._placements.items():
            if key not in other._placements or other._placements[key] != value:
                return False
        return True

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

    def generate_placement_list(self) -> list[Placement]:
        """Converts the dictionary entries into a list of placements, in random order.
        """
        return [
            Placement(position, letter) for position, letter in self._placements.items()
        ]

    def add_placement(self, placement: Placement):
        self._placements[placement.position] = placement.letter

    def update_range_start(self, start: Position):
        self._range = Range(start, self._range.end)

    def update_range_end(self, end: Position):
        self._range = Range(self._range.start, end)

    def get_tile_unchecked(self, position) -> str:
        return self._placements[position].val
