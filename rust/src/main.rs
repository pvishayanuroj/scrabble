use board::Board;

pub mod board;
pub mod letter;
pub mod util;

fn main() {
    let board = Board::from_file("../testcases/test3_state.txt").unwrap();
    println!("{}", board);
}
