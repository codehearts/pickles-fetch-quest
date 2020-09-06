from ..game_object import GameObject
from unittest.mock import Mock
import unittest


class TestGameObject(unittest.TestCase):
    """Test functionality of a event-drive game objects."""

    def setUp(self):
        """Defines the following properties for each test case:

        * self.on_move: Listener mock for on_move.
        * self.on_collider_enter: Listener mock for on_collider_enter.
        * self.game_object: A GameObject at (1,2) with width 3 and height 4.
        """
        self.on_collider_enter = Mock()
        self.on_move = Mock()
        self.physics = Mock()

        self.game_object = GameObject(x=1, y=2, width=3, height=4)
        self.game_object.add_listeners(
            on_move=self.on_move, on_collider_enter=self.on_collider_enter)

    def test_create_game_object(self):
        """Game objects are initialized with the given dimensions."""
        self.assertEqual(1, self.game_object.x)
        self.assertEqual(2, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)

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

    def test_set_x_dispatches_on_move(self):
        """Setting x coordinate triggers an on_move event."""
        self.game_object.x = 100
        self.assertEqual(100, self.game_object.x)
        self.assertEqual(2, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)
        self.on_move.assert_called_once_with((100, 2))

    def test_set_x_no_change_does_not_dispatch_events(self):
        """No event is fired when x value does not change."""
        self.game_object.x = 1
        self.assertEqual(1, self.game_object.x)
        self.assertEqual(2, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)
        self.on_move.assert_not_called()

    def test_set_y_dispatches_on_move(self):
        """Setting y coordinate triggers an on_move event."""
        self.game_object.y = 100
        self.assertEqual(1, self.game_object.x)
        self.assertEqual(100, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)
        self.on_move.assert_called_once_with((1, 100))

    def test_set_y_no_change_does_not_dispatch_events(self):
        """No event is fired when y value does not change."""
        self.game_object.y = 2
        self.assertEqual(1, self.game_object.x)
        self.assertEqual(2, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)
        self.on_move.assert_not_called()

    def test_set_position_dispatches_on_move(self):
        """Setting position dispatches an on_move event."""
        self.game_object.set_position((100, 200))
        self.assertEqual(100, self.game_object.x)
        self.assertEqual(200, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)
        self.on_move.assert_called_once_with((100, 200))

    def test_set_position_no_change_does_not_dispatch(self):
        """No event is fired when position does not change."""
        self.game_object.set_position((1, 2))
        self.assertEqual(1, self.game_object.x)
        self.assertEqual(2, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)
        self.on_move.assert_not_called()

    def test_move_by_dispatches_on_move(self):
        """Setting position relatively dispatches an on_move event."""
        self.game_object.move_by((10, 20))
        self.assertEqual(11, self.game_object.x)
        self.assertEqual(22, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)
        self.on_move.assert_called_once_with((11, 22))


    def test_move_by_no_change_does_not_dispatch(self):
        """No event is fired when relative position does not change."""
        self.game_object.move_by((0, 0))
        self.assertEqual(1, self.game_object.x)
        self.assertEqual(2, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)
        self.on_move.assert_not_called()

    def test_update_game_object_does_nothing(self):
        """Updating a game object does nothing."""
        self.game_object.update(1000)
        self.assertEqual(1, self.game_object.x)
        self.assertEqual(2, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)

        self.assertEqual(1, self.game_object.x)
        self.assertEqual(2, self.game_object.y)
        self.assertEqual(3, self.game_object.width)
        self.assertEqual(4, self.game_object.height)
