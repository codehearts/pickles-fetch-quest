from ..event_dispatcher import EventDispatcher
from engine.geometry import Point2d, Rectangle


class GameObject(EventDispatcher, Rectangle):
    """Game object with support for event dispatching.

    See :cls:`event_dispatcher.EventDispatcher` for usage information on the
    event dispatcher.

    Attributes:
        x (int): The x coordinate of the left edge of the object.
        y (int): The y coordinate of the bottom edge of the object.
        width (int): The width of the object.
        height (int): The height of the object.

    Events:
        on_move: The x or y coordinates of the object have changed.
            A tuple of the x and y coordinates will be passed to the listeners.
        on_move_relative: The x or y coordinates of the object have changed.
            A tuple of the x and y deltas will be passed to the listeners.
        on_collider_enter: The object's collider has entered a collision with
            another object. The other object will be passed to the listeners.
        on_collider_exit: The object's collider has exited a collision with
            another object. The other object will be passed to the listeners.
        on_trigger_enter: The object's trigger overlapped with another object.
            The other object will be passed to the listeners.
        on_trigger_leave: The object's trigger no longer overlaps with the
            other object. The other object will be passed to the listeners.
    """

    def __init__(self, x, y, width, height, **kwargs):
        """Creates a new event-driven game object.

        Args:
            x (int): The x coordinate of the left edge of the object.
            y (int): The y coordinate of the bottom edge of the object.
            width (int): The width of the object.
            height (int): The height of the object.
        """
        super(GameObject, self).__init__(x, y, width, height, **kwargs)
        self.register_event_type('on_collider_enter')
        self.register_event_type('on_collider_exit')
        self.register_event_type('on_trigger_enter')
        self.register_event_type('on_trigger_exit')
        self.register_event_type('on_move_relative')
        self.register_event_type('on_move')

    def attach(self, attachment, offset_coordinates):
        """Attaches an object to this one, updating its position upon movement.

        The attachment will have its position changed as part of this call.

        Args:
            attachment (:obj:`geometry.Rectangle`):
                The object to attach.
            offset_coordinates (tuple of int):
                The x and y offset from the bottom left corner of this object.
        """
        # Move the attachment into place
        attachment.set_position(self._coordinates + offset_coordinates)

        # Move the attachment when this object moves
        self.add_listeners(on_move_relative=attachment.move_by)

    def move_by(self, relative_positions):
        """Moves this object by the given relative x and y positions.

        Args:
            relative_positions (tuple of int):
                The amount to increase the x and y coordinates by.
        """
        self.set_position(self._coordinates + relative_positions)

    def set_position(self, coordinates):
        """Sets the x and y coordinates of the object at the same time.

        Args:
            coordinates (tuple of int): A tuple of the x and y coordinates.
        """
        if self._coordinates != coordinates:
            # ``coordinates`` is a tuple, so it must be on the righthand side
            coordinate_delta = (self._coordinates - coordinates) * -1

            self._coordinates.set(coordinates)

            self.dispatch_event('on_move_relative', coordinate_delta)
            self.dispatch_event('on_move', (self.x, self.y))

    def update(self, ms):
        """Updates the game object based on time.

        This is currently a noop.

        Args:
            ms (int): Number of milliseconds since the last update.
        """
        pass

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
        """Set the x coordinate and dispatch on_move and on_move_relative."""
        if self._coordinates.x != value:
            self.set_position((value, self.y))

    @property
    def y(self):
        """Returns the y coordinate of the object's bottom edge."""
        return self._coordinates.y

    @y.setter
    def y(self, value):
        """Set the y coordinate and dispatch on_move and on_move_relative."""
        if self._coordinates.y != value:
            self.set_position((self.x, value))
