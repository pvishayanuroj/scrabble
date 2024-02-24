from typing import List
from position import Position

class Turn:
    def __init__(self, position: Position, letter: str):
        self._position = position
        self._letter = letter

    @property
    def position(self) -> Position:
        return self._position

    @property
    def letter(self) -> str:
        return self._letter


class Solution:
    def __init__(self, turns: List[Turn]):
        self._turns = turns

    @property
    def turns(self) -> List[Turn]:
        return self._turns
