from position import Position
from enums import Shape


class WordPosition:
    def __init__(self, position: Position, word: str, shape: Shape):
        self._position = position
        self._word = word
        self._shape = shape

    @property
    def position(self) -> Position:
        return self._position

    @property
    def word(self) -> str:
        return self._word

    @property
    def shape(self) -> Shape:
        return self._shape

    def __str__(self):
        return f"{self._word} at {self._position}: {self._shape}"
