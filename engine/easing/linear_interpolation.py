from .easing_curve import EasingCurve


class LinearInterpolation(EasingCurve):
    """An easing transition using linear interpolation.

    Attributes:
        value (int): The current value of the easing curve.
    """

    def __init__(self, factor, start=0, end=0):
        """Creates a new linear interpolation curve.

        Args:
            factor (float): The interpolation factor to use.
                            Values closer to 1 are more instantaneous.

        Kwargs:
            start (int, optional): The starting value of the curve.
            end (int, optional): The ending value of the curve.
        """
        self._factor = int(factor * 100)
        self._precision_value = 0
        super(LinearInterpolation, self).__init__(start, end)

    def _calculate_value(self):
        """Uses linear interpolation to calculate the current value.

        Returns:
            An int representing the curve's current value.
        """
        # Reset the high resolution value if it no longer matches the int value
        if self._value != self._precision_value // 100:
            self._precision_value = self._value * 100

        # Calculate the current value with 2 decimal places of precision
        start = self._precision_value
        end = self.end * 100
        value = (start * (100 - self._factor) + end * self._factor) // 100

        # Round the value to 1 decimal point of precision
        self._precision_value = round(value, -1)

        # Return the integer value of the high resolution value
        return self._precision_value // 100
