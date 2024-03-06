from __future__ import annotations
import argparse
import datetime
import os
import re
import time
from board import Board
from constants import GAME_FILE_PATTERN, MAX_SOLUTIONS_TO_SHOW, TEST_FILE_PATTERN
from dictionary import Dictionary
from enums import MenuSelection
from player_tiles import PlayerTiles
from scoreboard import Scoreboard
from solution import Solution
from solution2 import Solution as Solution2
from turns import Turn, dedup_turns
from turns2 import Turn as Turn2
from typing import Optional
from solver import solve, solve_first_turn
from solver2 import solve as solve2


def main():
    parser = argparse.ArgumentParser(description="A command line word puzzle solver.")

    parser.add_argument("--dictionary", default="dictionaries/279k-dictionary.txt", help="Dictionary file path (default: %(default)s)")
    parser.add_argument("--omit", default="dictionaries/omit.txt", help="List of words to omit from dictionary (default: %(default)s)")
    parser.add_argument("--board", default="boards/official.txt", help="Board file path (default: %(default)s)")
    parser.add_argument("--points", default="points.txt", help="Points file path (default: %(default)s)")
    parser.add_argument("--games", default="games/", help="Games directory path (default: %(default)s)")
    parser.add_argument("--tests", default="testcases/", help="Test case directory path (default: %(default)s)")

    args = parser.parse_args()

    selection = select_menu_option()
    #selection = MenuSelection.LOAD_GAME
    if selection == MenuSelection.NEW_GAME:
        player_tiles = get_player_tiles()
        if player_tiles is None:
            return
        scoreboard = Scoreboard(args.board, args.points)
        dictionary = Dictionary(args.dictionary, args.omit)
        board = Board(scoreboard.size, dictionary)

        new_unique_turns = solve2(board, scoreboard, dictionary, player_tiles)
        new_solutions = []
        for turn in new_unique_turns:
            new_solutions.append(Solution2(board, turn, scoreboard))
        new_solutions.sort(reverse=True)
        for index, solution in enumerate(new_solutions[:MAX_SOLUTIONS_TO_SHOW]):
            print(f"\n---------Solution {index + 1}-----------\n{solution}")

        # print("OLD RUN")
        # start_time = time.time()
        # solution_boards = solve_first_turn(dictionary, board, scoreboard, player_tiles)
        # solutions = []
        # turns = []
        # for solution in solution_boards:
        #     turns.append(Turn(solution.get_placements_from_diff(board)))
        # dedup_start_time = time.time()
        # unique_turns = dedup_turns(turns)
        # dedup_end_time = time.time()
        # print(f"DEDUP to {len(unique_turns)} solutions in {(dedup_end_time - dedup_start_time):.2f} secs.")
        # print(f"TOTAL: {(time.time() - start_time):.2f} secs")
        # for turn in unique_turns:
        #     solutions.append(Solution(board, turn, scoreboard))
        # solutions.sort(reverse=True)
        # for index, solution in enumerate(solutions[:MAX_SOLUTIONS_TO_SHOW]):
        #     print(f"\n---------Solution {index + 1}-----------\n{solution}")

        # compare_solutions(board, scoreboard, unique_turns, new_unique_turns)

        # solutions.sort(reverse=True)
        # truncated_solutions = solutions[:MAX_SOLUTIONS_TO_SHOW]
        # selected_solution = select_solution(truncated_solutions)
        # if not selected_solution:
        #     return
        # game_name = input("Enter a game name: ")
        # selected_solution.save(generate_file_name(args.games, game_name))
    elif selection == MenuSelection.LOAD_GAME:
        game_names = get_games(args.games)
        game_name = select_option('Available games:', game_names)
        if game_name is None:
            return
        game_file = get_latest_game_file(args.games, game_name)
        player_tiles = get_player_tiles()
        if player_tiles is None:
            return
        scoreboard = Scoreboard(args.board, args.points)
        dictionary = Dictionary(args.dictionary, args.omit)
        board = Board(scoreboard.size, dictionary)
        board.load_state(game_file)

        new_unique_turns = solve2(board, scoreboard, dictionary, player_tiles)
        new_solutions = []
        for turn in new_unique_turns:
            new_solutions.append(Solution2(board, turn, scoreboard))
        new_solutions.sort(reverse=True)
        for index, solution in enumerate(new_solutions[:MAX_SOLUTIONS_TO_SHOW]):
            print(f"\n---------Solution {index + 1}-----------\n{solution}")

        print("OLD RUN")
        start_time = time.time()
        solution_boards = solve(dictionary, board, player_tiles)
        solutions = []
        turns = []
        for solution in solution_boards:
            turns.append(Turn(solution.get_placements_from_diff(board)))
        dedup_start_time = time.time()
        unique_turns = dedup_turns(turns)
        dedup_end_time = time.time()
        print(f"DEDUP to {len(unique_turns)} solutions in {(dedup_end_time - dedup_start_time):.2f} secs.")
        print(f"TOTAL: {(time.time() - start_time):.2f} secs")
        for turn in unique_turns:
            solutions.append(Solution(board, turn, scoreboard))
        solutions.sort(reverse=True)
        for index, solution in enumerate(solutions[:MAX_SOLUTIONS_TO_SHOW]):
            print(f"\n---------Solution {index + 1}-----------\n{solution}")

        # compare_solutions(board, scoreboard, unique_turns, new_unique_turns)

        # truncated_solutions = solutions[:MAX_SOLUTIONS_TO_SHOW]
        # selected_solution = select_solution(truncated_solutions)
        # if not selected_solution:
        #     return
        # selected_solution.save(generate_file_name(args.games, game_name))
    elif selection == MenuSelection.RUN_TEST:
        test_names = get_tests(args.tests)
        test_name = select_option('Test cases:', test_names)
        if test_name is None:
            return
        state_file = os.path.join(args.tests, f'{test_name}_state.txt')
        player_tiles_file = os.path.join(args.tests, f'{test_name}_tiles.txt')
        scoreboard = Scoreboard(args.board, args.points)
        dictionary = Dictionary(args.dictionary)
        board = Board(scoreboard.size, dictionary)
        board.load_state(state_file)
        player_tiles = read_player_tiles_file(player_tiles_file)

        turns = solve2(board, scoreboard, dictionary, player_tiles)
        solutions = []
        for turn in turns:
            solutions.append(Solution2(board, turn, scoreboard))
        solutions.sort(reverse=True)
        for index, solution in enumerate(solutions[:MAX_SOLUTIONS_TO_SHOW]):
            print(f"\n---------Solution {index + 1}-----------\n{solution}")

        # print("OLD RUN")
        # start_time = time.time()
        # solution_boards = solve(dictionary, board, player_tiles)
        # solutions = []
        # old_run_turns = []
        # for solution in solution_boards:
        #     old_run_turns.append(Turn(solution.get_placements_from_diff(board)))
        # dedup_start_time = time.time()
        # unique_turns = dedup_turns(old_run_turns)
        # dedup_end_time = time.time()
        # print(f"DEDUP to {len(unique_turns)} solutions in {(dedup_end_time - dedup_start_time):.2f} secs.")
        # print(f"TOTAL: {(time.time() - start_time):.2f} secs")
        # for turn in unique_turns:
        #     solutions.append(Solution(board, turn, scoreboard))
        # solutions.sort(reverse=True)
        # for index, solution in enumerate(solutions[:MAX_SOLUTIONS_TO_SHOW]):
        #     print(f"\n---------Solution {index + 1}-----------\n{solution}")

        # compare_solutions(board, scoreboard, unique_turns, turns)


