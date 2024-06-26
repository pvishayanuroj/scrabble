from __future__ import annotations
import re
from typing import Optional

from constants import PLAYER_TILES_PATTERN
from letter import Letter


class PlayerTiles:
    def __init__(self, raw_tiles: str):
        # Validate.
        tiles = raw_tiles.upper().replace(" ", "").strip()
        if not re.match(PLAYER_TILES_PATTERN, tiles):
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

    @classmethod
    def from_input(cls) -> Optional[PlayerTiles]:
        while True:
            user_input = input("\nEnter tiles ('*' for wildcard): ")
            try:
                player_tiles = cls(user_input)
                break
            except KeyboardInterrupt:
                print("Exiting.")
                return None
            except ValueError as e:
                print("Invalid input")
        print(player_tiles)
        return player_tiles
