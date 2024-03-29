pub struct Size {
    pub num_rows: u8,
    pub num_cols: u8,
}

impl Size {
    pub fn new(num_rows: u8, num_cols: u8) -> Size {
        Size { num_rows, num_cols }
    }
}