def compare_solutions(board: Board, scoreboard: Scoreboard, old_turns: list[Turn], new_turns: list[Turn2]):
    converted_new_turns = list(map(lambda x: Turn(x.generate_placement_list()), new_turns))
    missing_new_turns = []
    for turn in converted_new_turns:
        if turn not in old_turns:
            missing_new_turns.append(turn)
    print(f"{len(missing_new_turns)} turns in OLD not in NEW")
    for turn in missing_new_turns:
        s = Solution(board, turn, scoreboard)
        print(s)
        break

    missing_old_turns = []
    for turn in converted_new_turns:
        if turn not in old_turns:
            missing_old_turns.append(turn)
    print(f"{len(missing_old_turns)} turns in NEW not in OLD")

    for turn in missing_old_turns:
        s = Solution(board, turn, scoreboard)
        print(s)
        break


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


def get_games(directory_path: str) -> list[str]:
    games: set[str] = set()
    for filename in os.listdir(directory_path):
        match = re.match(GAME_FILE_PATTERN, filename)
        if match:
            games.add(match.groups()[0])
    return sorted(list(games))


def select_option(prompt: str, values: list[str]) -> Optional[str]:
    print(f"\n{prompt}")
    for index, option in enumerate(values):
        print(f"{index + 1}) {option}")
    while True:
        try:
            user_input = input("\nMake a selection: ")
            value = int(user_input)
            return values[value - 1]
        except KeyboardInterrupt:
            return None
        except:
            print("Invalid input. Select a valid option.")


def get_latest_game_file(directory_path: str, game_name: str) -> str:
    files = []
    for filename in os.listdir(directory_path):
        match = re.match(GAME_FILE_PATTERN, filename)
        if match and match.groups()[0] == game_name:
            files.append(os.path.join(directory_path, filename))
    return sorted(files, reverse=True)[0]


def get_player_tiles() -> Optional[PlayerTiles]:
    while True:
        user_input = input("\nEnter tiles ('*' for wildcard): ")
        try:
            player_tiles = PlayerTiles(user_input)
            break
        except KeyboardInterrupt:
            print("Exiting.")
            return None
        except ValueError as e:
            print('Invalid input')
    print(player_tiles)
    return player_tiles


def get_tests(directory_path: str) -> list[str]:
    tests: set[str] = set()
    for filename in os.listdir(directory_path):
        match = re.match(TEST_FILE_PATTERN, filename)
        if match:
            tests.add(match.groups()[0])
    return sorted(list(tests))


def read_player_tiles_file(filepath: str) -> PlayerTiles:
    with open(filepath, 'r') as file:
        return PlayerTiles(file.readline())


def select_solution(solutions: list[Solution]) -> Optional[Solution]:
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


if __name__ == "__main__":
    main()
