use crate::{position::Position, size::Size};

pub struct BoardIterator {
    curr_row: usize,
    curr_col: usize,
    size: Size,
}

impl BoardIterator {
    pub fn new(size: Size) -> Self {
        BoardIterator {
            size,
            curr_row: 0,
            curr_col: 0,
        }
    }
}

impl Iterator for BoardIterator {
    type Item = Position;

    fn next(&mut self) -> Option<Self::Item> {
        let position = Position::new(self.curr_row, self.curr_col);
        self.curr_col += 1;
        if self.curr_col == self.size.num_cols {
            self.curr_col = 0;
            self.curr_row += 1;
        }
        if self.curr_row == self.size.num_rows {
            return None;
        }
        Some(position)
    }
}
