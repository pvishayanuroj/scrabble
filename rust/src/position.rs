use std::fmt;

pub struct Position {
    row: u8,
    col: u8,
}

impl Position {
    pub fn new(row: u8, col: u8) -> Position {
        Position { row, col }
    }
}

impl fmt::Display for Position {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "[{}, {}]", self.row, self.col)
    }
}
