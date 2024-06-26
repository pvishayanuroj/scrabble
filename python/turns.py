from __future__ import annotations
from typing import Dict, Optional
from enums import Shape
from letter import Letter
from placement import Placement
from position import Position
from range import Range


class Turn:
    """Stores the tile placements made in a player's current turn."""

    def __init__(self, placements: Dict[Position, Letter], range: Range, shape: Shape):
        self._placements = placements
        self._range = range
        self._shape = shape

    def __eq__(self, other: object):
        if not isinstance(other, Turn):
            return NotImplemented
        if len(self._placements) != len(other._placements):
            return False
        for key, value in self._placements.items():
            if key not in other._placements or other._placements[key] != value:
                return False
        return True

    def __hash__(self):
        placements = self.generate_placement_list()
        placements.sort()
        value = ''
        for placement in placements:
            value += (str(placement.position.index)
                      + placement.letter.val
                      + '*' if placement.letter.is_wildcard else '')
        return hash(value)

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

    def get_tile_unchecked(self, position: Position) -> str:
        return self._placements[position].val

    def get_tile_checked(self, position: Position) -> Optional[Letter]:
        return self._placements.get(position)

    def serialize(self) -> str:
        placements = self.generate_placement_list()
        placements.sort()
        return '|'.join(map(lambda placement: placement.serialize(), placements))
