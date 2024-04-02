use crate::{enums::Direction, position::Position};

#[derive(Copy, Clone)]
pub struct Size {
    pub num_rows: usize,
    pub num_cols: usize,
}

impl Size {
    pub fn new(num_rows: usize, num_cols: usize) -> Size {
        Size { num_rows, num_cols }
    }

    pub fn is_within_bounds(&self, position: &Position) -> bool {
        position.row >= 0
            && position.row < self.num_rows
            && position.col >= 0
            && position.col < self.num_cols
    }

    pub fn increment(&self, position: &Position, direction: Direction) -> Option<Position> {
        match direction {
            Direction::Left => {
                if position.row == 0 {
                    return None;
                }
                return Some(Position::new(position.row - 1, position.col));
            }
            Direction::Right => {
                if position.row >= (self.num_rows - 1) {
                    return None;
                }
                return Some(Position::new(position.row + 1, position.col));
            }
            Direction::Up => {
                if position.col == 0 {
                    return None;
                }
                return Some(Position::new(position.row, position.col - 1));
            }
            Direction::Down => {
                if position.row >= (self.num_cols - 1) {
                    return None;
                }
                return Some(Position::new(position.row, position.col + 1));
            }
        }
    }
}
