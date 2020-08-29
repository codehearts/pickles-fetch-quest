from ..timed_easing_curve import TimedEasingCurve
import unittest


class TestTimedEasingCurve(unittest.TestCase):
    """Test functionality of the base timed easing curve."""

    def test_initial_timed_curve_value_is_starting_value(self):
        """A timed easing curve's initial value is its starting value."""
        curve = TimedEasingCurve(123, start=456, end=789)

        self.assertEqual(456, curve.value)

    def test_timed_easing_curve_value_is_read_only(self):
        """The value of a timed easing curve is read only."""
        curve = TimedEasingCurve(10, start=0, end=10)

        with self.assertRaises(AttributeError, msg='can\'t set attribute'):
            curve.value = 1
