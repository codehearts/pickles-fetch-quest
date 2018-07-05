from ..geometry import Point2d


class Physics2d(object):
    """Simple two dimensional physics simulation.

    Attributes:
        velocity (:obj:`geometry.Point2d`): Velocity along the x and y axes
            in units per second.
        acceleration (:obj:`geometry.Point2d`): Acceleration along the x and y
            axes in units per second.
    """

    def __init__(self, mass=1, velocity=(0, 0), acceleration=(0, 0),
                 gravity=(0, -10), terminal_velocity=(100, 100)):
        """Creates a new two dimensional physics simulation.

        Args:
            mass (int, optional): Mass of the object in units. Defaults to 100.
            velocity (tuple of int, optional): Initial velocity in units per
                second. Defaults to (0, 0).
            acceleration (tuple of int, optional): Initial acceleration in
                units per second. Defaults to (0, 0).
            gravity (tuple of int, optional): Gravitational pull on the object
                in units per second. Defaults to (0, 10).
            terminal_velocity (tuple of int, optional): Terminal velocity along
                the x and y axes in units per second. Defaults to (100, 100).
        """
        super(Physics2d, self).__init__()
        self.velocity = Point2d(*velocity)
        self.acceleration = Point2d(*acceleration)
        self._terminal_velocity = Point2d(*terminal_velocity)
        self._gravity = Point2d(*gravity)
        self._mass = mass

        # Higher resolution copies for simulation
        self._velocity_1000 = self.velocity * 1000

    def run_simulation(self, ms):
        """Adjusts velocities based on simulation results after the given time.

        This method call is instantaneous, it does not run for the given time.

        Args:
            ms (int): The number of milliseconds to run the simulation for.
        """
        # Ensure high resolution velocity matches the current velocity
        for axis in ('x', 'y'):
            velocity = getattr(self.velocity, axis)
            if (getattr(self._velocity_1000, axis) // 1000) != velocity:
                setattr(self._velocity_1000, axis, velocity * 1000)

        self._velocity_1000 += ((self.acceleration + self._gravity) *
                                self._mass * ms)
        self.velocity = self._velocity_1000 // 1000

        for axis in ('x', 'y'):
            velocity = getattr(self.velocity, axis)
            terminal_velocity = getattr(self._terminal_velocity, axis)

            if abs(velocity) > terminal_velocity:
                if velocity < 0:
                    terminal_velocity = -terminal_velocity

                setattr(self.velocity, axis, terminal_velocity)
