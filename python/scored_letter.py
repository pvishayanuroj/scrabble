from __future__ import annotations
from letter import Letter
from position import Position
from placement import Placement


class ScoredLetter:
    """Letter used for scoring purposes."""
    def __init__(self, position: Position, letter: Letter, is_active: bool):
        """Init method.

        Parameters:
        position: Position of the letter to score.
        letter: The letter, including whether or not it is a wildcard.
        is_active: Whether the letter was placed on this turn (and hence should be scored).
        """
        self._position = position
        self._letter = letter
        self._is_active = is_active

    @property
    def position(self) -> Position:
        return self._position

    @property
    def letter(self) -> Letter:
        return self._letter

    @property
    def is_active(self) -> bool:
        return self._is_active

    @classmethod
    def from_placement(cls, placement: Placement) -> ScoredLetter:
        """Creates a scored letter from a placement. Implies is_active is true."""
        return cls(placement.position, placement.letter, True)
