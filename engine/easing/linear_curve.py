from .timed_easing_curve import TimedEasingCurve


class LinearCurve(TimedEasingCurve):
    """An easing transition which moves at a constant rate.

    Attributes:
        value (int): The current value of the easing curve.
    """

    def __init__(self, duration, start=0, end=0):
        """Creates a new linear easing curve.

        Args:
            duration (int): The total milliseconds to transition for.

        Kwargs:
            start (int, optional): The starting value of the curve.
            end (int, optional): The ending value of the curve.
        """
        super(LinearCurve, self).__init__(duration, start, end)

    def _calculate_value(self):
        """Uses a linear equation to calculate the current value.

        Returns:
            An int representing the curve's value at the current time.
        """
        return self.start + self._delta * self._elapsed_time // self.duration
