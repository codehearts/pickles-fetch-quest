class CollisionCache(object):
    """Cache for collisions between two objects.

    This cache is useful for triggers, where the only information necessary
    is whether two objects are colliding or not.
    """

    def __init__(self):
        """Creates a new collision cache."""
        super(CollisionCache, self).__init__()

        self._collision_cache = set()

        self._current_collisions = set()  # All collisions since last update
        self._removed_collisions = set()  # Removed since last update
        self._new_collisions = set()  # Added since last update

    def add_collision(self, first, second):
        """Adds a collision to the cache.

        If the collision is already cached, it will not be added again.

        Args:
            first (:obj:`engine.game_object.GameObject`):
                The first object in the collision.
            second (:obj:`engine.game_object.GameObject`):
                The second object in the collision.
        """
        key = self._get_cache_key(first, second)

        self._current_collisions.add(key)

    def get_new_collisions(self):
        """Lists objects which collided during the last update.

        Returns:
            A list of tuples, with two :obj:`game_object.GameObject` per tuple.
        """
        return self._new_collisions

    def get_removed_collisions(self):
        """Lists objects which no longer collide as of the last update.

        Returns:
            A list of tuples, with two :obj:`game_object.GameObject` per tuple.
        """
        return self._removed_collisions

    def update(self, ms):
        """Removes cache entries for objects which no longer collide.

        Args:
            ms (int): Time since last update, in milliseconds.
        """
        # Gets collisions seen since the last update that are not in the cache
        self._new_collisions.clear()
        self._new_collisions.update(
            self._current_collisions - self._collision_cache)

        self._collision_cache.update(self._new_collisions)

        # Gets all cached collisions which were not seen since the last update
        self._removed_collisions.clear()
        self._removed_collisions.update(
            self._collision_cache - self._current_collisions)

        self._collision_cache -= self._removed_collisions

        self._current_collisions.clear()

    def _get_cache_key(self, first, second):
        """Creates a compound key for the given objects in the collision cache.

        Returns:
            A tuple of :obj:`game_object.GameObject` where the first and second
            elements are always in the returned order.
        """
        # The first key in the cache is whichever has a lower memory address
        if id(first) < id(second):
            return (first, second)
        return (second, first)
