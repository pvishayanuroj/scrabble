pub struct DictionaryEntry {
    is_substring: bool,
    is_word: bool,
}

impl DictionaryEntry {
    pub fn new(is_substring: bool, is_word: bool) -> DictionaryEntry {
        DictionaryEntry {
            is_substring,
            is_word,
        }
    }

    pub fn is_substring(&self) -> bool {
        self.is_substring
    }

    pub fn is_word(&self) -> bool {
        self.is_word
    }
}
