import copy

from board import Board
from constants import ALPHABET
from dictionary import Dictionary
from enums import Shape
from iterators import ColIterator, NextLetterIterator, RowIterator
from letter import Letter
from placement import Placement
from player_tiles import PlayerTiles
from range import Range
from scoreboard import Scoreboard
from turns2 import Turn
from util import dedup_turns, timer


@timer
def solve(board: Board, scoreboard: Scoreboard, dictionary: Dictionary, tiles: PlayerTiles) -> list[Turn]:
    """A recursive solver.

    Given a list of player tiles and a board state, returns a list of
    valid and deduped solutions in the form of turns.
    """

    if tiles.num_wildcards == 1:
        turns = []
        for letter in ALPHABET:
            turns.extend(_initial_expand(board, scoreboard, dictionary, tiles.letters + [Letter(letter, True)]))
        print(f"Generated {len(turns)} initial solutions.")
        valid_turns = _filter_valid_turns(turns, board)
        deduped_turns = dedup_turns(valid_turns)
        print(f"Generated {len(turns)} initial solutions.")
        print(f"Validation resulted in {len(valid_turns)} solutions.")
        print(f"Deduping resulted in {len(deduped_turns)} solutions.")
        return deduped_turns
    else:
        turns = _initial_expand(board, scoreboard, dictionary, tiles.letters)
        valid_turns = _filter_valid_turns(turns, board)
        deduped_turns = dedup_turns(valid_turns)
        print(f"Generated {len(turns)} initial solutions.")
        print(f"Validation resulted in {len(valid_turns)} solutions.")
        print(f"Deduping resulted in {len(deduped_turns)} solutions.")
        return deduped_turns


@timer
def _initial_expand(board: Board, scoreboard: Scoreboard, dictionary: Dictionary, letters: list[Letter]) -> list[Turn]:
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


def _expand(board: Board, dictionary: Dictionary, letters: list[Letter], turn: Turn) -> list[Turn]:
    """The recursive helper method used for second and later tile placements in a turn.

    Assumes that the given turn has at least one placement.
    """
    turns = []

    # Base case.
    if len(letters) == 0:
        return turns

    shape = turn.shape

    # Attempt to add a new tile at the start of the current word.
    start_position = board.get_next_empty_tile(turn.range.start, shape.start_direction)
    if start_position:
        existing_word_start_position = start_position.move(shape.start_direction.reverse)
        existing_word_range = Range(existing_word_start_position, turn.range.end)
        existing_word = _form_word(board, turn, existing_word_range, shape)
        for (letter, remaining_letters) in NextLetterIterator(letters):
            placement = Placement(start_position, letter)

            # If the new letter touches other tiles in the opposite
            # shape, check that the "cross" word it forms is valid.
            (cross_word, _) = board.get_word_from_placement(placement, turn.shape.opposite)
            if len(cross_word) > 1 and not dictionary.is_word(cross_word):
                continue

            # Check if the new word formed by adding the letter is:
            # 1) A dictionary word. If so, store the turn.
            # 2) A substring. If so, keep recursing.
            new_word = letter.val + existing_word
            word_type = dictionary.check(new_word)
            if word_type != None:
                # Do not update the original reference, since this is
                # being used by all the branches.
                updated_turn = copy.copy(turn)
                updated_turn.add_placement(placement)
                updated_turn.update_range_start(start_position)
                if word_type.is_word:
                    turns.append(updated_turn)
                if word_type.is_substring:
                    turns.extend(_expand(board, dictionary, remaining_letters, updated_turn))

    # Attempt to add a new tile at the end of the current word.
    end_position = board.get_next_empty_tile(turn.range.end, shape.end_direction)
    if end_position:
        existing_word_end_position = end_position.move(shape.end_direction.reverse)
        existing_word_range = Range(turn.range.start, existing_word_end_position)
        existing_word = _form_word(board, turn, existing_word_range, shape)
        for (letter, remaining_letters) in NextLetterIterator(letters):
            placement = Placement(end_position, letter)

            # If the new letter touches other tiles in the opposite
            # shape, check that the "cross" word it forms is valid.
            (cross_word, _) = board.get_word_from_placement(placement, turn.shape.opposite)
            if len(cross_word) > 1 and not dictionary.is_word(cross_word):
                continue

            # Check if the new word formed by adding the letter is:
            # 1) A dictionary word. If so, store the turn.
            # 2) A substring. If so, keep recursing.
            new_word = existing_word + letter.val
            word_type = dictionary.check(new_word)
            if word_type != None:
                # Do not update the original reference, since this is
                # being used by all the branches.
                updated_turn = copy.copy(turn)
                updated_turn.add_placement(placement)
                updated_turn.update_range_end(end_position)
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


def _form_word(board: Board, turn: Turn, range: Range, shape: Shape) -> str:
    """Uses the board and the placements made to form the word made by selecting the range."""
    letters: list[str] = []
    if shape == Shape.HORIZONTAL:
        iterator = RowIterator(range)
    elif shape == Shape.VERTICAL:
        iterator = ColIterator(range)
    else:
        raise ValueError(f"Unsupported enum value: {shape}")
    for position in iterator:
        tile = board.get_tile(position)
        if tile == '':
            tile = turn.get_tile_unchecked(position)
        letters.append(tile)
    return ''.join(letters)
