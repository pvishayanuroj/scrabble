from __future__ import annotations
import copy
from placement import Placement
from typing import List

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
