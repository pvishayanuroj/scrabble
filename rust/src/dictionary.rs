use crate::util::get_all_substrings;
use crate::{dictionary_entry::DictionaryEntry, util::read_lines};
use regex::Regex;
use std::collections::{HashMap, HashSet};
use std::io;

#[derive(Debug)]
pub enum DictionaryLoadError {
    IoError(io::Error),
    ParseError(String),
}

pub struct Dictionary {
    entries: HashMap<String, DictionaryEntry>,
}

impl Dictionary {
    pub fn from_file(
        dictionary_filepath: &str,
        omitted_words_filepath: Option<&str>,
    ) -> Result<Dictionary, DictionaryLoadError> {
        let pattern = Regex::new(r"^[a-zA-Z]+$").unwrap();

        let mut entries = HashMap::new();
        let mut words = HashSet::new();
        let mut substrings = HashSet::new();
        for line in read_lines(dictionary_filepath).map_err(DictionaryLoadError::IoError)? {
            let line = line.map_err(DictionaryLoadError::IoError)?;
            if line == "" {
                continue;
            }
            substrings.extend(get_all_substrings(&line));
            words.insert(line);
            // if pattern.is_match(&line) {
            //     substrings.extend(get_all_substrings(&line));
            //     words.insert(line);
            // } else {
            //     return Err(DictionaryLoadError::ParseError(format!(
            //         "Unexpected line: {line}"
            //     )));
            // }
        }

        println!(
            "Loaded {} dictionary words and {} substrings.",
            words.len(),
            substrings.len()
        );

        for substring in substrings {
            let entry = DictionaryEntry::new(true, words.contains(&substring));
            entries.insert(substring, entry);
        }

        Ok(Dictionary { entries })
    }

    pub fn lookup(&self, string: &String) -> Option<&DictionaryEntry> {
        self.entries.get(string)
    }
}
