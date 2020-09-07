from ..easing_curve import EasingCurve
import unittest


class TestEasingCurve(unittest.TestCase):
    """Test functionality of the base easing curve."""

    def test_initial_curve_value_is_starting_value(self):
        """An easing curve's initial value is its starting value."""
        curve = EasingCurve(123, 456)

        self.assertEqual(123, curve.value)

    def test_base_easing_curve_does_nothing_on_update(self):
        """The base easing curve does nothing on update."""
        curve = EasingCurve(123, 456)
        curve.update(789)

        self.assertEqual(123, curve.value)

    def test_easing_curve_value_is_read_only(self):
        """The value of an easing curve is read only."""
        curve = EasingCurve(0, 10)

        with self.assertRaises(AttributeError, msg='can\'t set attribute'):
            curve.value = 1
