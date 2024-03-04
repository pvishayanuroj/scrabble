from __future__ import annotations
from letter import Letter
from position import Position


class Placement:
    """Describes a single move of a player's turn."""
    def __init__(self, position: Position, letter: Letter):
        self._position = position
        self._letter = letter

    def __copy__(self):
        return Placement(self._position, self._letter)

    def __lt__(self, other: Placement):
        return self.position < other.position

    def __eq__(self, other: object):
        if not isinstance(other, Placement):
            return NotImplemented
        return self.position == other.position and self.letter == other.letter

    def __str__(self):
        return f"{self._position}: {self._letter.val}"

    @property
    def position(self) -> Position:
        return self._position

    @property
    def letter(self) -> Letter:
        return self._letter
