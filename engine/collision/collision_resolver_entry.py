DETECT_COLLISIONS = 0
"""int: Use detection-only method of resolution.

No objects will be moved, but a collision event will be fired.
"""

RESOLVE_COLLISIONS = 1
"""int: Use resolution method of resolution.

Objects will be moved to resolve the collision and a
collision event will be fired.
"""


class CollisionResolverEntry(object):
    """An entry within a collision resolver object.

    Attributes:
        geometry (:obj:`engine.geometry.Rectangle`):
            The geometry object registered with the collision resolver.
        method (int): The method for collision resolution. One of
                      ``CollisionResolverEntry.DETECT_COLLISIONS`` or
                      ``CollisionResolverEntry.RESOLVE_COLLISIONS``.
    """

    def __init__(self, geometry, method):
        """Creates a new collision resolver entry.

        Args:
            geometry (:obj:`engine.geometry.Rectangle`):
                The geometry object registered with the collision resolver.
            method (int): The method for collision resolution. One of
                          ``CollisionResolverEntry.DETECT_COLLISIONS`` or
                          ``CollisionResolverEntry.RESOLVE_COLLISIONS``.
                          An exception is raised if an invalid value is passed.

        Raises:
            ValueError: If ``method`` is invalid.
        """
        self.geometry = geometry
        self.method = method

        if not (method is DETECT_COLLISIONS or method is RESOLVE_COLLISIONS):
            raise ValueError('Collision resolution method is invalid')
