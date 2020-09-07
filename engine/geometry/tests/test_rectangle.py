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
        self.assertEqual(1, rect.coordinates.x)
        self.assertEqual(2, rect.coordinates.y)

    def test_rectangle_center(self):
        """The center of a Rectangle is provided as a property."""
        rect = Rectangle(0, 0, 10, 20)
        self.assertEqual(5, rect.center.x)
        self.assertEqual(10, rect.center.y)

    def test_rectangle_can_be_positioned_by_x_and_y_values(self):
        """A Rectangle can be repositioned using its x and y attributes."""
        rect = Rectangle(1, 2, 3, 4)
        self.assertEqual(1, rect.x)
        self.assertEqual(2, rect.y)
        self.assertEqual(1, rect.coordinates.x)
        self.assertEqual(2, rect.coordinates.y)

        rect.x = 10
        rect.y = 20
        self.assertEqual(10, rect.x)
        self.assertEqual(20, rect.y)
        self.assertEqual(10, rect.coordinates.x)
        self.assertEqual(20, rect.coordinates.y)

    def test_rectangle_can_be_positioned_using_coordinates(self):
        """A Rectangle can be positioned with a single set of coordinates."""
        rect = Rectangle(1, 2, 3, 4)
        rect.set_position((10, 20))

        self.assertEqual(10, rect.x)
        self.assertEqual(20, rect.y)
        self.assertEqual(10, rect.coordinates.x)
        self.assertEqual(20, rect.coordinates.y)

    def test_rectangle_can_be_positioned_relatively(self):
        """A Rectangle can be repositioned using a relative position."""
        rect = Rectangle(1, 2, 3, 4)
        rect.move_by((10, 20))

        self.assertEqual(11, rect.x)
        self.assertEqual(22, rect.y)
        self.assertEqual(11, rect.coordinates.x)
        self.assertEqual(22, rect.coordinates.y)
