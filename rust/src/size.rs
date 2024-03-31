use crate::position::Position;

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
}
