from __future__ import annotations
from placement import Placement


class Placements:
    """Simple wrapper for a sorted list of placements."""

    def __init__(self, placements: list[Placement]):
        self._placements = sorted(placements)

    @classmethod
    def from_strings(cls, strings: list[str]) -> Placements:
        """Assumes each string element in the list is a stringified placement."""
        placements: list[Placement] = []
        for string in strings:
            placements.append(Placement.from_string(string))
        return cls(placements)

    def __hash__(self):
        value = ""
        for placement in self._placements:
            value += str(placement.position.index) + placement.letter.serialize()
        return hash(value)

    def __eq__(self, other: object):
        if not isinstance(other, Placements):
            return NotImplemented
        return self._placements == other.placements

    def __str__(self):
        return f'{self._placements}'

    @property
    def placements(self) -> list[Placement]:
        return self._placements
