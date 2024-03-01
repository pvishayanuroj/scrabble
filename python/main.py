from __future__ import annotations
import argparse
import datetime
import os
import re
from board import Board
from dictionary import Dictionary
from enums import MenuSelection
from scoreboard import Scoreboard
from solution import Solution
from turns import Turn, dedup_turns
from solver import solve, solve_first_turn
from typing import List, Union


GAME_FILE_PATTERN = r'^(\w+)_\d{8}_\d{6}\.txt$'
MAX_SOLUTIONS_TO_SHOW = 5

def main():
    parser = argparse.ArgumentParser(description="A command line word puzzle solver.")

    parser.add_argument("--dictionary", default="dictionaries/279k-dictionary.txt", help="Dictionary file path (default: %(default)s)")
    parser.add_argument("--omit", default="dictionaries/omit.txt", help="List of words to omit from dictionary (default: %(default)s)")
    parser.add_argument("--board", default="boards/official.txt", help="Board file path (default: %(default)s)")
    parser.add_argument("--points", default="points.txt", help="Points file path (default: %(default)s)")
    parser.add_argument("--games", default="games/", help="Games directory path (default: %(default)s)")

    args = parser.parse_args()

    selection = select_menu_option()
    if selection == MenuSelection.NEW_GAME:
        #player_tiles = get_player_tiles()
        player_tiles = [letter for letter in 'AGAEETQ']
        scoreboard = Scoreboard(args.board, args.points)
        dictionary = Dictionary(args.dictionary, args.omit)
        board = Board(scoreboard.size)
        solution_boards = solve_first_turn(dictionary, board, scoreboard, player_tiles)
        solutions = []
        turns = []
        for solution in solution_boards:
            turns.append(Turn(solution.get_placements_from_diff(board)))
        unique_turns = dedup_turns(turns)
        for turn in unique_turns:
            solutions.append(Solution(board, turn, scoreboard))
        solutions.sort(reverse=True)
        truncated_solutions = solutions[:MAX_SOLUTIONS_TO_SHOW]
        selected_solution = select_solution(truncated_solutions)
        if not selected_solution:
            return
        #selected_solution.save(generate_file_name(args.games, game_name))
    elif selection == MenuSelection.LOAD_GAME:
        game_names = get_games(args.games)
        game_name = select_game_name(game_names)
        game_file = get_latest_game_file(args.games, game_name)
        player_tiles = get_player_tiles()
        scoreboard = Scoreboard(args.board, args.points)
        dictionary = Dictionary(args.dictionary, args.omit)
        board = Board(scoreboard.size)
        board.load_state(game_file)
        solution_boards = solve(dictionary, board, player_tiles)
        solutions = []
        turns = []
        for solution in solution_boards:
            turns.append(Turn(solution.get_placements_from_diff(board)))
        unique_turns = dedup_turns(turns)
        for turn in unique_turns:
            solutions.append(Solution(board, turn, scoreboard))
        solutions.sort(reverse=True)
        truncated_solutions = solutions[:MAX_SOLUTIONS_TO_SHOW]
        selected_solution = select_solution(truncated_solutions)
        if not selected_solution:
            return
        selected_solution.save(generate_file_name(args.games, game_name))


def generate_file_name(directory_path: str, game_name: str) -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{game_name}_{timestamp}.txt"
    return os.path.join(directory_path, filename)


def select_menu_option() -> MenuSelection:
    print("")
    for index, option in enumerate(MenuSelection):
        print(f"{index + 1}) {option}")
    while True:
        try:
            user_input = input("\nMake a selection: ")
            value = int(user_input)
            return MenuSelection(value)
        except:
            print("Invalid input. Select a valid option.")


def get_games(directory_path: str) -> List[str]:
    games = set()
    for filename in os.listdir(directory_path):
        match = re.match(GAME_FILE_PATTERN, filename)
        if match:
            games.add(match.groups()[0])
    return sorted(list(games))


def select_game_name(game_names: List[str]) -> str:
    print("\nAvailable games:")
    for index, option in enumerate(game_names):
        print(f"{index + 1}) {option}")
    while True:
        try:
            user_input = input("\nMake a selection: ")
            value = int(user_input)
            return game_names[value - 1]
        except:
            print("Invalid input. Select a valid option.")


def get_latest_game_file(directory_path: str, game_name: str) -> str:
    files = []
    for filename in os.listdir(directory_path):
        match = re.match(GAME_FILE_PATTERN, filename)
        if match and match.groups()[0] == game_name:
            files.append(os.path.join(directory_path, filename))
    return sorted(files, reverse=True)[0]


def get_player_tiles() -> List[str]:
    pattern = r'^[a-zA-Z]+$'
    while True:
        user_input = input("\nEnter tiles: ")
        match = re.match(pattern, user_input)
        if match:
            tiles = [letter for letter in user_input.upper().strip()]
            output = '\nTiles: '
            for index, tile in enumerate(tiles):
                output += f"'{tile}'"
                if index != len(tiles) - 1:
                    output += ", "
            print(output)
            return tiles
        else:
            print("Invalid tile input")


def select_solution(solutions: List[Solution]) -> Union[Solution, None]:
    print(f"Generated {len(solutions)} solutions")
    for index, solution in enumerate(solutions):
        print(f"\n---------Solution {index + 1}-----------\n{solution}")
    while True:
        try:
            user_input = input("\nMake a selection: ")
            value = int(user_input)
            return solutions[value - 1]
        except KeyboardInterrupt:
            print("Exiting.")
            return None
        except:
            print("Invalid input. Select a valid option.")


# board = Board(scoreboard.get_size())
# board.load_state(STATE_PATH)

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

# if not board.is_state_valid(dictionary):
#     print("Invalid board state")

# is_valid = board.is_state_valid(dictionary)
# print(f"is board valid: {is_valid}")
#first_moves = board.get_first_tile_moves()
#print(first_moves)
#next_moves = board.get_next_tile_moves([Position(6, 6)])
#next_moves = board.get_next_tile_moves([Position(6, 6), Position(7, 6)])
#print(next_moves)
#print(board.get_chunk(Position(7, 7), Shape.VERTICAL))
#print(board.get_chunk(Position(7, 7), Shape.HORIZONTAL))

if __name__ == "__main__":
    main()
