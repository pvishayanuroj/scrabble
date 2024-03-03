from typing import Optional

from word_type import WordType


class Dictionary:
    """Loads from a dictionary file and provides utility methods.
    
    The expected file format is one word per line.
    """
    def __init__(self, filepath: str, omit_filepath=None):
        self._words = set()
        self._substrings = set()
        self._words2 = {}
        omitted_words = (
            self._load_omitted_words(omit_filepath) if omit_filepath else set()
        )
        self._load(filepath, omitted_words)

    def _load_omitted_words(self, filepath: str) -> set[str]:
        unique_words = set(self._read_file(filepath))
        return unique_words

    def _load(self, filepath: str, omitted_words: set[str]):
        for word in self._read_file(filepath):
            if word not in omitted_words and word not in self._words:
                self._words.add(word)
        self._preprocess()
        self._preprocess2()
        print(f"Loaded {len(self._words)} words")
        print(f"Preprocessed {len(self._substrings)} substrings")

    def _read_file(self, filepath: str) -> list[str]:
        words = []
        with open(filepath, "r") as file:
            for line in file.readlines():
                if line == "":
                    continue
                words.append(line.strip().upper())
        return words

    def _preprocess(self):
        for word in self._words:
            for substring in get_all_substrings(word):
                self._substrings.add(substring)

    def _preprocess2(self):
        for value in self._substrings:
            is_substring = True
            is_word = value in self._words
            self._words2[value] = WordType(is_substring, is_word)

    def is_word(self, value: str) -> bool:
        return value in self._words

    def is_substring(self, value: str) -> bool:
        return value in self._substrings

    def check(self, value: str) -> Optional[WordType]:
        return self._words2.get(value)


def get_all_substrings(word: str) -> list[str]:
    substrings = []
    for substring_len in range(1, len(word) + 1):
        for start_index in range(len(word) - substring_len + 1):
            substrings.append(word[start_index : (start_index + substring_len)])
    return substrings
