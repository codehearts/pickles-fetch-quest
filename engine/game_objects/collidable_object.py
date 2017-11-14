from .event_rectangle import EventRectangle


class CollidableObject(EventRectangle):
    """Game object with support for collision detection and resolution.

    See :obj:`EventRectangle` for additional attributes.
    """

    def __init__(self, *args, **kwargs):
        """Creates a new collidable game object.

        Args:
            *args: See :obj:`EventRectangle` for more arguments.
            **kwargs: See :obj:`EventRectangle` for more keyword arguments.
        """
        super(CollidableObject, self).__init__(*args, **kwargs)
