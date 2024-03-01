from typing import List, Set


class Dictionary:
    def __init__(self, filepath: str, omit_filepath=None):
        self._words = set()
        self._substrings = set()
        omitted_words = self._load_omitted_words(omit_filepath) if omit_filepath else set()
        self._load(filepath, omitted_words)

    def _load_omitted_words(self, filepath: str) -> Set[str]:
        unique_words = set(self._read_file(filepath))
        return unique_words

    def _load(self, filepath: str, omitted_words: Set[str]):
        for word in self._read_file(filepath):
            if word not in omitted_words and word not in self._words:
                self._words.add(word)
        self.preprocess()
        print(f"Loaded {len(self._words)} words")
        print(f"Preprocessed {len(self._substrings)} substrings")

    def _read_file(self, filepath: str) -> List[str]:
        words = []
        with open(filepath, 'r') as file:
            for line in file.readlines():
                if line == '':
                    continue
                words.append(line.strip().upper())
        return words

    def preprocess(self):
        for word in self._words:
            for substring in get_all_substrings(word):
                self._substrings.add(substring)

    def is_word(self, value: str) -> bool:
        return value in self._words

    def is_substring(self, value: str) -> bool:
        return value in self._substrings


def get_all_substrings(word: str) -> List[str]:
    substrings = []
    for substring_len in range(2, len(word) + 1):
        for start_index in range(len(word) - substring_len + 1):
            substrings.append(word[start_index:(start_index + substring_len)])
    return substrings
