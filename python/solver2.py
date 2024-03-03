from typing import List
import copy

from board import Board
from iterators import NextLetterIterator
from enums import Direction, Shape
from dictionary import Dictionary
from placement import Placement
from position import Position
from turns2 import Turn
from scoreboard import Scoreboard


def solve(board: Board, scoreboard: Scoreboard, dictionary: Dictionary, letters: List[str]) -> List[Turn]:
    if board.is_empty():
        next_positions = [scoreboard.get_star_position()]
    else:
        next_positions = board.get_first_tile_positions()

    # The first tile placement is a special case in that each tile can act as part of a vertical or
    turns = []
    for (letter, remaining_letters) in NextLetterIterator(letters):
        for position in next_positions:
            placement = Placement(position, letter)
            for shape in [Shape.HORIZONTAL, Shape.VERTICAL]:
                (word, range) = board.get_word_from_placement(placement, shape)
                word_type = dictionary.check(word)
                if word_type != None:
                    placements = {placement.position: placement.letter}
                    turn = Turn(placements, range, shape)
                    if word_type.is_word:
                        turns.append(turn)
                    if word_type.is_substring:
                        turns.extend(_expand(board, dictionary, remaining_letters, turn))
    return turns

def _expand(board: Board, dictionary: Dictionary, letters: List[str], turn: Turn) -> List[Turn]:
    turns = []

    # Base case.
    if len(letters) == 0:
        return turns

    if turn.shape == Shape.HORIZONTAL:
        left = board.get_next_empty_tile(turn.range.start, Direction.LEFT)
        right = board.get_next_empty_tile(turn.range.end, Direction.RIGHT)

        if left:
            curr_word = select_row(board, turn, left.col + 1, turn.range.end.col, left.row)
            for (letter, remaining_letters) in NextLetterIterator(letters):

                (vertical_word, _) = board.get_word_from_placement(Placement(left, letter), Shape.VERTICAL)
                if len(vertical_word) > 1 and not dictionary.is_word(vertical_word):
                    continue

                word = letter + curr_word
                word_type = dictionary.check(word)
                if word_type != None:
                    updated_turn = copy.copy(turn)
                    updated_turn.add_placement(Placement(left, letter))
                    updated_turn.update_range_start(left)
                    if word_type.is_word:
                        turns.append(updated_turn)
                    if word_type.is_substring:
                        turns.extend(_expand(board, dictionary, remaining_letters, updated_turn))
        if right:
            curr_word = select_row(board, turn, turn.range.start.col, right.col - 1, right.row)
            for (letter, remaining_letters) in NextLetterIterator(letters):

                (vertical_word, _) = board.get_word_from_placement(Placement(right, letter), Shape.VERTICAL)
                if len(vertical_word) > 1 and not dictionary.is_word(vertical_word):
                    continue

                word = curr_word + letter
                word_type = dictionary.check(word)
                if word_type != None:
                    updated_turn = copy.copy(turn)
                    updated_turn.add_placement(Placement(right, letter))
                    updated_turn.update_range_end(right)
                    if word_type.is_word:
                        turns.append(updated_turn)
                    if word_type.is_substring:
                        turns.extend(_expand(board, dictionary, remaining_letters, updated_turn))

    elif turn.shape == Shape.VERTICAL:
        up = board.get_next_empty_tile(turn.range.start, Direction.UP)
        down = board.get_next_empty_tile(turn.range.end, Direction.DOWN)

        if up:
            curr_word = select_col(board, turn, up.row + 1, turn.range.end.row, up.col)
            for (letter, remaining_letters) in NextLetterIterator(letters):

                (horizontal_word, _) = board.get_word_from_placement(Placement(up, letter), Shape.HORIZONTAL)
                if len(horizontal_word) > 1 and not dictionary.is_word(horizontal_word):
                    continue

                word = letter + curr_word
                word_type = dictionary.check(word)
                if word_type != None:
                    updated_turn = copy.copy(turn)
                    updated_turn.add_placement(Placement(up, letter))
                    updated_turn.update_range_start(up)
                    if word_type.is_word:
                        turns.append(updated_turn)
                    if word_type.is_substring:
                        turns.extend(_expand(board, dictionary, remaining_letters, updated_turn))
        if down:
            curr_word = select_col(board, turn, turn.range.start.row, down.row - 1, down.col)
            for (letter, remaining_letters) in NextLetterIterator(letters):

                (horizontal_word, _) = board.get_word_from_placement(Placement(down, letter), Shape.HORIZONTAL)
                if len(horizontal_word) > 1 and not dictionary.is_word(horizontal_word):
                    continue

                word = curr_word + letter
                word_type = dictionary.check(word)
                if word_type != None:
                    updated_turn = copy.copy(turn)
                    updated_turn.add_placement(Placement(down, letter))
                    updated_turn.update_range_end(down)
                    if word_type.is_word:
                        turns.append(updated_turn)
                    if word_type.is_substring:
                        turns.extend(_expand(board, dictionary, remaining_letters, updated_turn))
    return turns


def select_row(board: Board, turn: Turn, start: int, end: int, row: int) -> str:
    letters = []
    for col in range(start, end + 1):
        position = Position(row, col)
        tile = board.get_tile(position)
        if tile == '':
            tile = turn.get_tile_unchecked(position)
        letters.append(tile)
    return ''.join(letters)

def select_col(board: Board, turn: Turn, start: int, end: int, col: int) -> str:
    letters = []
    for row in range(start, end + 1):
        position = Position(row, col)
        tile = board.get_tile(position)
        if tile == '':
            tile = turn.get_tile_unchecked(position)
        letters.append(tile)
    return ''.join(letters)
