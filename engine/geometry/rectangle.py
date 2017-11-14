class Rectangle(object):
    """Two-dimensional rectangle anchored to its lower left corner.

    Attributes:
        x (int): The x coordinate of the left edge of the rectangle.
        y (int): The y coordinate of the bottom edge of the rectangle.
        width (int): The width of the rectangle.
        height (int): The height of the rectangle.
        position (tuple of int): The (x, y) coordinates of the rectangle.
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
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def position(self):
        """Returns the x, y coordinates as a tuple."""
        return (self.x, self.y)
