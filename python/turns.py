from __future__ import annotations
import copy
from enums import Shape, SolutionState
from typing import List
from position import Position


class Turn:
    def __init__(self, position: Position, letter: str):
        self._position = position
        self._letter = letter

    def __copy__(self):
        return Turn(self._position, self._letter)

    def __lt__(self, other: Turn):
        return self.position < other.position

    def __eq__(self, other: Turn):
        return self.position == other.position and self.letter == other.letter

    @property
    def position(self) -> Position:
        return self._position

    @property
    def letter(self) -> str:
        return self._letter


class Turns:
    def __init__(self, turns):
        self._turns = turns
        self._state = SolutionState.NO_LETTERS

    def __copy__(self):
        return Turns(copy.deepcopy(self._turns))

    @property
    def turns(self) -> List[Turn]:
        return self._turns

    def len(self) -> int:
        return len(self._turns)

    def add(self, turn: Turn):
        self._turns.append(turn)

    def get_shape(self) -> Shape:
        rows = set(map(lambda x: x.position.row, self._turns))
        cols = set(map(lambda x: x.position.col, self._turns))
        if len(rows) == 1 and len(cols) != 1:
            return Shape.HORIZONTAL
        if len(rows) != 1 and len(cols) == 1:
            return Shape.VERTICAL
        raise ValueError(f"Cannot get shape. Distinct rows: {len(rows)}, distinct cols {len(cols)}")
