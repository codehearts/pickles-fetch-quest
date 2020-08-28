from engine.geometry import Rectangle, Point2d
from pyglet import gl


class Camera(Rectangle):
    """Camera for controlling zoom and tracking game objects.

    Attributes:
        x (int): The x coordinate of the camera's lower left corner.
        y (int): The y coordinate of the camera's lower left corner.
        coordinates (:obj:`engine.geometry.Point2d`):
            The coordinates of the lower left corner as a :obj:`Point2d`.
        width (int): The width of the camera.
        height (int): The height of the camera.
        scale (float): The scaling to apply to the visible scene.
        follow (:obj:`game_object.GameObject` or None):
            A target for the camera to follow, or None for manual control.
        follow_easing (:obj:`easing.EasingCurve` or None):
            An easing curve to apply when following a target
        follow_lead (:obj:`geometry.Point2d` or None):
            Pixels for the camera to lead by when following a target in motion.
    """

    def __init__(self, width, height):
        """Creates a new camera with the given dimensions.

        Args:
            width (int): The width of the camera.
            height (int): The height of the camera.
        """
        super(Camera, self).__init__(0, 0, width, height)

        # Scale of the visible scene
        self.scale = 1

        # Object tracking
        self.follow = None
        self.follow_easing = None
        self.follow_lead = Point2d(0, 0)

        # Boundary to restrict the camera to
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
        self._x_boundary = width - self.width
        self._y_boundary = height - self.height

    def look_at(self, x, y):
        """Positions the camera such that the given coordinates are centered.

        The coordinates may not be centered if the camera is at its boundary.

        Args:
            x (int): The x coordinate to center on.
            y (int): The y coordinate to center on.
        """
        self.x = self._apply_boundary(x - self.width // 2, self._x_boundary)
        self.y = self._apply_boundary(y - self.height // 2, self._y_boundary)

    def update(self, ms):
        """Updates the camera's position when following a target.

        Args:
            ms (int): Number of milliseconds since the last update.
        """
        if self.follow is not None:
            if self.follow_easing is not None:
                follow_direction = self._get_follow_direction()

                if follow_direction == (0, 0):
                    # Object is at rest, focus on its center if not already
                    if self.follow_easing.end != self.follow.center:
                        self.follow_easing.reset(self.center, self.follow.center)
                else:
                    # Object is moving, update curve to follow with lead space
                    with_lead = self.follow.center + self.follow_lead * follow_direction
                    self.follow_easing.reset(self.center, with_lead)

                self.follow_easing.update(ms)
                self.look_at(*self.follow_easing.value)
            else:
                self.look_at(*self.follow.center)

    def attach(self):
        """Applies camera transformations to subsequent draws.

        Calling :fn:`camera.Camera.detach` stops applying the transformations.
        """
        gl.glPushMatrix()
        gl.glScalef(self.scale, self.scale, 0)
        gl.glTranslatef(-self.x, -self.y, 0)

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

    def _get_follow_direction(self):
        """Returns the directional vector of the followed target.

        Returns:
            A :obj:`geometry.Point2d` of the directional vector, such as
            `(-1, 1)` for an object moving left and up, or `(0, 0)` for an
            object at rest.
        """
        if self.follow.physics is None:
            return Point2d(0, 0)

        velocity = self.follow.physics.velocity
        return Point2d(min(1, max(-1, velocity.x)), min(1, max(-1, velocity.y)))
