use crate::{enums::Shape, placement::Placement};
use std::ops::RangeInclusive;

pub struct Turn {
    placements: Vec<Placement>,
    shape: Shape,
    range: RangeInclusive<u8>,
}
