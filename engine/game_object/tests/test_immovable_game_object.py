from ..immovable_game_object import ImmovableGameObject
from engine.geometry import Point2d
from unittest.mock import Mock
import unittest


class TestImmovableGameObject(unittest.TestCase):
    """Test functionality of immovable game objects."""

    def test_immovable_game_object_have_large_mass(self):
        """Immovable game objects have large mass."""
        game_object = ImmovableGameObject(x=1, y=2, width=3, height=4)
        self.assertEqual(9999, game_object.mass)

    def test_immovable_game_object_have_no_gravity(self):
        """Immovable game objects have no gravity."""
        game_object = ImmovableGameObject(x=1, y=2, width=3, height=4)

        # Run a simulation to determine if gravity is applied
        game_object.acceleration = game_object.velocity = Point2d(0, 0)
        game_object.run_simulation(123)

        # Game object was not moved by gravity
        self.assertEqual(1, game_object.x)
        self.assertEqual(2, game_object.y)

    def test_update_does_not_run_physics_simulation(self):
        """Immovable game objects do not run physics simulations on update."""
        game_object = ImmovableGameObject(x=1, y=2, width=3, height=4)
        game_object.run_simulation = Mock()

        game_object.update(123)

        game_object.run_simulation.assert_not_called()
