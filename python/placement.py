from __future__ import annotations
from position import Position


class Placement:
    """Describes a single move of a player's turn."""
    def __init__(self, position: Position, letter: str):
        self._position = position
        self._letter = letter

    def __copy__(self):
        return Placement(self._position, self._letter)

    def __lt__(self, other: Placement):
        return self.position < other.position

    def __eq__(self, other: Placement):
        return self.position == other.position and self.letter == other.letter

    def __str__(self):
        return f"{self._position}: {self._letter}"

    @property
    def position(self) -> Position:
        return self._position

    @property
    def letter(self) -> str:
        return self._letter