COLLIDER = 0
"""int: Resolves collisions between two colliders using  the
        :mod:`collision` module. An on_collision event is dispatched to botch
        objects upon resolution.
"""

TRIGGER = 1
"""int: Dispatches an on_object_enter event when this object overlaps
        with another, and an on_object_leave event when they no longer overlap.
"""


class WorldObject(object):
    """An object within a world.

    Attributes:
        object (:obj:`engine.game_object.GameObject`):
            The physical object within the world.
        type (int): The collision type for the object. Must be one of
            ``world_object.TRIGGER`` or ``world_object.COLLIDER``.
    """

    def __init__(self, physical_object, type):
        """Creates a new object to place within a world.

        Args:
            object (:obj:`engine.game_object.GameObject`):
                The physical object within the world.
            type (int): The collision type for the object. Must be one of
                ``world_object.TRIGGER`` or ``world_object.COLLIDER``.

        Raises:
            ValueError: If ``method`` is invalid.
        """
        self.object = physical_object
        self.type = type

        if type not in (TRIGGER, COLLIDER):
            raise ValueError('World object type is invalid')
