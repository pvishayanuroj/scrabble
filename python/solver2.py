import copy

from board import Board
from dictionary import Dictionary
from enums import Direction, Shape
from iterators import NextLetterIterator
from placement import Placement
from position import Position
from scoreboard import Scoreboard
from turns2 import Turn
from util import dedup_turns, timer


@timer
def solve(board: Board, scoreboard: Scoreboard, dictionary: Dictionary, letters: list[str]) -> list[Turn]:
    """A recursive solver.

    Given a list of player tiles and a board state, returns a list of
    valid and deduped solutions in the form of turns.
    """
    turns = _initial_expand(board, scoreboard, dictionary, letters)
    valid_turns = _filter_valid_turns(turns, board)
    deduped_turns = dedup_turns(valid_turns)
    print(f"Generated {len(turns)} initial solutions.")
    print(f"Validation resulted in {len(valid_turns)} solutions.")
    print(f"Deduping resulted in {len(deduped_turns)} solutions.")
    return deduped_turns


@timer
def _initial_expand(board: Board, scoreboard: Scoreboard, dictionary: Dictionary, letters: list[str]) -> list[Turn]:
    # For an empty board, any word must use the star tile.
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
                    # If this is a valid word, store this as a solution.
                    if word_type.is_word:
                        turns.append(turn)
                    # If this is a substring, recurse from this branch.
                    if word_type.is_substring:
                        turns.extend(_expand(board, dictionary, remaining_letters, turn))
    return turns

def _expand(board: Board, dictionary: Dictionary, letters: list[str], turn: Turn) -> list[Turn]:
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


def _is_turn_valid(turn: Turn, board: Board) -> bool:
    new_board = board.copy_and_apply_turn2(turn)
    return new_board.is_state_valid()[0]


@timer
def _filter_valid_turns(turns: list[Turn], board: Board) -> list[Turn]:
    return list(filter(lambda turn: _is_turn_valid(turn, board), turns))

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
