import re

from letter import Letter

INPUT_PATTERN = r"^[A-Z*]{1,7}$"


class PlayerTiles:
    def __init__(self, raw_tiles: str):
        # Validate.
        tiles = raw_tiles.upper().replace(" ", "").strip()
        if not re.match(INPUT_PATTERN, tiles):
            raise ValueError(f"Invalid tiles: {tiles}")

        # Processing
        self._letters: list[Letter] = []
        self._num_wildcards = 0
        for tile in tiles:
            if tile == "*":
                self._num_wildcards += 1
            else:
                self._letters.append(Letter(tile))
        self._letters.sort()

    def __str__(self) -> str:
        output = "\nTiles: "
        chars = [letter.val for letter in self._letters] + ["*"] * self._num_wildcards
        for index, char in enumerate(chars):
            output += f"'{char}'"
            if index != len(chars) - 1:
                output += ", "
        return output

    @property
    def letters(self) -> list[Letter]:
        return self._letters

    @property
    def num_wildcards(self) -> int:
        return self._num_wildcards
