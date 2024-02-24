from __future__ import annotations
import copy
import os
import time
from board import Board
from enums import Shape
from position import Position
from dictionary import Dictionary
from iterators import NextLetterIterator
from scoreboard import Scoreboard
from typing import List


def read_directory_files(path):
    files = set()
    for filename in os.listdir(path):
        files.add(filename)
    return files

def get_shape(previous_move: Position, current_move: Position) -> Shape:
    if previous_move.col == current_move.col:
        return Shape.VERTICAL
    elif previous_move.row == current_move.row:
        return Shape.HORIZONTAL
    else:
        raise ValueError(f"Cannot get shape of previous move {previous_move} and current move {current_move}")

#DICTIONARIES_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries'
#DICTIONARY_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries/10k-dictionary.txt'
#DICTIONARY_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries/178k-dictionary.txt'
DICTIONARY_PATH = '/Users/pvishayanuroj/projects/scrabble/dictionaries/279k-dictionary.txt'
BOARD_PATH = '/Users/pvishayanuroj/projects/scrabble/boards/official.txt'
#STATE_PATH = '/Users/pvishayanuroj/projects/scrabble/states/test.txt'
#STATE_PATH = '/Users/pvishayanuroj/projects/scrabble/states/test2.txt'
STATE_PATH = '/Users/pvishayanuroj/projects/scrabble/states/test3.txt'
#STATE_PATH = '/Users/pvishayanuroj/projects/scrabble/states/test4.txt'
POINTS_PATH = '/Users/pvishayanuroj/projects/scrabble/points.txt'

scoreboard = Scoreboard(BOARD_PATH, POINTS_PATH)

board = Board(scoreboard.get_size())
board.load_state(STATE_PATH)

# turns = [
#     Turn(Position(11, 7), 'O'),
#     Turn(Position(12, 7), 'G'),
#     Turn(Position(13, 7), 'U'),
#     Turn(Position(14, 7), 'E'),
# ]
# solution = Solution(turns)
# for turn in turns:
#     board.set_tile(turn.position, turn.letter)
# print(board)
# print(board.get_score(solution, scoreboard))

#files = read_directory_files(PATH)
dictionary = Dictionary()
dictionary.load(DICTIONARY_PATH)

if not board.is_state_valid(dictionary):
    print("Invalid board state")

# is_valid = board.is_state_valid(dictionary)
# print(f"is board valid: {is_valid}")
#first_moves = board.get_first_tile_moves()
#print(first_moves)
#next_moves = board.get_next_tile_moves([Position(6, 6)])
#next_moves = board.get_next_tile_moves([Position(6, 6), Position(7, 6)])
#print(next_moves)
#print(board.get_chunk(Position(7, 7), Shape.VERTICAL))
#print(board.get_chunk(Position(7, 7), Shape.HORIZONTAL))

def solver(dictionary: Dictionary, board: Board, letters: List[str]):
    start_time = time.time()
    boards = solver_helper(dictionary, board, letters, [])
    board_generation_time = time.time()
    print(f"Generated {len(boards)} boards in {(board_generation_time - start_time):.2f} secs")
    valid_boards: List[Board] = list(filter(lambda x: x.is_state_valid(dictionary), boards))
    board_pruning_time = time.time()
    print(f"Prune down to {len(valid_boards)} boards in {(board_pruning_time - board_generation_time):.2f} secs")

    scored_boards = list(map(lambda x: (x, x.get_score_temp(board, scoreboard)), valid_boards))
    scored_boards.sort(key=lambda x: x[1], reverse = True)
    final_boards = scored_boards[:20]

    for index, (final_board, score) in enumerate(final_boards):
        print(f"Board {index}, Score {score}")
        print(final_board.get_diff(board))

def solver_helper(dictionary: Dictionary, board: Board, letters: List[str], moves: List[Position]):
    """Recursive solver method."""
    #print("------ SOVLER HELPER CALL -----")
    #print(letters)
    #print(moves)
    #print(board)
    boards = []
    if len(moves) == 0:
        next_moves = board.get_first_tile_moves()
        for (letter, next_letters) in NextLetterIterator(letters):
            #for letter in letters:
            #next_letters = list(filter(lambda x: x != letter, letters))
            for next_move in next_moves:
                maybe_board = board.is_first_move_valid(dictionary, next_move, letter)
                if maybe_board:
                    boards.append(maybe_board)
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(next_move)
                    boards.extend(solver_helper(dictionary, maybe_board, next_letters, new_moves))
    # elif len(moves) == 1:
    #     previous_move = moves[0]
    #     next_moves = board.get_next_tile_moves(moves)
    #     for letter in letters:
    #         new_letters = list(filter(lambda x: x != letter, letters))
    #         for next_move in next_moves:
    #             shape = get_shape(previous_move, next_move)
    else:
        next_moves = board.get_next_tile_moves(moves)
        for (letter, next_letters) in NextLetterIterator(letters):
            #for letter in letters:
            #next_letters = list(filter(lambda x: x != letter, letters))
            for next_move in next_moves:
                maybe_board = board.is_first_move_valid(dictionary, next_move, letter)
                if maybe_board:
                    boards.append(maybe_board)
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(next_move)
                    boards.extend(solver_helper(dictionary, maybe_board, next_letters, new_moves))

    # else:
    #     next_moves = board.get_next_tile_moves(moves)
    #     for letter in letters:
    #         new_letters = list(filter(lambda x: x != letter, letters))
    #         for next_move in next_moves:
    #             new_board = board.copy()
    #             boards.append(new_board)
    #             new_board.set_tile(next_move, letter)
    #             new_moves = copy.deepcopy(moves)
    #             new_moves.append(next_move)
    #             boards.extend(solver_helper(dictionary, new_board, new_letters, new_moves))
    return boards

letters = 'GETHUTO'
#letters = 'NRALEFI'
letters = [letter for letter in letters]

solver(dictionary, board, letters)
