use crate::dictionary::Dictionary;
use board::Board;

pub mod board;
pub mod board_iterator;
pub mod dictionary;
pub mod dictionary_entry;
pub mod direction_iterator;
pub mod enums;
pub mod iterative_solver;
pub mod letter;
pub mod placement;
pub mod position;
pub mod scoreboard;
pub mod size;
pub mod turn;
pub mod unique_and_first_iterator;
pub mod util;

fn main() {
    let dictionary = Dictionary::from_file(
        "../dictionaries/279k-dictionary.txt",
        Some("../dictionaries/omit.txt"),
    );
    let board = Board::from_file("../testcases/test3_state.txt").unwrap();
    println!("{}", board);
}
