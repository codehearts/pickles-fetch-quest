from ..physics_2d import Physics2d
import unittest


class TestPhysics2d(unittest.TestCase):
    """Test simulation results for two dimensional physics."""

    def assertPoint(self, expected_coordinates, point):
        """Asserts that point coordinates are equal to expected coordinates.

        Args:
            expected_coordinates (tuple of int): Expected coordinates.
            point (:obj:`engine.geometry.Point2d`):
                The point to assert against.
        """
        self.assertEqual(expected_coordinates[0], point.x)
        self.assertEqual(expected_coordinates[1], point.y)

    def test_create_2d_physics(self):
        """Creating 2d physics sets initial velocity and acceleration."""
        physics = Physics2d(mass=1, gravity=(5, 6), terminal_velocity=(7, 8))
        physics.velocity.set((1, 2))
        physics.acceleration.set((3, 4))

        self.assertPoint((1, 2), physics.velocity)
        self.assertPoint((3, 4), physics.acceleration)

    def test_simulate_with_mass(self):
        """Mass increases acceleration."""
        physics = Physics2d(mass=2, gravity=(1, 1), terminal_velocity=(10, 10))
        physics.acceleration.set((1, 1))

        # Mass of 2 doubles external and gravitational acceleration (1+1)*2
        physics.run_simulation(1000)
        self.assertPoint((4, 4), physics.velocity)

    def test_assign_velocity(self):
        """Assigning velocity changes velocity accordingly."""
        physics = Physics2d(mass=1, gravity=(3, 3), terminal_velocity=(50, 50))
        physics.acceleration.set((2, 2))

        physics.run_simulation(500)  # (0 + 2.5 = 2.5, 0 + 2.5 = 2.5)
        self.assertPoint((2, 2), physics.velocity)  # 2 from int rounding

        physics.velocity.x = 5
        physics.run_simulation(500)  # (5 + 2.5 = 7.5, 2.5 + 2.5 = 5)
        self.assertPoint((7, 5), physics.velocity)  # 7 from int rounding

        physics.velocity.y = 7
        physics.run_simulation(500)  # (7.5 + 2.5 = 10, 7 + 2.5 = 9.5)
        self.assertPoint((10, 9), physics.velocity)  # 9 from int rounding

    def test_assign_acceleration(self):
        """Assigning acceleration changes velocity accordingly."""
        physics = Physics2d(mass=1, gravity=(3, 3), terminal_velocity=(50, 50))
        physics.acceleration.set((2, 2))

        physics.run_simulation(500)  # (0 + 2.5 = 2.5, 0 + 2.5 = 2.5)
        self.assertPoint((2, 2), physics.velocity)  # 2 from int rounding

        physics.acceleration.x = 4
        physics.run_simulation(500)  # (2.5 + 3.5 = 6, 2.5 + 2.5 = 5)
        self.assertPoint((6, 5), physics.velocity)

        physics.acceleration.y = 4
        physics.run_simulation(500)  # (6 + 3.5 = 9.5, 5 + 3.5 = 8.5)
        self.assertPoint((9, 8), physics.velocity)  # 9, 8 from int rounding

    # Tests for acceleration with gravitational pull

    def test_simulate_positive_x(self):
        """Positive x acceleration increases velocity."""
        physics = Physics2d(mass=1, gravity=(3, 0), terminal_velocity=(5, 5))
        physics.acceleration.set((2, 0))

        physics.run_simulation(500)
        self.assertPoint((2, 0), physics.velocity)  # 2 from int truncation
        physics.run_simulation(500)
        self.assertPoint((5, 0), physics.velocity)

    def test_simulate_negative_x(self):
        """Negative x acceleration decreases velocity."""
        physics = Physics2d(mass=1, gravity=(-3, 0), terminal_velocity=(5, 5))
        physics.acceleration.set((-2, 0))
        physics.run_simulation(500)
        self.assertPoint((-2, 0), physics.velocity)  # -2 from int truncation
        physics.run_simulation(500)
        self.assertPoint((-5, 0), physics.velocity)

    def test_simulate_positive_y(self):
        """Positive y acceleration increases velocity."""
        physics = Physics2d(mass=1, gravity=(0, 3), terminal_velocity=(5, 5))
        physics.acceleration.set((0, 2))

        physics.run_simulation(500)
        self.assertPoint((0, 2), physics.velocity)  # 2 from int truncation
        physics.run_simulation(500)
        self.assertPoint((0, 5), physics.velocity)

    def test_simulate_negative_y(self):
        """Negative y acceleration decreases velocity."""
        physics = Physics2d(mass=1, gravity=(0, -3), terminal_velocity=(5, 5))
        physics.acceleration.set((0, -2))

        physics.run_simulation(500)
        self.assertPoint((0, -2), physics.velocity)  # -2 from int truncation
        physics.run_simulation(500)
        self.assertPoint((0, -5), physics.velocity)

    # Tests for terminal velocity

    def test_simulate_positive_x_terminal_velocity(self):
        """Positive x velocity caps at terminal velocity without gravity."""
        physics = Physics2d(mass=1, gravity=(10, 0), terminal_velocity=(5, 0))
        physics.acceleration.set((10, 0))

        physics.run_simulation(1000)
        self.assertPoint((5, 0), physics.velocity)

    def test_simulate_negative_x_terminal_velocity(self):
        """Negative x velocity caps at terminal velocity without gravity."""
        physics = Physics2d(mass=1, gravity=(-10, 0), terminal_velocity=(5, 0))
        physics.acceleration.set((-10, 0))

        physics.run_simulation(1000)
        self.assertPoint((-5, 0), physics.velocity)

    def test_simulate_positive_y_terminal_velocity(self):
        """Positive y velocity caps at terminal velocity without gravity."""
        physics = Physics2d(mass=1, gravity=(0, 10), terminal_velocity=(0, 5))
        physics.acceleration.set((0, 10))

        physics.run_simulation(1000)
        self.assertPoint((0, 5), physics.velocity)

    def test_simulate_negative_y_terminal_velocity(self):
        """Negative y velocity caps at terminal velocity without gravity."""
        physics = Physics2d(mass=1, gravity=(0, -10), terminal_velocity=(0, 5))
        physics.acceleration.set((0, -10))
        physics.run_simulation(1000)
        self.assertPoint((0, -5), physics.velocity)
