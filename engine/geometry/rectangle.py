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

    def __init__(self, x, y, width, height, *args, **kwargs):
        """Creates a new rectangle.

        Args:
            x (int): The x coordinate for the left edge of the rectangle.
            y (int): The y coordinate for the bottom edge of the rectangle.
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
        """
        super(Rectangle, self).__init__(*args, **kwargs)
        self._coordinates = Point2d(x, y)
        self.width = width
        self.height = height

    def move_by(self, relative_positions):
        """Moves the rectangle by the given relative x and y positions.

        Args:
            relative_positions (tuple of int):
                The amount to increase the x and y positions by.
        """
        self._coordinates += relative_positions

    def set_position(self, coordinates):
        """Sets the x and y coordinates of the rectangle at the same time.

        Args:
            coordinates (tuple of int): A tuple of the x and y coordinates.
        """
        self._coordinates.set(coordinates)

    @property
    def coordinates(self):
        """Returns the coordinates of the rectangle."""
        return self._coordinates

    @property
    def center(self):
        """Returns the coordinates of the center of the rectangle."""
        return self.coordinates + (self.width // 2, self.height // 2)

    @property
    def x(self):
        """Returns the x coordinate of rectangle."""
        return self._coordinates.x

    @property
    def y(self):
        """Returns the y coordinate of rectangle."""
        return self._coordinates.y

    @x.setter
    def x(self, x):
        """Sets the x coordinate of rectangle."""
        self._coordinates.x = x

    @y.setter
    def y(self, y):
        """Sets the y coordinate of rectangle."""
        self._coordinates.y = y
