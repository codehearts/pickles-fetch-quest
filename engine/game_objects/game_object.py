from ..event_dispatcher import EventDispatcher


class GameObject(EventDispatcher):
    """Game object with support for event dispatching.

    See :cls:`event_dispatcher.EventDispatcher` for usage information on the
    event dispatcher.

    Attributes:
        x (int): The x coordinate of the left edge of the object's geometry.
        y (int): The y coordinate of the bottom edge of the object's geometry.
        width (int): The width of the object's geometry.
        height (int): The height of the object's geometry.

    Events:
        on_move: The x or y coordinates of the object's geometry have changed.
            A tuple of the x and y coordinates will be passed to the listeners.
    """

    def __init__(self, geometry_states, x=0, y=0):
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
            x (int, optional): The x coordinate for the game object's bottom
                edge. Defaults to 0.
            y (int, optional): The y coordinate for the game object's left
                edge. Defaults to 0.

        Raises:
            KeyError: If ``geometry_states`` was missing the 'default' state.
        """
        super(GameObject, self).__init__()
        self.register_event_type('on_move')

        self._geometry_states = geometry_states
        self._geometry = geometry_states['default']
        self._x = x
        self._y = y

    def set_position(self, coordinates):
        """Sets the x and y coordinates of the object at the same time.

        Args:
            coordinates (tuple of int): A tuple of the x and y coordinates.
        """
        if self._x != coordinates[0] or self._y != coordinates[1]:
            self._x = coordinates[0]
            self._y = coordinates[1]
            self.dispatch_event('on_move', (self.x, self.y))

    @property
    def x(self):
        """Returns the x coordinate of the object's left edge."""
        return self._x

    @x.setter
    def x(self, value):
        """Sets the x coordinate of the object and dispatches on_move."""
        if self._x != value:
            self._x = value
            self.dispatch_event('on_move', (self.x, self.y))

    @property
    def y(self):
        """Returns the y coordinate of the object's bottom edge."""
        return self._y

    @y.setter
    def y(self, value):
        """Sets the y coordinate of the object and dispatches on_move."""
        if self._y != value:
            self._y = value
            self.dispatch_event('on_move', (self.x, self.y))

    @property
    def width(self):
        """Returns the width of the object's geometry."""
        return self._geometry.width

    @property
    def height(self):
        """Returns the height of the object's geometry."""
        return self._geometry.height