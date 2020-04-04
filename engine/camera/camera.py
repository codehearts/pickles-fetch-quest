from pyglet import gl


class Camera(object):
    """Camera for controlling zoom and tracking game objects.

    Attributes:
        x (int): The x coordinate of the camera's lower left corner.
        y (int): The y coordinate of the camera's lower left corner.
    """

    def __init__(self, width, height):
        """Creates a new camera with the given dimensions.

        Args:
            width (int): The width of the camera.
            height (int): The height of the camera.
        """
        self._width = width
        self._height = height

        self._x = 0
        self._y = 0

        # Offset for the camera to be centered
        self._x_offset = width // 2
        self._y_offset = height // 2

        # Camera has no boundaries by default
        self._x_boundary = None
        self._y_boundary = None

    def set_boundary(self, width, height):
        """Sets a boundary for the camera's movement.

        The camera will be locked within (0, 0) and (width, height).
        Setting either axis' boundary to None will unlock that axis.

        Args:
            width (int): The x coordinate for the right edge of the boundary.
            height (int): The y coordinate for the upper edge of the boundary.
        """
        self._x_boundary = width - self._width
        self._y_boundary = height - self._height

    def look_at(self, x, y):
        """Positions the camera such that the given coordinates are centered.

        The coordinates may not be centered if the camera is at its boundary.

        Args:
            x (int): The x coordinate to center on.
            y (int): The y coordinate to center on.
        """
        self._x = self._apply_boundary(x - self._x_offset, self._x_boundary)
        self._y = self._apply_boundary(y - self._y_offset, self._y_boundary)

    def update(self, ms):
        """Updates the camera's position when following a target.

        Args:
            ms (int): Number of milliseconds since the last update.
        """
        pass

    def attach(self):
        """Applies camera transformations to subsequent draws.

        Calling :fn:`camera.Camera.detach` stops applying the transformations.
        """
        gl.glPushMatrix()
        gl.glTranslatef(-self._x, -self._y, 0)

    def detach(self):
        """Stops applying transformations set by :fn:`camera.Camera.attach`."""
        gl.glPopMatrix()

    def _apply_boundary(self, value, boundary):
        """Applies the camera boundaries to the given coordinate.

        Args:
            value (int): The coordinate to apply the boundary to.
            boundary (int or None): The boundary to restrict the coordinate to.

        Returns:
            An int of the coordinate within the boundary.
        """
        return value if boundary is None else max(min(boundary, value), 0)

    @property
    def x(self):
        """Returns the x coordinate of the camera's lower left corner."""
        return self._x

    @property
    def y(self):
        """Returns the y coordinate of the camera's lower left corner."""
        return self._y
