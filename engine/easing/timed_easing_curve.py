from .easing_curve import EasingCurve


class TimedEasingCurve(EasingCurve):
    """Representation for an easing curve with a duration.

    Attributes:
        start (int): The starting value of the easing curve.
        end (int): The ending value of the easing curve.
        value (int): The current value of the easing curve.
        duration (int): The duration of the easing curve in ms.
    """

    def __init__(self, duration, start=0, end=0):
        """Creates a new timed easing curve.

        Args:
            duration (int): The total milliseconds to transition for.

        Kwargs:
            start (int, optional): The starting value of the curve.
            end (int, optional): The ending value of the curve.
        """
        super(TimedEasingCurve, self).__init__(start, end)
        self.reset(start, end, duration)

    def update(self, ms):
        """Updates the easing curve to reflect the current position in time.

        Args:
            ms (int): Number of milliseconds since the last update.
        """
        # Ensure the elapsed time does not exceed the duration
        self._elapsed_time = min(self.duration, self._elapsed_time + ms)

        super(TimedEasingCurve, self).update(ms)

    def reset(self, start, end, duration=None):
        """Resets the curve, essentially creating a new curve.

        Args:
            start (int): The new starting value of the curve.
            end (int): The new ending value of the curve.

        Kwargs:
            duration (int, optional): An optional new duration for the curve.
        """
        super(TimedEasingCurve, self).reset(start, end)

        self._elapsed_time = 0

        if duration is not None:
            self.duration = duration
