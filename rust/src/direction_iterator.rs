use crate::enums::Direction;

pub struct DirectionIterator {
    curr_direction: Option<Direction>,
}

impl DirectionIterator {
    pub fn new() -> Self {
        DirectionIterator {
            curr_direction: Some(Direction::Up),
        }
    }
}

impl Iterator for DirectionIterator {
    type Item = Direction;

    fn next(&mut self) -> Option<Self::Item> {
        let value = self.curr_direction.take();
        self.curr_direction = match value {
            Some(Direction::Up) => Some(Direction::Down),
            Some(Direction::Down) => Some(Direction::Left),
            Some(Direction::Left) => Some(Direction::Right),
            Some(Direction::Right) => None,
            None => None,
        };
        value
    }
}
