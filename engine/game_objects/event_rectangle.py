from .rectangle import Rectangle


class EventRectangle(Rectangle):
    """Two-dimensional rectangle which fires events when attributes change.

    This class takes a callable event handler which is expected to take an
    event string as its first argument and the rectangle object as its second.

    Possible event string values are::

        position_changed: Occurs when the position of the rectangle changes.
        size_changed: Occurs when the size of the rectangle changes.

    See :obj:`Rectangle` for additional attributes.

    Attributes:
        x (int): The x coordinate of the left edge of the rectangle.
        y (int): The y coordinate of the bottom edge of the rectangle.
        width (int): The width of the rectangle.
        height (int): The height of the rectangle.
        POSITION_CHANGED_EVENT (:obj:`str`): Class attribute containing the
            string for a position_changed event.
        SIZE_CHANGED_EVENT (:obj:`str`): Class attribute containing the string
            for a size_changed event.
    """

    POSITION_CHANGED_EVENT = 'position_changed'
    SIZE_CHANGED_EVENT = 'position_changed'

    def __init__(self, x, y, width, height, event_handler):
        """Creates a new event-driven rectangle using the given event handler.

        The position_changed and size_changed events will fire on
        instantiation.

        Args:
            x (int): The x coordinate for the left edge of the rectangle.
            y (int): The y coordinate for the bottom edge of the rectangle.
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            event_handler (callable): A function taking a :obj:`str` as its
                first argument and this object as its second. See the class
                documentation for a list of possible event string values.
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._event_handler = event_handler
        super(EventRectangle, self).__init__(x, y, width, height)

        self._fire_event(EventRectangle.POSITION_CHANGED_EVENT)
        self._fire_event(EventRectangle.SIZE_CHANGED_EVENT)

    def _fire_event(self, event_string):
        """Calls self.event_handler with the event string and self."""
        self._event_handler(event_string, self)

    @property
    def x(self):
        """Returns the x coordinate."""
        return self._x

    @x.setter
    def x(self, value):
        """Sets the x coordinate and fires the position_changed event."""
        if self._x != value:
            self._x = value
            self._fire_event(EventRectangle.POSITION_CHANGED_EVENT)

    @property
    def y(self):
        """Returns the y coordinate."""
        return self._y

    @y.setter
    def y(self, value):
        """Sets the y coordinate and fires the position_changed event."""
        if self._y != value:
            self._y = value
            self._fire_event(EventRectangle.POSITION_CHANGED_EVENT)

    @property
    def width(self):
        """Returns the width."""
        return self._width

    @width.setter
    def width(self, value):
        """Sets the width and fires the size_changed event."""
        if self._width != value:
            self._width = value
            self._fire_event(EventRectangle.SIZE_CHANGED_EVENT)

    @property
    def height(self):
        """Returns the height."""
        return self._height

    @height.setter
    def height(self, value):
        """Sets the height and fires the size_changed event."""
        if self._height != value:
            self._height = value
            self._fire_event(EventRectangle.SIZE_CHANGED_EVENT)
