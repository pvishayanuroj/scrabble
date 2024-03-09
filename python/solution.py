from __future__ import annotations
from board import Board
from constants import ENDC, RED
from scoreboard import Scoreboard
from scorer import calculate_score
from turns import Turn


class Solution:
    def __init__(self, original_board: Board, scoreboard: Scoreboard, turn: Turn):
        self._original_board = original_board
        self._turn = turn
        self._score = calculate_score(original_board, scoreboard, turn)

    @property
    def score(self) -> int:
        return self._score

    @property
    def turn(self) -> Turn:
        return self._turn

    def __lt__(self, other: Solution):
        return self.score < other.score

    def __str__(self):
        updated_board = self._original_board.copy_and_apply_placements(self._turn.generate_placement_list())
        output = updated_board.get_diff(self._original_board)
        output += f"\nScore: {RED}{self._score}{ENDC}"
        return output

    def serialize(self) -> str:
        return f'{self._score}||{self._turn.serialize()}'

    def save(self, filepath: str):
        updated_board = self._original_board.copy_and_apply_placements(self._turn.generate_placement_list())
        updated_board.save(filepath)
