from .collidable_object import CollidableObject


class Tile(CollidableObject):
    """Solid rectangular tile which can not be collided with.

    See :obj:`CollidableObject` for additional attributes.
    """

    def __init__(self, *args, **kwargs):
        """Creates a new tile.

        Args:
            *args: See :obj:`CollidableObject` for more arguments.
            **kwargs: See :obj:`CollidableObject` for more keyword arguments.
        """
        super(Tile, self).__init__(*args, **kwargs)
