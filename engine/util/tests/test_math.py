from ..math import divide_toward_zero
import unittest


class TestMathUtils(unittest.TestCase):
    """Test math utility functions."""

    def test_zero_divide_towards_zero(self):
        """Dividing 0 rounds towards 0 during division."""
        self.assertEqual(0, divide_toward_zero(0, 2))

    def test_positives_divide_towards_zero(self):
        """Positives integers are rounded towards 0 during division."""
        self.assertEqual(0, divide_toward_zero(1, 2))
        self.assertEqual(1, divide_toward_zero(2, 2))

    def test_negatives_divide_towards_zero(self):
        """Negative integers are rounded towards 0 during division."""
        self.assertEqual(0, divide_toward_zero(-1, 2))
        self.assertEqual(-1, divide_toward_zero(-2, 2))
