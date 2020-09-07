from ..physical_game_object import PhysicalGameObject
from unittest.mock import Mock
import unittest


class TestPhysicalGameObject(unittest.TestCase):
    """Test functionality of physical game objects."""

    def test_create_physical_game_object(self):
        """Physical game objects are initialized with the given properties."""
        game_object = PhysicalGameObject(
            x=1, y=2, width=3, height=4,
            mass=5, friction=6, terminal_velocity=(7, 8), gravity=(9, 10))

        self.assertEqual(1, game_object.x)
        self.assertEqual(2, game_object.y)
        self.assertEqual(3, game_object.width)
        self.assertEqual(4, game_object.height)
        self.assertEqual(5, game_object.mass)
        self.assertEqual(6, game_object.friction)
        self.assertEqual((0, 0), game_object.velocity)
        self.assertEqual((0, 0), game_object.acceleration)

    def test_physics_simulation_is_run_on_update(self):
        """Physical game objects are run their simulation on update."""
        game_object = PhysicalGameObject(x=1, y=2, width=3, height=4)
        game_object.run_simulation = Mock()

        game_object.update(123)

        game_object.run_simulation.assert_called_once_with(123)

    def test_update_applies_velocity_to_position(self):
        """Physical game objects are affected by their velocity on update."""
        game_object = PhysicalGameObject(x=1, y=2, width=3, height=4)
        game_object.run_simulation = Mock()
        game_object.velocity = (10, 20)

        game_object.update(123)

        self.assertEqual(11, game_object.x)
        self.assertEqual(22, game_object.y)
