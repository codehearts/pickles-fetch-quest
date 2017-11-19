from ..point_2d import Point2d
import unittest


class TestPoint2d(unittest.TestCase):
    """Test properties and manipulation of 2d point."""

    def test_create_point(self):
        """Creates a point and verifies its attributes."""
        point = Point2d(1, 2)
        self.assertEqual(1, point.x)
        self.assertEqual(2, point.y)

    def test_point_setters(self):
        """Setting x or y updates attributes."""
        point = Point2d(0, 0)
        point.x = 1
        point.y = 2
        self.assertEqual(1, point.x)
        self.assertEqual(2, point.y)

    def test_point_scalar_equality(self):
        """Point is equal to scalar when both coordinates are equal to it."""
        equal_point = Point2d(0, 0)
        self.assertEqual(0, equal_point)
        self.assertNotEqual(1, equal_point)

        inequal_point = Point2d(1, 2)
        self.assertNotEqual(1, inequal_point)
        self.assertNotEqual(2, inequal_point)

    def test_point_vector_equality(self):
        """Point is equal to vector if coordinates are equal to its indices."""
        point = Point2d(1, 2)
        self.assertEqual((1, 2), point)
        self.assertNotEqual((1, 1), point)
        self.assertNotEqual((2, 2), point)
        self.assertNotEqual((0, 0), point)

    def test_point_equality(self):
        """Point is equal to another point when both coordinates are equal."""
        point = Point2d(1, 2)
        self.assertEqual(Point2d(1, 2), point)
        self.assertNotEqual(Point2d(1, 1), point)
        self.assertNotEqual(Point2d(2, 2), point)
        self.assertNotEqual(Point2d(0, 0), point)

    def test_point_scalar_addition(self):
        """Adding scalar to point updates both coordinates."""
        point = Point2d(0, 0)

        # __add__ should not affect the value of point
        point2 = point + 2

        point += 2
        self.assertEqual(2, point.x)
        self.assertEqual(2, point.y)
        self.assertEqual(2, point2.x)
        self.assertEqual(2, point2.y)

    def test_point_vector_addition(self):
        """Adding vector to point updates both coordinates."""
        point = Point2d(0, 0)

        # __add__ should not affect the value of point
        point2 = point + (1, 2)

        point += (1, 2)
        self.assertEqual(1, point.x)
        self.assertEqual(2, point.y)
        self.assertEqual(1, point2.x)
        self.assertEqual(2, point2.y)

    def test_point_addition(self):
        """Adding point to point updates both coordinates."""
        point = Point2d(0, 0)

        # __add__ should not affect the value of point
        point2 = point + Point2d(1, 2)

        point += Point2d(1, 2)
        self.assertEqual(1, point.x)
        self.assertEqual(2, point.y)
        self.assertEqual(1, point2.x)
        self.assertEqual(2, point2.y)

    def test_point_scalar_multiplication(self):
        """Multiplying point by scalar updates both coordinates."""
        point = Point2d(1, 2)

        # __mul__ should not affect the value of point
        point2 = point * 2

        point *= 2
        self.assertEqual(2, point.x)
        self.assertEqual(4, point.y)
        self.assertEqual(2, point2.x)
        self.assertEqual(4, point2.y)

    def test_point_vector_multiplication(self):
        """Multiplying point by vector updates both coordinates."""
        point = Point2d(1, 2)

        # __mul__ should not affect the value of point
        point2 = point * (2, 3)

        point *= (2, 3)
        self.assertEqual(2, point.x)
        self.assertEqual(6, point.y)
        self.assertEqual(2, point2.x)
        self.assertEqual(6, point2.y)

    def test_point_multiplication(self):
        """Multiplying point by point updates both coordinates."""
        point = Point2d(1, 2)

        # __mul__ should not affect the value of point
        point2 = point * Point2d(2, 3)

        point *= Point2d(2, 3)
        self.assertEqual(2, point.x)
        self.assertEqual(6, point.y)
        self.assertEqual(2, point2.x)
        self.assertEqual(6, point2.y)

    def test_point_scalar_floor_division(self):
        """Floor dividing point by scalar updates both coordinates."""
        point = Point2d(2, 5)

        # __div__ should not affect the value of point
        point2 = point // 2

        point //= 2
        self.assertEqual(1, point.x)
        self.assertEqual(2, point.y)
        self.assertEqual(1, point2.x)
        self.assertEqual(2, point2.y)

    def test_point_vector_floor_division(self):
        """Floor dividing point by vector updates both coordinates."""
        point = Point2d(6, 7)

        # __div__ should not affect the value of point
        point2 = point // (2, 3)

        point //= (2, 3)
        self.assertEqual(3, point.x)
        self.assertEqual(2, point.y)
        self.assertEqual(3, point2.x)
        self.assertEqual(2, point2.y)

    def test_point_floor_division(self):
        """Floor dividing point by point updates both coordinates."""
        point = Point2d(6, 7)

        # __div__ should not affect the value of point
        point2 = point // Point2d(2, 3)

        point //= Point2d(2, 3)
        self.assertEqual(3, point.x)
        self.assertEqual(2, point.y)
        self.assertEqual(3, point2.x)
        self.assertEqual(2, point2.y)
