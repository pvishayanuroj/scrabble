from __future__ import annotations
from board import Board
from constants import ENDC, RED
from scoreboard import Scoreboard
from turns2 import Turn


class Solution:
    def __init__(self, original_board: Board, turn: Turn, scoreboard: Scoreboard):
        self._original_board = original_board
        self._board = original_board.copy_and_apply_placements(turn.generate_placement_list())
        self._score = self._board.get_score2(turn, scoreboard)

    @property
    def score(self) -> int:
        return self._score

    def __lt__(self, other: Solution):
        return self.score < other.score

    def __str__(self):
        output = self._board.get_diff(self._original_board)
        output += f"\nScore: {RED}{self._score}{ENDC}"
        return output

    def save(self, filepath: str):
        self._board.save(filepath)
