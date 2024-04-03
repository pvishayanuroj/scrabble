use crate::position::Position;

pub struct WordPlacement {
    pub word: String,
    pub start_position: Position,
    pub end_position: Position,
}

impl WordPlacement {
    pub fn new(word: String, start_position: Position, end_position: Position) -> Self {
        WordPlacement {
            word,
            start_position,
            end_position,
        }
    }
}
