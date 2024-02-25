from typing import List


class Dictionary:
    def __init__(self, filepath: str):
        self._words = set()
        self._substrings = set()
        self.load(filepath)

    def load(self, filepath: str):
        with open(filepath, 'r') as file:
            for line in file.readlines():
                if line == '':
                    continue
                self._words.add(line.strip().upper())
        self.preprocess()
        print(f"Loaded {len(self._words)} words")
        print(f"Preprocessed {len(self._substrings)} substrings")

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
