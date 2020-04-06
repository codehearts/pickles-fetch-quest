from ..linear_curve import LinearCurve
import unittest


class TestLinearCurve(unittest.TestCase):
    """Test calculations for a linear easing curve."""

    def test_positive_linear_curve_value_updates_linearly(self):
        """A positive linear curve's value changes linearly in time."""
        # From 0 to 10 in 10 time units
        curve = LinearCurve(10, start=0, end=10)
        curve.update(5)  # 5 units elapsed

        self.assertEqual(5, curve.value)
        curve.update(5)  # 10 units elapsed

        self.assertEqual(10, curve.value)

    def test_negative_linear_curve_value_updates_linearly(self):
        """A negative linear curve's value changes linearly in time."""
        # From 10 to 0 in 10 time units
        curve = LinearCurve(10, start=10, end=0)
        curve.update(5)  # 5 units elapsed

        self.assertEqual(5, curve.value)
        curve.update(5)  # 10 units elapsed

        self.assertEqual(0, curve.value)

    def test_linear_curve_does_not_update_after_duration(self):
        """A linear curve's value doesn't change after the duration."""
        # From 0 to 10 in 10 time units
        curve = LinearCurve(10, start=0, end=10)
        curve.update(10)  # 10 units elapsed

        self.assertEqual(10, curve.value)
        curve.update(5)  # 15 units elapsed

        self.assertEqual(10, curve.value)

    def test_linear_curve_is_done_once_duration_elapses(self):
        """A linear curve is done once its duration has expired."""
        curve = LinearCurve(10, start=0, end=10)

        curve.update(9)  # 9 units elapsed
        self.assertFalse(curve.is_done())

        curve.update(1)  # 10 units elapsed (duration met)
        self.assertTrue(curve.is_done(), "duration met")

        curve.update(1)  # 11 units elapsed (duration exceeded)
        self.assertTrue(curve.is_done(), "duration exceeded")
