class WordType:
    """Helper class to categorize words."""
    def __init__(self, is_substring: bool, is_word: bool):
        self._is_substring = is_substring
        self._is_word = is_word

    def __str__(self) -> str:
        return f'Word: {self._is_word}, Substr: {self._is_substring}'

    @property
    def is_substring(self) -> bool:
        return self._is_substring

    @property
    def is_word(self) -> bool:
        return self._is_word
