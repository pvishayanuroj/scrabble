from typing import List
import copy

from board import Board
from iterators import NextLetterIterator
from enums import Direction, Shape
from dictionary import Dictionary
from position import Position
from turns2 import Turn
from scoreboard import Scoreboard
from turns import Placement


def solve(board: Board, scoreboard: Scoreboard, dictionary: Dictionary, letters: List[str]) -> List[Turn]:
    if board.is_empty():
        next_positions = [scoreboard.get_star_position()]
    else:
        next_positions = board.get_first_tile_positions()
    turns = []
    for (letter, remaining_letters) in NextLetterIterator(letters):
        for position in next_positions:
            placement = Placement(position, letter)
            (horizontal_word, horizontal_start, horizontal_end) = board.get_word_from_placement(placement, Shape.HORIZONTAL)
            #print(f"{placement} {horizontal_word}")
            word_type = dictionary.check(horizontal_word)
            if word_type != None:
                placements = {placement.position: placement.letter}
                turn = Turn(placements, horizontal_start, horizontal_end, Shape.HORIZONTAL)
                if word_type.is_word:
                    turns.append(turn)
                if word_type.is_substring:
                    turns.extend(_expand(board, dictionary, remaining_letters, turn))
            (vertical_word, vertical_start, vertical_end) = board.get_word_from_placement(placement, Shape.VERTICAL)
            #print(f"{placement} {vertical_word}")
            word_type = dictionary.check(vertical_word)
            if word_type != None:
                placements = {placement.position: placement.letter}
                turn = Turn(placements, vertical_start, vertical_end, Shape.VERTICAL)
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
        left = board.get_next_empty_tile(turn.first_position, Direction.LEFT)
        right = board.get_next_empty_tile(turn.last_position, Direction.RIGHT)

        if left:
            #print(turn._placements)
            #print(f"2 left: {left} {letters} {left.col + 1} {turn.last_position.col} {left.row}")
            curr_word = select_row(board, turn, left.col + 1, turn.last_position.col, left.row)
            for (letter, remaining_letters) in NextLetterIterator(letters):

                (vertical_word, _, _) = board.get_word_from_placement(Placement(left, letter), Shape.VERTICAL)
                if len(vertical_word) > 1 and not dictionary.is_word(vertical_word):
                    continue

                word = letter + curr_word
                #print(f"2 LEFT: {word} {left}")
                word_type = dictionary.check(word)
                if word_type != None:
                    updated_turn = copy.copy(turn)
                    updated_turn.add_placement(Placement(left, letter))
                    updated_turn._first_position = left
                    if word_type.is_word:
                        turns.append(updated_turn)
                    if word_type.is_substring:
                        turns.extend(_expand(board, dictionary, remaining_letters, updated_turn))
        if right:
            curr_word = select_row(board, turn, turn.first_position.col, right.col - 1, right.row)
            for (letter, remaining_letters) in NextLetterIterator(letters):

                (vertical_word, _, _) = board.get_word_from_placement(Placement(right, letter), Shape.VERTICAL)
                if len(vertical_word) > 1 and not dictionary.is_word(vertical_word):
                    continue

                word = curr_word + letter
                #print(f"2 RIGHT: {word} {right}")
                word_type = dictionary.check(word)
                if word_type != None:
                    updated_turn = copy.copy(turn)
                    updated_turn.add_placement(Placement(right, letter))
                    updated_turn._last_position = right
                    if word_type.is_word:
                        turns.append(updated_turn)
                    if word_type.is_substring:
                        turns.extend(_expand(board, dictionary, remaining_letters, updated_turn))            
                    
    elif turn.shape == Shape.VERTICAL:
        up = board.get_next_empty_tile(turn.first_position, Direction.UP)
        down = board.get_next_empty_tile(turn.last_position, Direction.DOWN)

        if up:
            curr_word = select_col(board, turn, up.row + 1, turn.last_position.row, up.col)
            for (letter, remaining_letters) in NextLetterIterator(letters):

                (horizontal_word, _, _) = board.get_word_from_placement(Placement(up, letter), Shape.HORIZONTAL)
                if len(horizontal_word) > 1 and not dictionary.is_word(horizontal_word):
                    continue

                word = letter + curr_word
                word_type = dictionary.check(word)
                if word_type != None:
                    updated_turn = copy.copy(turn)
                    updated_turn.add_placement(Placement(up, letter))
                    updated_turn._first_position = up
                    if word_type.is_word:
                        turns.append(updated_turn)
                    if word_type.is_substring:
                        turns.extend(_expand(board, dictionary, remaining_letters, updated_turn))      
        if down:
            curr_word = select_col(board, turn, turn.first_position.row, down.row - 1, down.col)
            for (letter, remaining_letters) in NextLetterIterator(letters):

                (horizontal_word, _, _) = board.get_word_from_placement(Placement(down, letter), Shape.HORIZONTAL)
                if len(horizontal_word) > 1 and not dictionary.is_word(horizontal_word):
                    continue

                word = curr_word + letter
                # if letter == "O" and down == Position(12, 9) and len(turn._placements) == 1:
                #     print(f"{word}, {turn}")
                word_type = dictionary.check(word)
                if word_type != None:
                    updated_turn = copy.copy(turn) 
                    updated_turn.add_placement(Placement(down, letter))
                    updated_turn._last_position = down
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