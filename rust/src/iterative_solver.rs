use crate::{board::Board, letter::Letter, scoreboard::Scoreboard, turn::Turn};

pub fn solve(board: &Board, scoreboard: &Scoreboard, letters: Vec<Letter>) {
    // Run iterative DFS.
    let mut stack: Vec<Turn> = initial_eval(board, scoreboard, letters);
    while let Some(turn) = &stack.pop() {
        stack.extend(evaluate(board, turn));
    }
}

fn initial_eval(board: &Board, scoreboard: &Scoreboard, letters: Vec<Letter>) -> Vec<Turn> {
    let turns = vec![];
    turns
}

fn evaluate(board: &Board, turn: &Turn) -> Vec<Turn> {
    let expanded = vec![];
    expanded
}
