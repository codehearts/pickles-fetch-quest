from ..rectangle import Rectangle
import unittest


class TestRectangle(unittest.TestCase):
    """Test properties of a Rectangle object."""

    def test_create_rectangle(self):
        """Creates a Rectangle object and verifies its attributes."""
        rect = Rectangle(1, 2, 3, 4)
        self.assertEqual(1, rect.x)
        self.assertEqual(2, rect.y)
        self.assertEqual(3, rect.width)
        self.assertEqual(4, rect.height)
        self.assertEqual((1, 2), rect.position)
