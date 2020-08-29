from engine.geometry import Rectangle, Point2d, detect_overlap_1d
from pyglet import gl


class Camera(Rectangle):
    """Camera for controlling zoom and tracking game objects.

    When following a target, the camera can be provided an easing function,
    lead spacing, and a deadzone to fine-tune the tracking. This is based on
    the `STALKER-X <https://github.com/a327ex/STALKER-X>`_ camera for the
    `LÖVE <https://love2d.org>`_ Lua framework.

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
        follow_lead (:obj:`geometry.Point2d`):
            Pixels for the camera to lead by when following a target in motion.
        follow_deadzone (:obj:`geometry.Rectangle`):
            Rectangular deadzone relative to the bottom left corner in which
            the camera won't follow the target.
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
        self._follow_deadzone = Rectangle(0, 0, 0, 0)
        self._apply_deadzone = [False, False]  # Internal for smooth following

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
        # There is nothing to update if nothing is being followed
        if self.follow is None:
            return

        # If there is no easing, track the object directly
        if self.follow_easing is None:
            self.look_at(*self.follow.center)
            return

        # Target movement vector and center (with respect to deadzone)
        target_vector = self._get_follow_vector()
        target_center = Point2d(
            self._center_with_deadzone(self.follow, target_vector, 'x'),
            self._center_with_deadzone(self.follow, target_vector, 'y'))

        if target_vector != (0, 0):
            # Target is moving, update the curve to follow it with lead
            self.follow_easing.reset(
                self.center, self._apply_lead(target_center, target_vector))
        elif self.follow_easing.end != target_center:
            # Target is not moving and curve is out of date, reset to center
            self.follow_easing.reset(self.center, target_center)

        self.follow_easing.update(ms)
        self.look_at(*self.follow_easing.value)

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

    def _get_follow_vector(self):
        """Returns the directional vector of the followed target.

        Returns:
            A :obj:`geometry.Point2d` of the directional vector, such as
            `(-1, 1)` for an object moving left and up, or `(0, 0)` for an
            object at rest.
        """
        if self.follow.physics is None:
            return Point2d(0, 0)

        velocity = self.follow.physics.velocity
        return Point2d(
            min(1, max(-1, velocity.x)),
            min(1, max(-1, velocity.y)))

    def _apply_lead(self, target_center, target_vector):
        """Applies lead distance to the given coordinates.

        Args:
            target_center (:obj:`geometry.Point2d`):
                Center coordinates of the target to apply lead to.
            target_vector (:obj:`geometry.Point2d`):
                Vector of the target's movement.
        """
        lead = self.follow_lead * target_vector

        # Do not apply lead if the deadzone applies to the axis
        if self._apply_deadzone[0]:
            lead.x = 0
        if self._apply_deadzone[1]:
            lead.y = 0

        return target_center + lead

    def _center_with_deadzone(self, target, target_vector, axis):
        """Centers on a target with respect to the camera's deadzone.

        This avoids moving the camera when an target is within the deadzone
        and has not left it.

        Args:
            target (:obj:`game_object.GameObject`):
                Target to center on with respect to the deadzone.
            target_vector (:obj:`geometry.Point2d`):
                Vector of the target's movement.
            axis (str): Axis to center along, either 'x' or 'y'.

        Returns:
            An int of the coordinate bounded by the deadzone along the axis.
        """
        axis_int = 0 if axis == 'x' else 1
        dimension = ('width', 'height')[axis_int]

        within_deadzone = detect_overlap_1d(
            getattr(self, axis) + getattr(self._follow_deadzone, axis),
            getattr(self._follow_deadzone, dimension),
            getattr(target, axis),
            getattr(target, dimension))

        if not within_deadzone:
            # Stop applying deadzone if target has moved outside
            self._apply_deadzone[axis_int] = False
        elif target_vector[axis_int] == 0:
            # Apply deadzone when object is at rest within it
            self._apply_deadzone[axis_int] = True

        # Don't move the camera along the axis if the deadzone applies
        if self._apply_deadzone[axis_int]:
            return self.center[axis_int]

        return target.center[axis_int]

    @property
    def follow_deadzone(self):
        """Returns the deadzone for the followed target."""
        return self._follow_deadzone

    @follow_deadzone.setter
    def follow_deadzone(self, deadzone):
        """Sets the follow deadzone."""
        self._follow_deadzone = deadzone
        self._apply_deadzone = [True, True]
