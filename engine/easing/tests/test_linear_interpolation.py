from ..linear_interpolation import LinearInterpolation
import unittest


class TestLinearInterpolation(unittest.TestCase):
    """Test calculations for linear interpolation."""

    def test_positive_linear_interpolation_with_factor_of_three_fourths(self):
        """Positive linear interpolations approach end with factor of 0.75."""
        curve = LinearInterpolation(0.75, start=0, end=10)
        self.assertEqual(0, curve.value)

        curve.update(0)  # Time does not matter for linear interpolation
        self.assertEqual(7, curve.value)

        curve.update(0)  # 9.38
        curve.update(0)  # 9.84
        self.assertEqual(9, curve.value)

        curve.update(0)
        self.assertEqual(10, curve.value)

    def test_positive_linear_interpolation_with_factor_of_1(self):
        """Positive linear interpolations change instantly with factor of 1."""
        curve = LinearInterpolation(1.0, start=0, end=10)
        self.assertEqual(0, curve.value)

        curve.update(0)  # Time does not matter for linear interpolation
        self.assertEqual(10, curve.value)

    def test_negative_linear_interpolation_with_factor_of_three_fourths(self):
        """Negative linear interpolations approach end with factor of 0.75."""
        curve = LinearInterpolation(0.75, start=10, end=0)
        self.assertEqual(10, curve.value)

        curve.update(0)  # Time does not matter for linear interpolation
        self.assertEqual(2, curve.value)

        curve.update(0)  # 0.64
        self.assertEqual(0, curve.value)

    def test_negative_linear_interpolation_with_factor_of_1(self):
        """Negative linear interpolations change instantly with factor of 1."""
        curve = LinearInterpolation(1.0, start=10, end=0)
        self.assertEqual(10, curve.value)

        curve.update(0)  # Time does not matter for linear interpolation
        self.assertEqual(0, curve.value)

    def test_linear_interpolation_does_not_exceed_its_end(self):
        """Linear interpolation does not exceed its end value."""
        curve = LinearInterpolation(1.0, start=0, end=10)
        curve.update(0)
        self.assertEqual(10, curve.value)

        curve.update(0)  # Updating will not move past the endpoint
        self.assertEqual(10, curve.value)

    def test_linear_interpolation_is_done_once_endpoint_is_reached(self):
        """Linear interpolation is done once its end is reached."""
        curve = LinearInterpolation(1.0, start=0, end=10)
        self.assertFalse(curve.is_done())

        curve.update(0)
        self.assertTrue(curve.is_done())
