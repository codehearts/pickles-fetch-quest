from engine.util.math import divide_toward_zero
from engine import geometry


class Physics2d(object):
    """Simple two dimensional physics simulation.

    Attributes:
        velocity (:obj:`engine.geometry.Point2d`):
            Velocity along the x and y axes in units per second.
        acceleration (:obj:`engine.geometry.Point2d`):
            Acceleration along the x and y axes in units per second.
        friction (int): Coefficient of friction between 1 and 100 when no
            acceleration is applied, to slow the object to rest.
    """

    def __init__(self, mass=1, friction=100, gravity=(0, -10),
                 terminal_velocity=(100, 100)):
        """Creates a new two dimensional physics simulation.

        Args:
            mass (int, optional): Mass of the object in units. Defaults to 100.
            friction (int): Coefficient of friction between 1 and 100 when no
                acceleration is applied, to slow it to rest. Defaults to 100.
            gravity (tuple of int, optional): Gravitational pull on the object
                in units per second. Defaults to (0, 10).
            terminal_velocity (tuple of int, optional): Terminal velocity along
                the x and y axes in units per second. Defaults to (100, 100).
        """
        super(Physics2d, self).__init__()
        self.velocity = geometry.Point2d(0, 0)
        self.acceleration = geometry.Point2d(0, 0)
        self.friction = max(min(100, friction), 1)  # Clamp between 1 and 100
        self._terminal_velocity = geometry.Point2d(*terminal_velocity)
        self._gravity = geometry.Point2d(*gravity)
        self.mass = mass

        # Higher resolution copies for simulation
        self._velocity_1000 = self.velocity * 1000

    def run_simulation(self, ms):
        """Adjusts velocities based on simulation results after the given time.

        This method call is instantaneous, it does not run for the given time.

        Args:
            ms (int): The number of milliseconds to run the simulation for.
        """
        # Calculate the total acceleration as force applied plus gravity
        total_acceleration = (self.acceleration + self._gravity)
        friction = 100 - self.friction

        for axis in ('x', 'y'):
            velocity = getattr(self.velocity, axis)
            velocity_1000 = getattr(self._velocity_1000, axis)

            # Ensure high resolution velocity matches the current velocity
            if divide_toward_zero(velocity_1000, 1000) != velocity:
                setattr(self._velocity_1000, axis, velocity * 1000)

            # Apply friction to decelerate when no acceleration is present
            if getattr(total_acceleration, axis) == 0:
                setattr(self._velocity_1000, axis,
                        divide_toward_zero(velocity_1000 * friction, 100))

        # Update velocity based on acceleration, mass, and time
        self._velocity_1000 += (total_acceleration * self.mass * ms)

        for axis in ('x', 'y'):
            velocity_1000 = getattr(self._velocity_1000, axis)

            # Round off the integer velocity towards 0
            setattr(self.velocity, axis,
                    divide_toward_zero(velocity_1000, 1000))

            velocity = getattr(self.velocity, axis)
            terminal_velocity = getattr(self._terminal_velocity, axis)

            # Apply terminal velocity
            if abs(velocity) > terminal_velocity:
                if velocity < 0:
                    terminal_velocity = -terminal_velocity

                setattr(self.velocity, axis, terminal_velocity)
