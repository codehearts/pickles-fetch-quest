from .game_object import GameObject


class Tile(GameObject):
    """Solid rectangular game object which can not be collided with.

    See :obj:`GameObject` for additional attributes.
    """

    def __init__(self, *args, **kwargs):
        """Creates a new tile.

        Args:
            *args: See :obj:`GameObject` for more arguments.
            **kwargs: See :obj:`GameObject` for more keyword arguments.
        """
        super(Tile, self).__init__(*args, **kwargs)
