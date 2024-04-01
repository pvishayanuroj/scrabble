use std::fmt;

use crate::enums::Direction;

pub struct Position {
    pub row: usize,
    pub col: usize,
}

impl Position {
    pub fn new(row: usize, col: usize) -> Position {
        Position { row, col }
    }

    pub fn increment(&self, direction: Direction) -> Position {
        match direction {
            Direction::Left => Position::new(self.row - 1),
            Direction::Right => todo!(),
            Direction::Up => todo!(),
            Direction::Down => todo!(),
        }
    }
}

impl fmt::Display for Position {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "[{}, {}]", self.row, self.col)
    }
}
