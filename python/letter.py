from __future__ import annotations
import re

LETTER_PATTERN = r"^[a-zA-Z]$"


class Letter:
    """Represents a single letter."""

    def __init__(self, val: str, is_wildcard: bool) -> None:
        if not re.match(LETTER_PATTERN, val):
            raise ValueError("Expected a single letter.")
        self._val = val.upper()
        self._is_wildcard = is_wildcard

    def __lt__(self, other: Letter) -> bool:
        return self.val < other.val

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Letter):
            return NotImplemented
        return self.val == other.val and self.is_wildcard == other.is_wildcard

    @property
    def val(self) -> str:
        return self._val

    @property
    def is_wildcard(self) -> bool:
        return self._is_wildcard
