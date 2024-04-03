use std::fmt;

use crate::{letter::Letter, position::Position};

pub struct Placement {
    pub letter: Letter,
    pub position: Position,
}

impl Placement {
    pub fn new(&self, letter: Letter, position: Position) -> Placement {
        Placement { letter, position }
    }
}

impl fmt::Display for Placement {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}: {}]", self.position, self.letter)
    }
}
