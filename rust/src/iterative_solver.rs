use crate::{
    board::Board, dictionary::Dictionary, iterators::UniqueFirstAndRestIterator, letter::Letter,
    scoreboard::Scoreboard, turn::Turn,
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
    let turns = vec![];
    for (letter, remaining_letters) in UniqueFirstAndRestIterator::new(letters) {}
    turns
}

fn evaluate(board: &Board, turn: &Turn) -> Vec<Turn> {
    let expanded = vec![];
    expanded
}
