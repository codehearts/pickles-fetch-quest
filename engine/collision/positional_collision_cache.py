from .collision_cache import CollisionCache


class PositionalCollisionCache(CollisionCache):
    """Collision cache based on object positioning and velocity.

    This cache is useful for colliders, as collisions will remain cached until
    the objects visually move and no longer collide. The term "visual movement"
    refers to collisions where the player can see objects move, as opposed to
    collisions where objects return to their previous position such as when an
    object collides with the ground while at rest.
    """

    def __init__(self):
        """Creates a new positional collision cache."""
        super(PositionalCollisionCache, self).__init__()

        # Object position cache from past collisions, to limit notifications
        # This is a mapping of (first, second) => PositionalCacheEntry
        self._positional_collision_cache = {}

    def add_collision(self, first, second, velocity_delta):
        """Adds a collision to the cache.

        If the collision is already cached, it will not be added again.

        Args:
            first (:obj:`engine.game_object.GameObject`):
                The first object in a collision.
            second (:obj:`engine.game_object.GameObject`):
                The second object in a collision.
            velocity_delta (tuple of int):
                Delta of the x and y velocity for resolution.
        """
        # There's nothing to do if the collision had no movement
        if velocity_delta == (0, 0):
            return

        super(PositionalCollisionCache, self).add_collision(first, second)

        # Update the positional cache
        key = self._get_cache_key(first, second)
        self._positional_collision_cache[key] = PositionalCacheEntry(
            first=key[0], second=key[1], velocity_delta=velocity_delta)

    def update(self, ms):
        """Removes cache entries for objects which moved and no longer collide.

        Args:
            ms (int): Time since last update, in milliseconds.
        """
        super(PositionalCollisionCache, self).update(ms)

        # Keep any removed collisions that are repeats of a previous collision
        positional_cache = self._positional_collision_cache
        kept_collisions = {c for c in self._removed_collisions
                           if self._is_repeat_collision(
                               *c, positional_cache[c].velocity_delta)}

        self._removed_collisions -= kept_collisions
        self._collision_cache.update(kept_collisions)

        # Delete all removed collisions from the positional cache
        for collision in self._removed_collisions:
            del self._positional_collision_cache[collision]

    def _is_repeat_collision(self, first, second, velocity_delta):
        """Checks if a collision between two objects is identical to the last.

        Args:
            first (:obj:`engine.game_object.GameObject`):
                The first object in a collision.
            second (:obj:`engine.game_object.GameObject`):
                The second object in a collision.
            velocity_delta (tuple of int):
                Delta of the x and y velocities after resolution.

        Returns:
            True if the collision is identical to the last collision between
            these objects, False otherwise.
        """
        key = self._get_cache_key(first, second)

        # A collision between these objects is not cached, this must be new
        if key not in self._positional_collision_cache:
            return False

        # Iterate over the cached and new positions on the x and y axes
        return self._is_repeated_on_axis(key, velocity_delta, 'x') and \
            self._is_repeated_on_axis(key, velocity_delta, 'y')

    def _is_repeated_on_axis(self, key, velocity_delta, axis):
        """Checks if a collision between two objects is identical to the last.

        Args:
            key (tuple of :obj:`engine.game_object.GameObject`):
                Key to the cached collision.
            velocity_delta (tuple of int):
                Delta of the x and y velocities after resolution.
            axis (str):
                The axis to check for a repeated collision on.

        Returns:
            True if the collision is identical to the last collision between
            these objects and the given axis, False otherwise.
        """
        cached = self._positional_collision_cache[key]
        index = 0 if axis == 'x' else 1

        is_first_same = cached.first_position[index] == getattr(key[0], axis)
        is_second_same = cached.second_position[index] == getattr(key[1], axis)
        has_no_velocity = velocity_delta[index] == 0

        return is_first_same and is_second_same or has_no_velocity


class PositionalCacheEntry(object):
    """Positional collision cache entry."""

    def __init__(self, first, second, velocity_delta):
        """Creates a new positional collision cache entry."""
        self.first_position = (first.x, first.y)
        self.second_position = (second.x, second.y)
        self.velocity_delta = velocity_delta
