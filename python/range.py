from position import Position


class Range:
    """Describes a straight line with start and end coordinates."""
    def __init__(self, start: Position, end: Position):
        self._start = start
        self._end = end

    def __str__(self):
        return f"First: {self._start}, Last: {self._end}" 

    @property
    def start(self) -> Position:
        return self._start
    
    @property
    def end(self) -> Position:
        return self._end