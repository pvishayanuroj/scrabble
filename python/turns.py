from __future__ import annotations
import copy
from enums import Shape, SolutionState
from typing import List
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


class Turn:
    """Wrapper for holding a list of letter placements."""

    def __init__(self, placements: List[Placement]):
        self._placements = copy.deepcopy(placements)
        self._placements.sort()

    def __eq__(self, other: Turn):
        return self.placements == other.placements

    def __str__(self):
        output = 'Turn:\n'
        for placement in self._placements:
            output += f"{placement}\n"
        return output

    @property
    def placements(self) -> List[Placement]:
        return self._placements
    
    @property
    def len(self) -> int:
        return len(self._placements)


def dedup_turns(turns: List[Turn]) -> List[Turn]:
    unique_turns = []
    for turn in turns:
        if turn not in unique_turns:
            unique_turns.append(turn)
    return unique_turns
