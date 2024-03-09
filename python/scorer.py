from board import Board
from constants import MAX_LENGTH_WORD_SCORE, MAX_PLAYER_TILES
from enums import Direction, Shape
from letter import Letter
from position import Position
from scoreboard import Scoreboard
from scored_letter import ScoredLetter
from turns import Turn


def calculate_score(board: Board, scoreboard: Scoreboard, turn: Turn) -> int:
    """Calculates the score based on applying the placements to the current board."""
    placements = turn.generate_placement_list()
    # Get the word by selecting the first placement and expanding
    # in both directions.
    prefix = _expand_tiles(
        board, turn, placements[0].position, turn.shape.start_direction
    )
    suffix = _expand_tiles(
        board, turn, placements[0].position, turn.shape.end_direction
    )
    word = prefix + [ScoredLetter.from_placement(placements[0])] + suffix
    words = [word]

    # Get "cross" shape words.
    cross_shape = turn.shape.opposite
    for placement in placements:
        prefix = _expand_non_active_tiles(
            board, placement.position, cross_shape.start_direction
        )
        suffix = _expand_non_active_tiles(
            board, placement.position, cross_shape.end_direction
        )
        word = prefix + [ScoredLetter.from_placement(placement)] + suffix
        words.append(word)

    # Perform scoring.
    score = 0
    for word in words:
        if len(word) < 2:
            continue
        score += _score_word(scoreboard, word)
    if len(placements) == MAX_PLAYER_TILES:
        score += MAX_LENGTH_WORD_SCORE
    return score


def _expand_tiles(
    board: Board, turn: Turn, position: Position, direction: Direction
) -> list[ScoredLetter]:
    """Gets the letters starting from the adjacent tile in the given direction to the position until the end or an empty tile.

    Uses both the board and the placed letters in a turn.
    """
    letters: list[ScoredLetter] = []
    curr_position = position
    while True:
        next_position = curr_position.move(direction)
        non_active_letter = board.get_letter_checked(next_position)
        active_letter = turn.get_tile_checked(next_position)
        if non_active_letter is not None:
            letters.append(ScoredLetter(next_position, non_active_letter, False))
        elif active_letter is not None:
            letters.append(ScoredLetter(next_position, active_letter, True))
        else:
            break
        curr_position = next_position
    if direction == Direction.LEFT or direction == Direction.UP:
        return letters[::-1]
    return letters


def _expand_non_active_tiles(
    board: Board, position: Position, direction: Direction
) -> list[ScoredLetter]:
    """Gets the letters starting from the adjacent tile in the given direction to the position until the end or an empty tile.

    Uses only the board letters.
    """
    letters: list[ScoredLetter] = []
    curr_position = position
    while True:
        next_position = curr_position.move(direction)
        letter = board.get_letter_checked(next_position)
        if letter is None:
            break
        letters.append(ScoredLetter(next_position, letter, False))
        curr_position = next_position
    if direction == Direction.LEFT or direction == Direction.UP:
        return letters[::-1]
    return letters


def _score_word(scoreboard: Scoreboard, word: list[ScoredLetter]) -> int:
    score = 0
    word_multipler = 1
    for scored_letter in word:
        letter_value = _score_letter(scoreboard, scored_letter.letter)
        letter_multiplier = 1
        if scored_letter.is_active:
            word_multipler *= scoreboard.get_word_multiplier(scored_letter.position)
            letter_multiplier = scoreboard.get_letter_multiplier(scored_letter.position)
        score += letter_value * letter_multiplier
    return score * word_multipler


def _score_letter(scoreboard: Scoreboard, letter: Letter) -> int:
    if letter.is_wildcard:
        return 0
    return scoreboard.get_letter_value(letter.val)
