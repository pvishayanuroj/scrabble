from typing import Dict, Optional

from util import get_all_substrings, timer
from word_type import WordType


class Dictionary:
    """Loads from a dictionary file and provides utility methods.

    The expected file format is one word per line.
    """

    def __init__(self, filepath: str, omitted_words_filepath: Optional[str] = None):
        self._words: set[str] = set()
        self._substrings: set[str] = set()
        self._substring_types: Dict[str, WordType] = {}
        self._load(filepath, omitted_words_filepath)

    def _load_omitted_words(self, filepath: str) -> set[str]:
        unique_words = set(self._read_file(filepath))
        return unique_words

    @timer
    def _load(self, filepath: str, omit_filepath: Optional[str]):
        # Load words to omit.
        omitted_words = (
            self._load_omitted_words(omit_filepath) if omit_filepath else set()
        )

        # Load the words.
        for word in self._read_file(filepath):
            if word not in omitted_words and word not in self._words:
                self._words.add(word)

        # Generate the substrings.
        for word in self._words:
            self._substrings.update(get_all_substrings(word))

        # Preprocess all the substrings.
        for substring in self._substrings:
            is_substring = True
            is_word = substring in self._words
            self._substring_types[substring] = WordType(is_substring, is_word)

        print(f"Loaded {len(self._words)} dictionary words and {len(self._substrings)} substrings.")

    def _read_file(self, filepath: str) -> list[str]:
        words = []
        with open(filepath, "r") as file:
            for line in file.readlines():
                if line == "":
                    continue
                words.append(line.strip().upper())
        return words

    def is_word(self, value: str) -> bool:
        return value in self._words

    def is_substring(self, value: str) -> bool:
        return value in self._substrings

    def check(self, value: str) -> Optional[WordType]:
        return self._substring_types.get(value)
