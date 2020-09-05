from ..game_object import GameObject
from ...geometry import Rectangle
from unittest.mock import Mock
import unittest


class TestGameObject(unittest.TestCase):
    """Test functionality of a event-drive game objects.

    Each test case is provided the following properties::

        self.on_move: The listener mock for the object's on_move event.
        self.on_collider_enter: Listener mock for the on_collider_enter event.
        self.physics: The mock for the object's physics.
        self.game_object: A GameObject at (1,2) with geometry states:

            {
                'default': Rectangle(x=1, y=2, width=3, height=4)
            }
    """

    def setUp(self):
        geometry_states = {
            'default': Rectangle(x=1,  y=2,  width=3,  height=4),
            'x10':     Rectangle(x=10, y=20, width=30, height=40),
        }

        self.on_collider_enter = Mock()
        self.on_move = Mock()
        self.physics = Mock()
        self.game_object = GameObject(
            geometry_states, x=1, y=2, physics=self.physics)
        self.game_object.add_listeners(
            on_move=self.on_move, on_collider_enter=self.on_collider_enter)

    def test_create_game_object(self):
        """Creates a GameObject and verifies its attributes."""
        geometry_states = {
            'default': Rectangle(x=1, y=2, width=3, height=4)
        }
        physics_mock = Mock()

        game_object = GameObject(geometry_states, x=5, y=6,
                                 physics=physics_mock)
        self.assertEqual(5, game_object.x)
        self.assertEqual(6, game_object.y)
        self.assertEqual(3, game_object.width)
        self.assertEqual(4, game_object.height)

    def test_coordinates_are_read_only(self):
        """Coordinates are read-only."""
        with self.assertRaises(AttributeError):
            self.game_object.coordinates = (100, 200)
        self.game_object.coordinates.x = 300
        self.game_object.coordinates.y = 400
        self.assertEqual(1, self.game_object.x)
        self.assertEqual(2, self.game_object.y)
        self.assertEqual(1, self.game_object.coordinates.x)
        self.assertEqual(2, self.game_object.coordinates.y)

    def test_set_x(self):
        """Setting x coordinate triggers an on_move event."""
        self.game_object.x = 100
        self.assertEqual(100, self.game_object.x)
        self.assertEqual(2, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)
        self.on_move.assert_called_once_with((100, 2))

    def test_set_x_no_change(self):
        """No on_move event is fired when x value does not change."""
        self.game_object.x = 1
        self.assertEqual(1, self.game_object.x)
        self.assertEqual(2, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)
        self.on_move.assert_not_called()

    def test_set_y(self):
        """Setting y coordinate triggers an on_move event."""
        self.game_object.y = 100
        self.assertEqual(1, self.game_object.x)
        self.assertEqual(100, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)
        self.on_move.assert_called_once_with((1, 100))

    def test_set_y_no_change(self):
        """No on_move event is fired when y value does not change."""
        self.game_object.y = 2
        self.assertEqual(1, self.game_object.x)
        self.assertEqual(2, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)
        self.on_move.assert_not_called()

    def test_set_position(self):
        """Setting position triggers an on_move event."""
        self.game_object.set_position((100, 200))
        self.assertEqual(100, self.game_object.x)
        self.assertEqual(200, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)
        self.on_move.assert_called_once_with((100, 200))

    def test_set_position_no_change(self):
        """No on_move event is fired when position does not change."""
        self.game_object.set_position((1, 2))
        self.assertEqual(1, self.game_object.x)
        self.assertEqual(2, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)
        self.on_move.assert_not_called()

    def test_update_game_object_without_physics(self):
        """Updating without physics does nothing."""
        geometry_states = {
            'default': Rectangle(x=1, y=2, width=3, height=4)
        }

        game_object = GameObject(geometry_states, x=5, y=6, physics=None)
        game_object.update(1000)
        self.assertEqual(5, game_object.x)
        self.assertEqual(6, game_object.y)

    def test_update_game_object_with_physics(self):
        """Updating with physics applies velocity to coordinates."""
        self.physics.velocity.x = 4
        self.physics.velocity.y = 8

        self.game_object.update(1000)
        self.assertEqual(1 + 4, self.game_object.x)
        self.assertEqual(2 + 8, self.game_object.y)
        self.physics.run_simulation.assert_called_once_with(1000)

    def test_set_geometry_state(self):
        """Setting geometry state updates dimensions but not coordinates."""
        self.assertEqual(1, self.game_object.x)
        self.assertEqual(2, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)

        self.game_object.set_geometry_state('x10')
        self.assertEqual(1, self.game_object.x)
        self.assertEqual(2, self.game_object.y)
        self.assertEqual(30, self.game_object.width)
        self.assertEqual(40, self.game_object.height)
