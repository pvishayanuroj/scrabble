from __future__ import annotations
from board import Board
from constants import ENDC, RED
from scoreboard import Scoreboard
from turns import Turn
from typing import List


class Solution:
    def __init__(self, original_board: Board, turn: Turn, scoreboard: Scoreboard):
        self._original_board = original_board
        self._board = original_board.copy_and_apply_turn(turn)
        self._score = self._board.get_score(turn, scoreboard)

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
