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
        self._velocity_1000 += ((self.acceleration + self._gravity) *
                                self._mass * ms)
        self.velocity = self._velocity_1000 // 1000

        if abs(self.velocity.x) > self._terminal_velocity.x:
            if self.velocity.x < 0:
                self.velocity.x = -(self._terminal_velocity.x)
            else:
                self.velocity.x = self._terminal_velocity.x

        if abs(self.velocity.y) > self._terminal_velocity.y:
            if self.velocity.y < 0:
                self.velocity.y = -(self._terminal_velocity.y)
            else:
                self.velocity.y = self._terminal_velocity.y
