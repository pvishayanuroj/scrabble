use std::collections::HashSet;
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

pub fn get_all_substrings(val: &str) -> HashSet<String> {
    let mut substrings: HashSet<String> = HashSet::new();
    for substring_len in 1..=val.len() {
        for start_index in 0..=(val.len() - substring_len) {
            let substring = &val[start_index..(start_index + substring_len)];
            substrings.insert(substring.to_string());
        }
    }
    substrings
}
