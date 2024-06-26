from __future__ import annotations
import argparse
import os
import re
from board import Board
from constants import (
    ENDC,
    GAME_FILE_PATTERN,
    GREEN,
    MAX_SOLUTIONS_TO_SHOW,
    RED,
    TEST_FILE_PATTERN,
    WORD_PATTERN,
)
from dictionary import Dictionary
from enums import MenuSelection
from placements import Placements
from player_tiles import PlayerTiles
from scoreboard import Scoreboard
from solution import Solution
from solver import solve
from typing import Optional


def main():
    parser = argparse.ArgumentParser(description="A command line word puzzle solver.")

    parser.add_argument(
        "--dictionary",
        default="dictionaries/279k-dictionary.txt",
        help="Dictionary file path (default: %(default)s)",
    )
    parser.add_argument(
        "--omit",
        default="dictionaries/omit.txt",
        help="List of words to omit from dictionary (default: %(default)s)",
    )
    parser.add_argument(
        "--board",
        default="boards/official.txt",
        help="Board file path (default: %(default)s)",
    )
    parser.add_argument(
        "--points", default="points.txt", help="Points file path (default: %(default)s)"
    )
    parser.add_argument(
        "--games", default="games/", help="Games directory path (default: %(default)s)"
    )
    parser.add_argument(
        "--tests",
        default="testcases/",
        help="Test case directory path (default: %(default)s)",
    )

    args = parser.parse_args()

    selection = select_menu_option()
    if selection == MenuSelection.NEW_GAME:
        player_tiles = PlayerTiles.from_input()
        if player_tiles is None:
            return
        scoreboard = Scoreboard(args.board, args.points)
        dictionary = Dictionary(args.dictionary, args.omit)
        board = Board(scoreboard.size, dictionary)

        solutions = solve(board, scoreboard, dictionary, player_tiles)
        selected_solution = select_solution(solutions[:MAX_SOLUTIONS_TO_SHOW])
        if not selected_solution:
            return
        game_name = input("Enter a game name: ")
        selected_solution.save(generate_file_name(args.games, game_name))
    elif selection == MenuSelection.LOAD_GAME:
        game_names = get_games(args.games)
        if len(game_names) < 1:
            print("No saved games found. Exiting.")
            return
        if len(game_names) == 1:
            game_name = game_names[0]
        else:
            game_name = select_option("Available games:", game_names)
        if game_name is None:
            return
        game_file = os.path.join(args.games, f"{game_name}.txt")
        player_tiles = PlayerTiles.from_input()
        if player_tiles is None:
            return
        scoreboard = Scoreboard(args.board, args.points)
        dictionary = Dictionary(args.dictionary, args.omit)
        board = Board(scoreboard.size, dictionary)
        board.load_state(game_file)

        solutions = solve(board, scoreboard, dictionary, player_tiles)
        selected_solution = select_solution(solutions)
        if selected_solution:
            selected_solution.save(game_file)
    elif selection == MenuSelection.RUN_TEST:
        test_names = get_tests(args.tests)
        test_name = select_option("Test cases:", test_names)
        if test_name is None:
            return
        state_file = os.path.join(args.tests, f"{test_name}_state.txt")
        player_tiles_file = os.path.join(args.tests, f"{test_name}_tiles.txt")
        golden_file = os.path.join(args.tests, f"{test_name}_golden.txt")
        scoreboard = Scoreboard(args.board, args.points)
        dictionary = Dictionary(args.dictionary)
        board = Board(scoreboard.size, dictionary)
        board.load_state(state_file)
        player_tiles = read_player_tiles_file(player_tiles_file)

        solutions = solve(board, scoreboard, dictionary, player_tiles)

        actual = list(
            map(
                lambda solution: (
                    Placements(solution.turn.generate_placement_list()),
                    solution.score,
                ),
                solutions,
            )
        )
        compare_solutions(actual, load_golden(golden_file))

    elif selection == MenuSelection.REGEN_GOLDENS:
        test_names = get_tests(args.tests)
        test_name = select_option("Test cases:", test_names)
        if test_name is None:
            return
        state_file = os.path.join(args.tests, f"{test_name}_state.txt")
        player_tiles_file = os.path.join(args.tests, f"{test_name}_tiles.txt")
        golden_file = os.path.join(args.tests, f"{test_name}_golden.txt")
        scoreboard = Scoreboard(args.board, args.points)
        dictionary = Dictionary(args.dictionary)
        board = Board(scoreboard.size, dictionary)
        board.load_state(state_file)
        player_tiles = read_player_tiles_file(player_tiles_file)

        solutions = solve(board, scoreboard, dictionary, player_tiles)
        with open(golden_file, "w") as file:
            file.writelines(
                map(lambda solution: solution.serialize() + "\n", solutions)
            )
        print(f"Wrote {golden_file}")
    elif selection == MenuSelection.UPDATE_OMIT:
        words = read_word_list()
        if words is None:
            return
        if not check_word_list(words):
            return
        update_omitted_words(args.omit, words)
    else:
        print("Unsupported menu selection")


