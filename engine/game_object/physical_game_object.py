from .game_object import GameObject
from engine.physics import Physics2d


class PhysicalGameObject(GameObject, Physics2d):
    """Game object with support for two dimensional physics simulation.

    See :cls:`physics.Physics2d` for usage information on physics.

    Attributes:
        x (int): The x coordinate of the left edge of the object.
        y (int): The y coordinate of the bottom edge of the object.
        width (int): The width of the object.
        height (int): The height of the object.
        velocity (:obj:`geometry.Point2d`):
            Velocity along the x and y axes in units per second.
        acceleration (:obj:`geometry.Point2d`):
            Acceleration along the x and y axes in units per second.
        friction (int): Coefficient of friction between 1 and 100 when no
            acceleration is applied, to slow the object to rest.

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

    def __init__(self, x, y, width, height, **kwargs):
        """Creates a new physical game object.

        Args:
            x (int): The x coordinate of the left edge of the object.
            y (int): The y coordinate of the bottom edge of the object.
            width (int): The width of the object.
            height (int): The height of the object.

        Kwargs:
            mass (int, optional): Mass of the object in units. Defaults to 100.
            friction (int, optional):
                Coefficient of friction between 1 and 100 when no acceleration
                is applied, to slow to rest. Defaults to 100.
            gravity (tuple of int, optional):
                Gravitational pull in units per second. Defaults to (0, 10).
            terminal_velocity (tuple of int, optional):
                Terminal velocity along the x and y axes in units per second.
                Defaults to (100, 100).
        """
        super(PhysicalGameObject, self).__init__(x, y, width, height, **kwargs)

    def update(self, ms):
        """Updates the physics simulation of the game object based on time.

        The object will be repositioned according to its velocity.

        Args:
            ms (int): Number of milliseconds since the last update.
        """
        self.run_simulation(ms)
        self.move_by(self.velocity)
