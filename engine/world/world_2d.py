from engine.collision import CollisionCache, PositionalCollisionCache
from engine.collision import resolve_game_object_collision
from engine.event_dispatcher import EventDispatcher
from engine.geometry import detect_overlap_2d
from .world_object import WorldObject, COLLIDER, TRIGGER


class World2d(EventDispatcher):
    """Detects overlap and resolves collisions between game objects.

    This is implemented as a sweep-and-prune algorithm over all registered
    objects. Objects can be registered as:

    * Triggers: Dispatches an on_object_enter event when this object overlaps
        with another, and an on_object_leave event when they no longer overlap.
    * Colliders: Resolves collisions between two colliders using  the
        :mod:`collision` module. An on_collision event is dispatched to botch
        objects upon resolution.

    Events:
        on_update_enter: A world update has just begun.
            The world will be passed to the listeners.
        on_update_exit: A world update has just completed.
            The world will be passed to the listeners.
        on_collider_add: A collider was added to the world.
            The collider will be passed to the listeners.
        on_trigger_add: A trigger was added to the world.
            The trigger will be passed to the listeners.
    """

    def __init__(self):
        """Creates an empty world with two dimensional physics."""
        super(World2d, self).__init__()
        self._colliders = PositionalCollisionCache()
        self._triggers = CollisionCache()
        self._objects = []

        self.register_event_type('on_update_enter')
        self.register_event_type('on_update_exit')
        self.register_event_type('on_collider_add')
        self.register_event_type('on_trigger_add')

    def add_collider(self, physical_object):
        """Adds a game object to be treated as a collider.

        Args:
            physical_object (:obj:`engine.game_object.PhysicalObject`):
                The game object to resolve collisions against.
        """
        self._objects.append(WorldObject(physical_object, COLLIDER))
        self.dispatch_event('on_collider_add', physical_object)

    def add_trigger(self, physical_object):
        """Adds a game object to be treated as a trigger area.

        Args:
            physical_object (:obj:`engine.game_object.GameObject`):
                The game object to detect collisions with.
        """
        self._objects.append(WorldObject(physical_object, TRIGGER))
        self.dispatch_event('on_trigger_add', physical_object)

    def update(self, ms):
        """Updates the state of the world by processing object collisions.

        Args:
            ms (int): The time since last update, in milliseconds.
        """
        self.dispatch_event('on_update_enter', self)

        # Sort objects by their x coordinate
        self._objects.sort(key=lambda world_object: world_object.object.x)

        sweep_list = []
        for obj in self._objects:
            # Run narrow phase on sweep entries, removing swept-past objects
            sweep_list = [self._narrow_phase(x, obj) for x in sweep_list
                          if not self._is_swept_past(x, obj)]
            # Add the current object to the sweep list
            sweep_list.append(obj)

        # Update the colliders and triggers
        self._colliders.update(ms)
        self._triggers.update(ms)

        # Notify of objects entering and leaving collisions
        self._dispatch(
            'on_collider_enter', self._colliders.get_new_collisions())
        self._dispatch(
            'on_collider_exit', self._colliders.get_removed_collisions())
        self._dispatch(
            'on_trigger_enter', self._triggers.get_new_collisions())
        self._dispatch(
            'on_trigger_exit', self._triggers.get_removed_collisions())

        self.dispatch_event('on_update_exit', self)

    def _narrow_phase(self, first, second):
        """Detects and processes a collision between two game objects.

        If both objects are colliders, the lighter object will be moved.

        Args:
            first (:obj:`world_object.WorldObject`):
                The first potential collision object.
            second (:obj:`world_object.WorldObject`):
                The second potential collision object.

        Returns:
            The first object passed into the narrow phase.
        """
        # Process as a collider collision if neither object is a trigger
        if TRIGGER not in (first.type, second.type):
            self._resolve_colliders(first.object, second.object)
        else:
            self._resolve_triggers(first.object, second.object)

        return first

    def _resolve_colliders(self, first, second):
        """Resolves a collision between colliders.

        Args:
            first (:obj:`game_object.GameObject`):
                The first collider in the collision.
            second (:obj:`game_object.GameObject`):
                The second collider in the collision.
        """
        velocity_delta = resolve_game_object_collision(first, second)
        self._colliders.add_collision(first, second, velocity_delta)

    def _resolve_triggers(self, first, second):
        """Resolves a collision between one trigger and any other object.

        Args:
            first (:obj:`game_object.GameObject`):
                The first trigger or collider in the collision.
            second (:obj:`game_object.GameObject`):
                The second trigger or collider in the collision.
        """
        if detect_overlap_2d(first, second):
            self._triggers.add_collision(first, second)

    def _dispatch(self, event, collisions):
        """Dispatches a collision event to all collisions.

        Args:
            event (str): Name of the event to fire.
            collisions (list of tuple of :obj:`game_object.GameObject`):
                A list with pairs of objects which have collided.
        """
        for first, second in collisions:
            first.dispatch_event(event, second)
            second.dispatch_event(event, first)

    def _is_swept_past(self, old_entry, new_entry):
        """Determines if the new entry has swept past the prior entry.

        Args:
            old_entry (:obj:`world_object.WorldObject`):
                The prior entry in the sweep list.
            new_entry (:obj:`world_object.WorldObject`):
                The new entry into the sweep list.

        Returns:
            True if the prior entry has been swept past, false otherwise.
        """
        prior_endpoint = old_entry.object.x + old_entry.object.width
        return prior_endpoint <= new_entry.object.x