def compare_solutions(
    actual: list[tuple[Placements, int]], expected: list[tuple[Placements, int]]
):
    actual_placements = set(map(lambda x: x[0], actual))
    expected_placements = set(map(lambda x: x[0], expected))
    extra_placements = actual_placements - expected_placements
    missing_placements = expected_placements - actual_placements

    if len(extra_placements) == 0 and len(missing_placements) == 0:
        actual_scores = dict(actual)
        incorrect_scores = []
        for placements, expected_score in expected:
            actual_score = actual_scores[placements]
            if actual_score != expected_score:
                incorrect_scores.append(
                    (placements, actual_score, expected_score),
                )
        if len(incorrect_scores) == 0:
            print(f"{GREEN}PASS{ENDC}: {len(actual)} turns in TEST match GOLDEN.")
        else:
            print(f"{RED}FAIL{ENDC}: {len(incorrect_scores)} incorrect scores in TEST.")
    else:
        if len(extra_placements) > 0:
            print(f"{RED}FAIL{ENDC}: {len(extra_placements)} extra turns in TEST.")
        if len(missing_placements) > 0:
            print(f"{RED}FAIL{ENDC}: {len(missing_placements)} missing turns in TEST.")


def generate_file_name(directory_path: str, game_name: str) -> str:
    filename = f"{game_name}.txt"
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


def get_tests(directory_path: str) -> list[str]:
    tests: set[str] = set()
    for filename in os.listdir(directory_path):
        match = re.match(TEST_FILE_PATTERN, filename)
        if match:
            tests.add(match.groups()[0])
    return sorted(list(tests))


def read_player_tiles_file(filepath: str) -> PlayerTiles:
    with open(filepath, "r") as file:
        return PlayerTiles(file.readline())


def select_solution(solutions: list[Solution]) -> Optional[Solution]:
    print(f"Generated {len(solutions)} solutions")
    for index, solution in enumerate(solutions[:MAX_SOLUTIONS_TO_SHOW]):
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


def load_golden(filepath: str) -> list[tuple[int, Placements]]:
    output: list[tuple[int, Placements]] = []
    with open(filepath, "r") as file:
        for line in file.readlines():
            if line != "":
                elements = line.strip().split("||")
                if len(elements) != 2:
                    raise ValueError(f"Improperly formatted line: {line}")
                score = int(elements[0])
                placement_strings = elements[1].split("|")
                placements = Placements.from_strings(placement_strings)
                output.append(
                    (placements, score),
                )
    return output


def read_word_list() -> Optional[list[str]]:
    while True:
        user_input = input("\nEnter word or comma-separated words: ")
        try:
            input_words = user_input.split(",")
            words = []
            words_valid = True
            for raw_word in input_words:
                word = raw_word.upper().strip()
                if re.match(WORD_PATTERN, word):
                    words.append(word)
                else:
                    words_valid = False
                    break
            if words_valid:
                return words
        except KeyboardInterrupt:
            print("Exiting.")
            return None


def check_word_list(words: list[str]) -> bool:
    words_list = ""
    for index, word in enumerate(words):
        if index != 0:
            words_list += ", "
        words_list += f"{RED}{word}{ENDC}"
    response = input(f"Add the following words: {words_list}\nDo you want to continue [Y/n]? ")
    return response.upper().strip() == "Y"


def update_omitted_words(filepath: str, words: list[str]):
    existing_words = []
    if os.path.exists(filepath):
        existing_words = []
        with open(filepath, "r") as file:
            for line in file.readlines():
                if line == "":
                    continue
                existing_words.append(line.strip().upper())
    new_words = list(set(existing_words + words))
    new_words.sort()
    with open(filepath, 'w') as file:
        for word in new_words:
            file.write(f"{word}\n")
    print(f"Updated {filepath}")


if __name__ == "__main__":
    main()
