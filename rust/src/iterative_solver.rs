use crate::{
    board::Board, dictionary::Dictionary, letter::Letter, scoreboard::Scoreboard, turn::Turn,
    unique_and_first_iterator::UniqueFirstAndRestIterator,
};

pub fn solve(
    board: &Board,
    scoreboard: &Scoreboard,
    dictionary: &Dictionary,
    letters: &Vec<Letter>,
) {
    // Run iterative DFS.
    let mut stack: Vec<Turn> = initial_eval(board, scoreboard, dictionary, letters);
    while let Some(turn) = &stack.pop() {
        stack.extend(evaluate(board, turn));
    }
}

fn initial_eval(
    board: &Board,
    scoreboard: &Scoreboard,
    dictionary: &Dictionary,
    letters: &Vec<Letter>,
) -> Vec<Turn> {
    let next_positions = board.get_first_tile_positions();

    let turns = vec![];
    for (letter, remaining_letters) in UniqueFirstAndRestIterator::new(letters) {
        for position in &next_positions {}
    }
    turns
}

fn evaluate(board: &Board, turn: &Turn) -> Vec<Turn> {
    let expanded = vec![];
    expanded
}
