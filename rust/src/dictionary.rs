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
        validate_files: bool,
    ) -> Result<Dictionary, DictionaryLoadError> {
        let mut entries = HashMap::new();
        let mut words = HashSet::new();
        let mut substrings = HashSet::new();

        let omitted_words: HashSet<String> = match omitted_words_filepath {
            Some(omitted_words_filepath) => {
                Self::read_string_lines(omitted_words_filepath, validate_files)?
                    .into_iter()
                    .collect()
            }
            None => HashSet::new(),
        };

        for word in Self::read_string_lines(dictionary_filepath, validate_files)? {
            if !omitted_words.contains(&word) {
                substrings.extend(get_all_substrings(&word));
                words.insert(word);
            }
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

    fn read_string_lines(
        filepath: &str,
        validate: bool,
    ) -> Result<Vec<String>, DictionaryLoadError> {
        let mut strings = vec![];
        let pattern = Regex::new(r"^[a-zA-Z]+$").unwrap();
        for line in read_lines(filepath).map_err(DictionaryLoadError::IoError)? {
            let line = line.map_err(DictionaryLoadError::IoError)?;
            if line == "" {
                continue;
            }
            if validate {
                if pattern.is_match(&line) {
                    strings.push(line);
                } else {
                    return Err(DictionaryLoadError::ParseError(format!(
                        "Unexpected line: {line}"
                    )));
                }
            } else {
                strings.push(line);
            }
        }
        Ok(strings)
    }

    pub fn lookup(&self, string: &String) -> Option<&DictionaryEntry> {
        self.entries.get(string)
    }
}
