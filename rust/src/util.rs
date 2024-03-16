use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

pub fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

/// Returns a character from a string that contains a single character.
///
/// Checks that the letter is either a lower or uppper-case letter.
/// Returns None of these conditions are not satisified.
///
pub fn char_from_string(val: &str) -> Option<char> {
    if val.len() == 1 {
        let val = val.chars().next().unwrap();
        if val == '-' || val.is_alphabetic() {
            return Some(val);
        }
    }
    None
}
