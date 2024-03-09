from board import Board
from constants import MAX_LENGTH_WORD_SCORE, MAX_PLAYER_TILES
from letter import Letter
from position import Position
from scoreboard import Scoreboard
from turns import Turn


def calculate_score(board: Board, scoreboard: Scoreboard, turn: Turn) -> int:
    """Calculates the score based on applying the placements to the current board."""

    placements = turn.generate_placement_list()

    # Get the word by selecting the first placement and expanding
    # in both directions.
    curr_position = placements[0].position
    # The bool indicates whether or not it is an active tile.
    start_letters: list[tuple[Letter, Position, bool]] = []
    while True:
        next_position = curr_position.move(turn.shape.start_direction)
        non_active_tile = board.get_letter_checked(next_position)
        active_tile = turn.get_tile_checked(next_position)
        if non_active_tile is not None:
            foo = (non_active_tile, next_position, False)
            start_letters.append(foo)
        elif active_tile is not None:
            foo = (active_tile, next_position, True)
            start_letters.append(foo)
        else:
            break
        curr_position = next_position
    start_letters.reverse()

    curr_position = placements[0].position
    end_letters: list[tuple[Letter, Position, bool]] = []
    while True:
        next_position = curr_position.move(turn.shape.end_direction)
        non_active_tile = board.get_letter_checked(next_position)
        active_tile = turn.get_tile_checked(next_position)
        if non_active_tile is not None:
            foo = (non_active_tile, next_position, False)
            end_letters.append(foo)
        elif active_tile is not None:
            foo = (active_tile, next_position, True)
            end_letters.append(foo)
        else:
            break
        curr_position = next_position

    foo = (placements[0].letter, placements[0].position, True)
    word = start_letters + [foo] + end_letters
    words = [word]

    # Get "cross" shape words.
    cross_shape = turn.shape.opposite
    for placement in placements:
        curr_position = placement.position
        start_letters_cross: list[tuple[Letter, Position, bool]] = []
        while True:
            next_position = curr_position.move(cross_shape.start_direction)
            non_active_tile = board.get_letter_checked(next_position)
            if non_active_tile is not None:
                foo = (non_active_tile, next_position, False)
                start_letters_cross.append(foo)
            else:
                break
            curr_position = next_position
        start_letters_cross.reverse()

        curr_position = placement.position
        end_letters_cross: list[tuple[Letter, Position, bool]] = []
        while True:
            next_position = curr_position.move(cross_shape.end_direction)
            non_active_tile = board.get_letter_checked(next_position)
            if non_active_tile is not None:
                foo = (non_active_tile, next_position, False)
                end_letters_cross.append(foo)
            else:
                break
            curr_position = next_position

        foo = (placement.letter, placement.position, True)
        word = start_letters_cross + [foo] + end_letters_cross
        words.append(word)

    score = 0
    for word in words:
        if len(word) < 2:
            continue
        word_multipler = 1
        word_total = 0
        for letter, position, is_active_tile in word:
            letter_value = 0 if letter.is_wildcard else scoreboard.get_letter_value(letter.val)
            if is_active_tile:
                word_multipler *= scoreboard.get_word_multiplier(position)
            letter_multiplier = 1 if not is_active_tile else scoreboard.get_letter_multiplier(position)
            word_total += (letter_value * letter_multiplier)
        score += (word_total * word_multipler)

    if len(placements) == MAX_PLAYER_TILES:
        score += MAX_LENGTH_WORD_SCORE

    return score
