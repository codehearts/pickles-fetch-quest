from .collision_resolution_game_object import resolve_game_object_collision
from .collision_resolver_entry import CollisionResolverEntry
from engine import collision


class CollisionResolver2d(object):
    """Resolves collisions between registered two dimensional game objects.

    This is implemented as a sweep-and-prune algorithm.
    """

    def __init__(self):
        """Creates a new two dimensional collision resolver.
        """
        super(CollisionResolver2d, self).__init__()
        self._registered_entries = []
        self._collision_cache = {}

    def register(self, game_object, method):
        """Registers a game object to be resolved using the given method.

        Args:
            game_object (:obj:`engine.game_object.GameObject`):
                The game object to resolve collisions against.
            method (int): The method for resolving collisions with this object.
                          One of ``engine.collisions.DETECT_COLLISIONS`` or
                          ``engine.RESOLVE_COLLISIONS``. An exception is
                          raised for any other value.

        Raises:
            ValueError: If ``method`` is invalid.
        """
        entry = CollisionResolverEntry(game_object, method)
        self._registered_entries.append(entry)

    def resolve(self):
        """Detects and resolves collisions amongst registered game objects."""
        # Sort entries by the x coordinate of their geometry
        self._registered_entries.sort(key=lambda x: x.geometry.x)

        sweep_list = []
        for entry in self._registered_entries:
            # Run narrow phase on sweep entries, removing swept-past entries
            sweep_list = [self._narrow_phase(x, entry) for x in sweep_list
                          if not self._is_swept_past(x, entry)]
            # Add the current entry to the sweep list
            sweep_list.append(entry)

    def _narrow_phase(self, first, second):
        """Detects a collision between the two game objects and resolves it.

        This operation will move one or both objects.

        Args:
            first (:obj:`engine.game_object.GameObject`):
                The first potential collision object.
            second (:obj:`engine.game_object.GameObject`):
                The second potential collision object.

        Returns:
            The first object passed into the narrow phase.
        """
        if collision.DETECT_COLLISIONS in (first.method, second.method):
            # If either object is detection-only, notify of the collision
            self._notify_collision(first.geometry, second.geometry)
        else:
            # If neither object is detection-only, resolve the collision
            delta = resolve_game_object_collision(
                first.geometry, second.geometry)

            # Look for delta from a prior collision between these objects
            cache_delta = ()
            if first in self._collision_cache:
                if second in self._collision_cache[first]:
                    cache_delta = self._collision_cache[first][second]

            if delta != (0, 0):
                # Is any index in `delta` > the same index in `cache_delta`?
                delta_expanded = any(x > y for x, y in zip(delta, cache_delta))

                if not cache_delta or delta_expanded:
                    # Notify collision if displacement increased on any axis
                    self._notify_collision(first.geometry, second.geometry)

                # Cache the delta from this collision
                self._collision_cache.setdefault(first, {})[second] = delta
                self._collision_cache.setdefault(second, {})[first] = delta

        return first

    def _notify_collision(self, first, second):
        """Notifies collision if the objects weren't already colliding.

        Args:
            first (:obj:`engine.game_object.GameObject`):
                The first potential collision object.
            second (:obj:`engine.game_object.GameObject`):
                The second potential collision object.
        """
        # Only notify if these objects were not previously colliding
        first.notify_collision_with(second)
        second.notify_collision_with(first)

    def _is_swept_past(self, old_entry, new_entry):
        """Determines if the new entry has swept past the prior entry.

        Args:
            old_entry (:obj:`collision_resolver_entry.CollisionResolverEntry`):
                The prior entry in the sweep list.
            new_entry (:obj:`collision_resolver_entry.CollisionResolverEntry`):
                The new entry into the sweep list.

        Returns:
            True if the prior entry has been swept past, false otherwise.
        """
        prior_endpoint = old_entry.geometry.x + old_entry.geometry.width
        return prior_endpoint <= new_entry.geometry.x
