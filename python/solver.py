import copy
import time
from board import Board
from dictionary import Dictionary
from enums import MoveStatus, SolutionState
from iterators import NextLetterIterator
from position import Position
from scoreboard import Scoreboard
from typing import List


def solve(dictionary: Dictionary, board: Board, scoreboard: Scoreboard, letters: List[str]) -> List[Board]:
    start_time = time.time()
    boards = solve_helper(dictionary, board, letters, [], SolutionState.NO_LETTERS)
    board_generation_time = time.time()
    print(f"Generated {len(boards)} boards in {(board_generation_time - start_time):.2f} secs")
    valid_boards: List[Board] = list(filter(lambda x: x.is_state_valid(dictionary)[0], boards))
    board_pruning_time = time.time()
    print(f"Prune down to {len(valid_boards)} boards in {(board_pruning_time - board_generation_time):.2f} secs")

    # scored_boards = list(map(lambda x: (x, x.get_score_temp(board, scoreboard)), valid_boards))
    # scored_boards.sort(key=lambda x: x[1], reverse = True)
    # final_boards = scored_boards[:20]

    # for index, (final_board, score) in enumerate(final_boards):
    #     print(f"Board {index}, Score {score}")
    #     print(final_board.get_diff(board))
    #     final_board.save('/Users/pvishayanuroj/projects/scrabble/states/test5.txt')
    #     break
    return valid_boards

def solve_helper(dictionary: Dictionary, board: Board, letters: List[str], moves: List[Position], solution_state: SolutionState):
    """Recursive solver method."""
    boards = []
    if solution_state == SolutionState.NO_LETTERS:
        next_moves = board.get_first_tile_moves()
        for (letter, next_letters) in NextLetterIterator(letters):
            for next_move in next_moves:
                (result, new_board) = board.is_first_move_valid(dictionary, next_move, letter)
                if result == MoveStatus.COMPLETE_WORD:
                    boards.append(new_board)
                elif result == MoveStatus.PARTIAL_AND_COMPLETE_WORD:
                    boards.append(new_board)
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(next_move)
                    boards.extend(solve_helper(dictionary, new_board, next_letters, new_moves, SolutionState.FIRST_LETTER))
                elif result == MoveStatus.PARTIAL_WORD:
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(next_move)
                    boards.extend(solve_helper(dictionary, new_board, next_letters, new_moves, SolutionState.FIRST_LETTER))
    elif solution_state == SolutionState.FIRST_LETTER:
        next_moves = board.get_next_tile_moves(moves)
        for (letter, next_letters) in NextLetterIterator(letters):
            for next_move in next_moves:
                rows = set(map(lambda x: x.row, moves))
                cols = set(map(lambda x: x.col, moves))
                next_solution_state = SolutionState.VERTICAL
                if len(rows) == 1 and len(cols) != 1:
                    next_solution_state = SolutionState.HORIZONTAL
                (result, new_board) = board.is_move_valid(dictionary, next_move, letter, next_solution_state)
                if result == MoveStatus.COMPLETE_WORD:
                    boards.append(new_board)
                elif result == MoveStatus.PARTIAL_AND_COMPLETE_WORD:
                    boards.append(new_board)
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(next_move)
                    boards.extend(solve_helper(dictionary, new_board, next_letters, new_moves, next_solution_state))
                elif result == MoveStatus.PARTIAL_WORD:
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(next_move)
                    boards.extend(solve_helper(dictionary, new_board, next_letters, new_moves, next_solution_state))
    elif solution_state == SolutionState.HORIZONTAL or solution_state == SolutionState.VERTICAL:
        next_moves = board.get_next_tile_moves(moves)
        for (letter, next_letters) in NextLetterIterator(letters):
            for next_move in next_moves:
                (result, new_board) = board.is_move_valid(dictionary, next_move, letter, solution_state)
                if result == MoveStatus.COMPLETE_WORD:
                    boards.append(new_board)
                elif result == MoveStatus.PARTIAL_AND_COMPLETE_WORD:
                    boards.append(new_board)
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(next_move)
                    boards.extend(solve_helper(dictionary, new_board, next_letters, new_moves, solution_state))
                elif result == MoveStatus.PARTIAL_WORD:
                    new_moves = copy.deepcopy(moves)
                    new_moves.append(next_move)
                    boards.extend(solve_helper(dictionary, new_board, next_letters, new_moves, solution_state))
    return boards
