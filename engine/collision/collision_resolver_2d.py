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

        # Object position cache from past collisions, to limit notifications
        # Objects which collided have their positions store like so:
        #     [(first_object, second_object)] = {
        #         'first' => cached first_object.coordinates,
        #         'second' => cached second_object.coordinates,
        #         'delta' => cached velocity_delta,
        #     }
        # Note: first_object < second_object, compared by memory address
        self._collision_position_cache = {}

        # Collision resolution cache for the current resolution pass
        # This is a mapping of (first, second) => delta
        self._resolved_collisions = {}

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

        # Clean the collision position cache after resolution
        self._clean_position_cache()

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
            self._resolve_collision(first.geometry, second.geometry)

        return first

    def _resolve_collision(self, first, second):
        """Resolve a collision between two objects, notifying new collisions.

        Args:
            first (:obj:`engine.game_object.GameObject`):
                The first object in the collision.
            second (:obj:`engine.game_object.GameObject`):
                The second object in the collision.
        """
        velocity_delta = resolve_game_object_collision(first, second)

        is_repeat = self._is_repeat_collision(first, second, velocity_delta)

        # Notify if a collision occurred and is not a repeat
        if velocity_delta != (0, 0) and not is_repeat:
            self._notify_collision(first, second)

            # Cache this new collision
            key = self._get_cache_key(first, second)
            self._resolved_collisions[key] = velocity_delta

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

    def _is_repeat_axis_collision(self, first, second, cache_entry, axis):
        """Determines whether the collision was repeated on the axis."""
        key = self._get_cache_key(first, second)
        index = 0 if axis == 'x' else 1

        first_changed = cache_entry['first'][index] == getattr(key[0], axis)
        second_changed = cache_entry['second'][index] == getattr(key[1], axis)
        axis_delta = cache_entry['delta'][index]

        return first_changed and second_changed or axis_delta == 0

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
        cache = self._get_cached_collision(first, second)

        # No prior collision is cached, this can't be a repeat
        if cache is None:
            return False

        x_repeated = self._is_repeat_axis_collision(first, second, cache, 'x')
        y_repeated = self._is_repeat_axis_collision(first, second, cache, 'y')

        return x_repeated and y_repeated

    def _get_cached_collision(self, first, second):
        """Returns the cache entry for a collision between two objects.

        Args:
            first (:obj:`engine.game_object.GameObject`):
                The first object in a collision.
            second (:obj:`engine.game_object.GameObject`):
                The second object in a collision.

        Returns:
            An object with "first," "second," and "delta" fields if the
            collision was cached, None otherwise.
        """
        cache_key = self._get_cache_key(first, second)

        if cache_key in self._collision_position_cache:
            return self._collision_position_cache[cache_key]
        return None

    def _clean_position_cache(self):
        """Removes positional cache entries for objects which have moved."""
        clean_position_cache = {}

        # Create a new positional cache of repeated collisions
        for key, cache in self._collision_position_cache.items():
            if self._is_repeat_collision(key[0], key[1], cache['delta']):
                clean_position_cache[key] = cache

        self._collision_position_cache = clean_position_cache

        # Cache the positions of all newly resolved collisions
        for key, delta in self._resolved_collisions.items():
            self._collision_position_cache[key] = {
                'first': (key[0].x, key[0].y),
                'second': (key[1].x, key[1].y),
                'delta': delta
            }

        self._resolved_collisions = {}

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
