from .physical_game_object import PhysicalGameObject


class ImmovableGameObject(PhysicalGameObject):
    """Immovable physical game object.

    This object has physics, but will always remain at rest in the simulation.
    This is useful for things like colliders for stage boundaries.

    Attributes:
        x (int): The x coordinate of the left edge of the object.
        y (int): The y coordinate of the bottom edge of the object.
        width (int): The width of the object.
        height (int): The height of the object.

    Events:
        on_move: The x or y coordinates of the object have changed.
            A tuple of the x and y coordinates will be passed to the listeners.
        on_move_relative: The x or y coordinates of the object have changed.
            A tuple of the x and y deltas will be passed to the listeners.
        on_collider_enter: The object's collider has entered a collision with
            another object. The other object will be passed to the listeners.
        on_collider_exit: The object's collider has exited a collision with
            another object. The other object will be passed to the listeners.
        on_trigger_enter: The object's trigger overlapped with another object.
            The other object will be passed to the listeners.
        on_trigger_leave: The object's trigger no longer overlaps with the
            other object. The other object will be passed to the listeners.
    """

    def __init__(self, x, y, width, height):
        """Creates a new immovable game object.

        Args:
            x (int): The x coordinate of the left edge of the object.
            y (int): The y coordinate of the bottom edge of the object.
            width (int): The width of the object.
            height (int): The height of the object.
        """
        super(ImmovableGameObject, self).__init__(
            x, y, width, height, mass=9999, gravity=(0, 0))

    def update(self, ms):
        """Updates the immovable game object based on time.

        Because immovable objects will not be moved by a physics simulation,
        this is implemented as a noop.

        Args:
            ms (int): Number of milliseconds since the last update.
        """
        pass
