use std::fmt;

#[derive(Hash, Eq, PartialEq)]
pub struct Letter {
    pub val: char,
    pub is_wildcard: bool,
}

impl Letter {
    pub fn new(val: char) -> Letter {
        Letter {
            val,
            is_wildcard: false,
        }
    }

    pub fn new_wildcard(val: char) -> Letter {
        Letter {
            val,
            is_wildcard: true,
        }
    }
}

impl fmt::Display for Letter {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.val)
    }
}
