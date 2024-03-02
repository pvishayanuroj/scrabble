from enums import Shape, TurnStateValue


class TurnState:
    """A state machine for taking a turn."""

    def __init__(self):
        self._state = TurnStateValue.NO_PLACEMENTS
        self._shape = Shape.UNSPECIFIED_SHAPE
        self._cross_shape = Shape.UNSPECIFIED_SHAPE

    @property
    def state(self) -> TurnStateValue:
        return self._state

    @property
    def shape(self) -> Shape:
        return self._shape
    
    @property
    def cross_shape(self) -> Shape:
        return self._cross_shape
    
    def first_placement(self):
        """The first tile was placed."""
        if self._state != TurnStateValue.NO_PLACEMENTS:
            raise RuntimeError(f"Cannot change state from {self._state} to first placement state.")
        self._state = TurnStateValue.FIRST_PLACEMENT

    def second_placement(self, shape: Shape):
        """The second tile was placed."""
        if self._state != TurnStateValue.FIRST_PLACEMENT:
            raise RuntimeError(f"Cannot change state from {self._state} to mid-turn state.")
        if shape != Shape.VERTICAL and shape != Shape.HORIZONTAL:
            raise RuntimeError(f"Invalid shape: {shape}.")
        self._state = TurnStateValue.MID_TURN
        self._shape = shape
        self._cross_shape = Shape.HORIZONTAL if shape == Shape.VERTICAL else Shape.VERTICAL