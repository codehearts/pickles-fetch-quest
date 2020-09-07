class EasingCurve(object):
    """Representation for an easing curve.

    Attributes:
        start (int): The starting value of the easing curve.
        end (int): The ending value of the easing curve.
        value (int): The current value of the easing curve.
    """

    def __init__(self, start=0, end=0):
        """Creates a new easing curve.

        Kwargs:
            start (int, optional): The starting value of the curve.
            end (int, optional): The ending value of the curve.
        """
        self.reset(start, end)

    def _calculate_value(self):
        """Method for base classes to override with their easing equations.

        Returns:
            An int representing the easing curve's value at the current time.
        """
        return self._value

    def update(self, ms):
        """Updates the easing curve to reflect the current position in time.

        Args:
            ms (int): Number of milliseconds since the last update.
        """
        if not self.is_done():
            self._value = self._calculate_value()

    def reset(self, start, end):
        """Resets the curve, essentially creating a new curve.

        Args:
            start (int): The new starting value of the curve.
            end (int): The new ending value of the curve.
        """
        self.start = start
        self.end = end
        self._delta = end - start
        self._value = start

    def is_done(self):
        """Returns true if the easing curve is done."""
        return self._value == self.end

    @property
    def value(self):
        """Returns the current value of the easing curve."""
        return self._value
