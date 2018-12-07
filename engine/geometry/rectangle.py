from .point_2d import Point2d


class Rectangle(object):
    """Two-dimensional rectangle anchored to its lower left corner.

    Attributes:
        x (int): The x coordinate of the left edge of the rectangle.
        y (int): The y coordinate of the bottom edge of the rectangle.
        coordinates (:obj:`engine.geometry.Point2d`):
            The coordinates as a :obj:`Point2d`.
        width (int): The width of the rectangle.
        height (int): The height of the rectangle.
    """

    def __init__(self, x, y, width, height):
        """Creates a new rectangle.

        Args:
            x (int): The x coordinate for the left edge of the rectangle.
            y (int): The y coordinate for the bottom edge of the rectangle.
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
        """
        super(Rectangle, self).__init__()
        self._coordinates = Point2d(x, y)
        self.width = width
        self.height = height

    @property
    def coordinates(self):
        """Returns the coordinates of the rectangle."""
        return self._coordinates

    @property
    def x(self):
        """Returns the x coordinate of rectangle."""
        return self._coordinates.x

    @property
    def y(self):
        """Returns the y coordinate of rectangle."""
        return self._coordinates.y
