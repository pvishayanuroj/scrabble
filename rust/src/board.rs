use crate::board_iterator::BoardIterator;
use crate::direction_iterator::DirectionIterator;
use crate::enums::{Direction, Shape};
use crate::placement::Placement;
use crate::position::Position;
use crate::size::Size;
use crate::util::char_from_string;
use crate::word_placement::WordPlacement;
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

    pub fn get_letter(&self, position: &Position) -> &Option<Letter> {
        &self.state[position.row][position.col]
    }

    /// A position is a valid first tile position if it is empty but is adjacent to any non-empty
    /// tile.
    fn is_valid_first_tile_position(&self, position: &Position) -> bool {
        if !self.get_letter(position).is_none() {
            return false;
        }
        for direction in DirectionIterator::new() {
            if let Some(adjacent_position) = &self.size.increment(position, direction) {
                if let Some(_) = self.get_letter(adjacent_position) {
                    return true;
                }
            }
        }
        return false;
    }

    pub fn get_first_tile_positions(&self) -> Vec<Position> {
        BoardIterator::new(self.size)
            .into_iter()
            .filter(|x| self.is_valid_first_tile_position(x))
            .collect()
    }

    /// Checks adjacent tiles in the given direction and returns the longest "word" formed by tiles
    /// in that direction. Returns none if no filled tiles were found.
    fn get_contiguous_letters(
        &self,
        position: &Position,
        direction: Direction,
    ) -> Option<WordPlacement> {
        let mut start_position = None;
        let mut end_position = None;
        let mut word = String::new();
        loop {
            match &self.size.increment(position, direction) {
                Some(new_position) => match self.get_letter(new_position) {
                    Some(letter) => {
                        word.push(letter.val);
                        start_position.get_or_insert(*new_position);
                        end_position.insert(*new_position);
                    }
                    None => break,
                },
                None => break,
            }
        }

        match (start_position, end_position) {
            (Some(start_position), Some(end_position)) => match direction {
                Direction::Right | Direction::Down => {
                    Some(WordPlacement::new(word, start_position, end_position))
                }
                Direction::Left | Direction::Up => Some(WordPlacement::new(
                    word.chars().rev().collect(),
                    end_position,
                    start_position,
                )),
            },
            _ => None,
        }
    }

    pub fn get_word_from_placement(&self, placement: &Placement, shape: Shape) -> WordPlacement {
        let start_word = self.get_contiguous_letters(&placement.position, shape.start_direction());
        let end_word = self.get_contiguous_letters(&placement.position, shape.end_direction());
        match (start_word, end_word) {
            (None, None) => WordPlacement::new(
                placement.letter.val.to_string(),
                placement.position,
                placement.position,
            ),
            (None, Some(end_word)) => WordPlacement::new(
                placement.letter.val.to_string() + &end_word.word,
                placement.position,
                end_word.end_position,
            ),
            (Some(start_word), None) => WordPlacement::new(
                start_word.word + &placement.letter.val.to_string(),
                start_word.start_position,
                placement.position,
            ),
            (Some(start_word), Some(end_word)) => WordPlacement::new(
                start_word.word + &placement.letter.val.to_string() + &end_word.word,
                start_word.start_position,
                end_word.end_position,
            ),
        }
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
