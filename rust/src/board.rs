use crate::util::char_from_string;
use crate::{letter::Letter, util::read_lines};
use std::fmt;
use std::io;

pub struct Board {
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
            state.push(row);
        }
        Ok(Board { state })
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
