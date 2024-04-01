use crate::board_iterator::BoardIterator;
use crate::position::Position;
use crate::size::Size;
use crate::util::char_from_string;
use crate::{letter::Letter, util::read_lines};
use std::fmt;
use std::io;

pub struct Board {
    size: Size,
    state: Vec<Vec<Option<Letter>>>,
}

#[derive(Debug)]
pub enum BoardLoadError {
    IoError(io::Error),
    ParseError(String),
}

impl Board {
    pub fn from_file(filepath: &str) -> Result<Board, BoardLoadError> {
        let mut state = vec![];
        let mut num_cols = 0;
        for line in read_lines(filepath).map_err(BoardLoadError::IoError)? {
            let line = line.map_err(BoardLoadError::IoError)?;
            if line == "" {
                continue;
            }
            let mut row: Vec<Option<Letter>> = vec![];
            for chunk in line.split_whitespace() {
                match char_from_string(chunk) {
                    Some(letter) => {
                        if letter == '-' {
                            row.push(None);
                        } else if letter.is_ascii_uppercase() {
                            row.push(Some(Letter::new(letter)));
                        } else if letter.is_ascii_lowercase() {
                            row.push(Some(Letter::new_wildcard(letter)));
                        } else {
                            return Err(BoardLoadError::ParseError(format!(
                                "Unexpected character: {letter}"
                            )));
                        }
                    }
                    None => {
                        return Err(BoardLoadError::ParseError(format!(
                            "Could not parse chunk: {chunk}"
                        )));
                    }
                }
            }
            if num_cols == 0 {
                num_cols = row.len();
            } else if num_cols != row.len() {
                return Err(BoardLoadError::ParseError(format!(
                    "Invalid number of columns"
                )));
            }
            state.push(row);
        }
        let size = Size::new(state.len(), num_cols);
        Ok(Board { size, state })
    }

    pub fn get_letter(&self, position: &Position) -> Option<Letter> {
        self.state[position.row][position.col]
    }

    pub fn is_any_adjacent_position_filled(&self, position: &Position) -> bool {}

    /// A position is a valid first tile position if it is empty but is adjacent to any non-empty
    /// tile.
    fn is_valid_first_tile_position(&self, position: &Position) -> bool {
        if !self.get_letter(position).is_none() {
            return false;
        }
    }

    pub fn get_first_tile_positions(&self) -> Vec<Position> {
        BoardIterator::new(self.size)
            .into_iter()
            .filter(|x| self.is_valid_first_tile_position(x))
            .collect()
    }
}

impl fmt::Display for Board {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        for row in &self.state {
            let mut row_string = String::from("");
            for col in row {
                match col {
                    Some(letter) => row_string += &format!("{letter} "),
                    None => row_string += "- ",
                }
            }
            writeln!(f, "{}", row_string)?;
        }
        Ok(())
    }
}
