from .collision_resolver_entry import DETECT_COLLISIONS, CollisionResolverEntry
from .collision_resolution_game_object import resolve_game_object_collision


class CollisionResolver2d(object):
    """Resolves collisions between registered two dimensional game objects.

    This is implemented as a sweep-and-prune algorithm.
    """

    def __init__(self):
        """Creates a new two dimensional collision resolver."""
        super(CollisionResolver2d, self).__init__()
        self._registered_entries = []
        self._current_collisions = {}
        self._previous_collisions = {}
        self._i = 0

    def register(self, game_object, method):
        """Registers a game object to be resolved using the given method.

        Args:
            game_object (:obj:`GameObject`): The game object to resolve
                                             collisions against.
            method (int): The method for resolving collisions with this object.
                          One of ``engine.DETECT_COLLISIONS`` or
                          ``engine.RESOLVE_COLLISIONS``. An exception is
                          raised for any other value.

        Raises:
            ValueError: If ``method`` is invalid.
        """
        entry = CollisionResolverEntry(game_object, method)
        self._registered_entries.append(entry)

    def resolve(self):
        """Detects and resolves collisions amongst registered game objects."""
        self._previous_collisions, self._current_collisions = \
            self._current_collisions, self._previous_collisions
        self._current_collisions.clear()

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
            first (:obj:`GameObject`): The first potential collision object.
            second (:obj:`GameObject`): The second potential collision object.

        Returns:
            The first object passed into the narrow phase.
        """
        # If either object is detection-only or resolution was performed
        if DETECT_COLLISIONS in (first.method, second.method) or \
           resolve_game_object_collision(first.geometry, second.geometry):
            self._notify_collision(first.geometry, second.geometry)

        return first

    def _notify_collision(self, first, second):
        """Notifies collision if the objects weren't already colliding.

        Args:
            first (:obj:`GameObject`): The first potential collision object.
            second (:obj:`GameObject`): The second potential collision object.
        """
        # Only notify if these objects were not previously colliding
        if first not in self._previous_collisions or \
           second not in self._previous_collisions[first]:
            first.notify_collision_with(second)
            second.notify_collision_with(first)

        self._current_collisions.setdefault(first, []).append(second)
        self._current_collisions.setdefault(second, []).append(first)

    def _is_swept_past(self, prior_entry, new_entry):
        """Determines if the new entry has swept past the prior entry.

        Args:
            prior_entry (:obj:`CollisionResolverEntry`): The prior entry
                                                         in the sweep list.
            new_entry (:obj:`CollisionResolverEntry`): The new entry into
                                                       the sweep list.

        Returns:
            True if the prior entry has been swept past, false otherwise.
        """
        prior_endpoint = prior_entry.geometry.x + prior_entry.geometry.width
        return prior_endpoint <= new_entry.geometry.x
