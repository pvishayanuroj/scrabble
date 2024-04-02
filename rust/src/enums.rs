#[derive(Copy, Clone)]
pub enum Shape {
    Vertical,
    Horizontal,
}

#[derive(Copy, Clone)]
pub enum Direction {
    Left,
    Right,
    Up,
    Down,
}

impl Shape {
    pub fn start_direction(&self) -> Direction {
        match self {
            Shape::Vertical => Direction::Up,
            Shape::Horizontal => Direction::Left,
        }
    }

    pub fn end_direction(&self) -> Direction {
        match self {
            Shape::Vertical => Direction::Down,
            Shape::Horizontal => Direction::Right,
        }
    }

    pub fn opposite(&self) -> Shape {
        match self {
            Shape::Vertical => Shape::Horizontal,
            Shape::Horizontal => Shape::Vertical,
        }
    }
}

impl Direction {
    pub fn reverse(&self) -> Direction {
        match self {
            Direction::Left => Direction::Right,
            Direction::Right => Direction::Left,
            Direction::Up => Direction::Down,
            Direction::Down => Direction::Up,
        }
    }
}
