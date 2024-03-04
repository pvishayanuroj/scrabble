import copy
import time
from board import Board
from dictionary import Dictionary
from enums import MoveStatus, SolutionState
from iterators import NextLetterIterator
from letter import Letter
from position import Position
from placement import Placement
from player_tiles import PlayerTiles
from scoreboard import Scoreboard


def solve_first_turn(dictionary: Dictionary, board: Board, scoreboard: Scoreboard, tiles: PlayerTiles) -> list[Board]:
    start_time = time.time()
    boards = solve_first_turn_helper(dictionary, board, scoreboard, tiles.letters, [], SolutionState.NO_LETTERS)
    board_generation_time = time.time()
    print(f"Generated {len(boards)} boards in {(board_generation_time - start_time):.2f} secs")
    valid_boards: list[Board] = list(filter(lambda x: x.is_state_valid()[0], boards))
    board_pruning_time = time.time()
    print(f"Prune down to {len(valid_boards)} boards in {(board_pruning_time - board_generation_time):.2f} secs")
    return valid_boards


def solve_first_turn_helper(dictionary: Dictionary, board: Board, scoreboard: Scoreboard, letters: list[Letter], moves: list[Position], solution_state: SolutionState):
    """Recursive solver method."""
    boards = []
    if solution_state == SolutionState.NO_LETTERS:
        next_moves = [scoreboard.get_star_position()]
        for (letter, next_letters) in NextLetterIterator(letters):
            for next_move in next_moves:
                new_board = copy.copy(board)
                new_board.set_tile(Placement(next_move, letter))
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
                (result, new_board) = board.is_move_valid(next_move, letter, next_solution_state)
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
                (result, new_board) = board.is_move_valid(next_move, letter, solution_state)
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


def solve(dictionary: Dictionary, board: Board, tiles: PlayerTiles) -> list[Board]:
    start_time = time.time()
    boards = solve_helper(dictionary, board, tiles.letters, [], SolutionState.NO_LETTERS)
    board_generation_time = time.time()
    print(f"Generated {len(boards)} boards in {(board_generation_time - start_time):.2f} secs")
    valid_boards: list[Board] = list(filter(lambda x: x.is_state_valid()[0], boards))
    board_pruning_time = time.time()
    print(f"Prune down to {len(valid_boards)} boards in {(board_pruning_time - board_generation_time):.2f} secs")
    return valid_boards


def solve_helper(dictionary: Dictionary, board: Board, letters: list[Letter], moves: list[Position], solution_state: SolutionState):
    """Recursive solver method."""
    boards = []
    # If no letters, place the first letter.
    if solution_state == SolutionState.NO_LETTERS:
        next_moves = board.get_first_tile_positions()
        for (letter, next_letters) in NextLetterIterator(letters):
            for next_move in next_moves:
                (result, new_board) = board.is_first_move_valid(next_move, letter)
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
    # If first letter placed, place the second letter.
    elif solution_state == SolutionState.FIRST_LETTER:
        next_moves = board.get_next_tile_moves(moves)
        for (letter, next_letters) in NextLetterIterator(letters):
            for next_move in next_moves:
                rows = set(map(lambda x: x.row, moves + [next_move]))
                cols = set(map(lambda x: x.col, moves + [next_move]))
                next_solution_state = SolutionState.VERTICAL
                if len(rows) == 1 and len(cols) != 1:
                    next_solution_state = SolutionState.HORIZONTAL
                (result, new_board) = board.is_move_valid(next_move, letter, next_solution_state)
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
                (result, new_board) = board.is_move_valid(next_move, letter, solution_state)
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
