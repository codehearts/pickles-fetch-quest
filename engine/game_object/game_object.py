from ..event_dispatcher import EventDispatcher
from ..geometry import Point2d, Rectangle


class GameObject(Rectangle, EventDispatcher):
    """Game object with support for event dispatching.

    See :cls:`event_dispatcher.EventDispatcher` for usage information on the
    event dispatcher.

    Attributes:
        x (int): The x coordinate of the left edge of the object's geometry.
        y (int): The y coordinate of the bottom edge of the object's geometry.
        coordinates (:obj:`Point2d`): The coordinates for the bottom left edge
                                      of the object's geometry. Read-only.
        width (int): The width of the object's geometry.
        height (int): The height of the object's geometry.
        physics (:obj:`Physics2d`): Physics that the object obeys on update.

    Events:
        on_move: The x or y coordinates of the object's geometry have changed.
            A tuple of the x and y coordinates will be passed to the listeners.
        on_collision: The object's geometry overlapped with another object.
            The other object will be passed to the listeners.
    """

    def __init__(self, geometry_states, x, y, physics):
        """Creates a new event-driven game object.

        Args:
            geometry_states (dict of :obj:`str`: :obj:`geometry.Rectangle`):
                A mapping of state names to geometry objects. The 'default'
                state is required or a ``KeyError`` is raised.

                A possible valid ``geometry_states`` value would be::

                    {
                        'default': Rectangle(0, 0, 32, 32),
                        'active': Rectangle(10, 10, 64, 128)
                    }
            x (int): The x coordinate for the game object's bottom edge.
            y (int): The y coordinate for the game object's left edge.
            physics (:obj:`physics.Physics2d`): Physics for the object to obey
                when its `update` method is called.

        Raises:
            KeyError: If ``geometry_states`` was missing the 'default' state.
        """
        super(GameObject, self).__init__(x, y,
                                         geometry_states['default'].width,
                                         geometry_states['default'].height)
        self.register_event_type('on_collision')
        self.register_event_type('on_move')

        self._geometry_states = geometry_states
        self.physics = physics

        self.set_geometry_state('default')

    def set_position(self, coordinates):
        """Sets the x and y coordinates of the object at the same time.

        Args:
            coordinates (tuple of int): A tuple of the x and y coordinates.
        """
        if self._coordinates != coordinates:
            self._coordinates.set(coordinates)
            self.dispatch_event('on_move', (self.x, self.y))

    def notify_collision_with(self, other):
        """Dispatches an ``on_collision`` event with the other object.

        Args:
            other (:obj:`GameObject`): The object this one overlapped with.
        """
        self.dispatch_event('on_collision', other)

    def set_geometry_state(self, state_name):
        """Sets the geometry of the object to the state with the given name.

        Args:
            state_name (str): The name of the geometry state to switch to.
        """
        state = self._geometry_states[state_name]
        self.width = state.width
        self.height = state.height

    def update(self, ms):
        """Updates the position and state of the game object based on time.

        Args:
            ms (int): Number of milliseconds since the last update.
        """
        if self.physics is not None:
            self.physics.run_simulation(ms)
            self.set_position((self.x + self.physics.velocity.x,
                               self.y + self.physics.velocity.y))

    @property
    def coordinates(self):
        """Returns the coordinates of the object's bottom left edge.

        This property is read-only. Use ``set_position`` to set it.
        """
        return Point2d(self._coordinates.x, self._coordinates.y)

    @property
    def x(self):
        """Returns the x coordinate of the object's left edge."""
        return self._coordinates.x

    @x.setter
    def x(self, value):
        """Sets the x coordinate of the object and dispatches on_move."""
        if self._coordinates.x != value:
            self.set_position((value, self.y))

    @property
    def y(self):
        """Returns the y coordinate of the object's bottom edge."""
        return self._coordinates.y

    @y.setter
    def y(self, value):
        """Sets the y coordinate of the object and dispatches on_move."""
        if self._coordinates.y != value:
            self.set_position((self.x, value))
