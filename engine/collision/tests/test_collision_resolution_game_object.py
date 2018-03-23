from ..collision_resolution_game_object import resolve_game_object_collision
from ..collision_resolution_game_object import resolve_game_object_x_collision
from ..collision_resolution_game_object import resolve_game_object_y_collision
from unittest.mock import Mock, patch
import unittest


class TestResolveGameObjectCollision(unittest.TestCase):
    """Test functionality of resolve_game_object_collision function."""

    collision_2d_module = 'engine.collision.collision_resolution_game_object'

    @patch(collision_2d_module + '.get_nonoverlapping_coordinates_2d')
    def test_neither_have_physics(self, mock_2d_resolve):
        """Objects are not moved when neither has physics."""
        first = Mock(physics=None)
        second = Mock(physics=None)

        self.assertFalse(resolve_game_object_collision(first, second),
                         "True returned when no collision was resolved")
        mock_2d_resolve.assert_not_called()
        first.assert_not_called()
        second.assert_not_called()

    @patch(collision_2d_module + '.get_nonoverlapping_coordinates_2d')
    def test_first_has_no_physics(self, mock_2d_resolve):
        """Second object is moved when first object has no physics."""
        first = Mock(physics=None)
        second = Mock(physics=Mock(velocity=Mock()))

        mock_2d_resolve.return_value = (1, 2)
        self.assertTrue(resolve_game_object_collision(first, second),
                        "False returned when collision was resolved")

        mock_2d_resolve.assert_called_once_with(
            second, second.physics.velocity, first)
        first.set_position.assert_not_called()
        second.set_position.assert_called_once_with((1, 2))

    @patch(collision_2d_module + '.get_nonoverlapping_coordinates_2d')
    def test_second_has_no_physics(self, mock_2d_resolve):
        """First object is moved when second object has no physics."""
        first = Mock(physics=Mock(velocity=Mock()))
        second = Mock(physics=None)

        mock_2d_resolve.return_value = (1, 2)
        self.assertTrue(resolve_game_object_collision(first, second),
                        "False returned when collision was resolved")

        mock_2d_resolve.assert_called_once_with(
            first, first.physics.velocity, second)
        first.set_position.assert_called_once_with((1, 2))
        second.set_position.assert_not_called()

    @patch(collision_2d_module + '.resolve_game_object_y_collision')
    @patch(collision_2d_module + '.resolve_game_object_x_collision')
    @patch(collision_2d_module + '.get_nonoverlapping_coordinates_2d')
    @patch(collision_2d_module + '.detect_overlap_2d')
    def test_no_overlap(self, mock_2d_detect, mock_2d_resolve,
                        mock_x_resolve, mock_y_resolve):
        """No work is performed if neither object overlaps."""
        first = Mock(physics=Mock(velocity=Mock()))
        second = Mock(physics=Mock(velocity=Mock()))

        mock_2d_detect.return_value = False
        self.assertFalse(resolve_game_object_collision(first, second),
                         "True returned when no overlap exists")

        mock_2d_detect.assert_called_once_with(first, second)
        mock_2d_resolve.assert_not_called()
        mock_x_resolve.assert_not_called()
        mock_y_resolve.assert_not_called()
        first.set_position.assert_not_called()
        second.set_position.assert_not_called()

    @patch(collision_2d_module + '.resolve_game_object_y_collision')
    @patch(collision_2d_module + '.resolve_game_object_x_collision')
    @patch(collision_2d_module + '.get_nonoverlapping_coordinates_2d')
    @patch(collision_2d_module + '.detect_overlap_2d')
    def test_first_has_lesser_velocity(self, mock_2d_detect, mock_2d_resolve,
                                       mock_x_resolve, mock_y_resolve):
        """Second object moves when absolute velocity is less than first."""
        first = Mock(x=1, y=2, width=3, height=4,
                     physics=Mock(velocity=Mock(x=1, y=1)))
        second = Mock(x=1, y=2, width=3, height=4,
                      physics=Mock(velocity=Mock(x=2, y=2)))

        mock_2d_detect.return_value = True
        self.assertTrue(resolve_game_object_collision(first, second),
                        "False returned when collision was resolved")

        mock_2d_detect.assert_called_once()
        mock_x_resolve.assert_called_once_with(second, first)
        mock_y_resolve.assert_called_once_with(second, first)

        mock_2d_resolve.assert_not_called()
        first.set_position.assert_not_called()
        second.set_position.assert_not_called()

    @patch(collision_2d_module + '.resolve_game_object_y_collision')
    @patch(collision_2d_module + '.resolve_game_object_x_collision')
    @patch(collision_2d_module + '.get_nonoverlapping_coordinates_2d')
    @patch(collision_2d_module + '.detect_overlap_2d')
    def test_first_has_equal_velocity(self, mock_2d_detect, mock_2d_resolve,
                                      mock_x_resolve, mock_y_resolve):
        """Second object moves when absolute velocity is equal to first's."""
        first = Mock(x=1, y=2, width=3, height=4,
                     physics=Mock(velocity=Mock(x=-1, y=1)))
        second = Mock(x=1, y=2, width=3, height=4,
                      physics=Mock(velocity=Mock(x=1, y=-1)))

        mock_2d_detect.return_value = True
        self.assertTrue(resolve_game_object_collision(first, second),
                        "False returned when collision was resolved")

        mock_2d_detect.assert_called_once()
        mock_x_resolve.assert_called_once_with(second, first)
        mock_y_resolve.assert_called_once_with(second, first)

        mock_2d_resolve.assert_not_called()
        first.set_position.assert_not_called()
        second.set_position.assert_not_called()

    @patch(collision_2d_module + '.resolve_game_object_y_collision')
    @patch(collision_2d_module + '.resolve_game_object_x_collision')
    @patch(collision_2d_module + '.get_nonoverlapping_coordinates_2d')
    @patch(collision_2d_module + '.detect_overlap_2d')
    def test_first_has_greater_velocity(self, mock_2d_detect, mock_2d_resolve,
                                        mock_x_resolve, mock_y_resolve):
        """First object moves when absolute velocity is less than second's."""
        first = Mock(x=1, y=2, width=3, height=4,
                     physics=Mock(velocity=Mock(x=-2, y=-2)))
        second = Mock(x=1, y=2, width=3, height=4,
                      physics=Mock(velocity=Mock(x=1, y=1)))

        mock_2d_detect.return_value = True
        self.assertTrue(resolve_game_object_collision(first, second),
                        "False returned when collision was resolved")

        mock_2d_detect.assert_called_once()
        mock_x_resolve.assert_called_once_with(first, second)
        mock_y_resolve.assert_called_once_with(first, second)

        mock_2d_resolve.assert_not_called()
        first.set_position.assert_not_called()
        second.set_position.assert_not_called()

    @patch(collision_2d_module + '.get_nonoverlapping_coordinates_2d')
    def test_x_velocity_is_reset_moving_along_x_axis(self, mock_2d_resolve):
        """First object's x velocity is cancelled when moved along x axis."""
        first = Mock(x=1, y=2, coordinates=(1, 2),
                     physics=Mock(
                         velocity=Mock(x=10, y=20),
                         acceleration=Mock(x=10, y=20)))
        second = Mock(physics=None)

        mock_2d_resolve.return_value = (3, 2)
        self.assertTrue(resolve_game_object_collision(first, second),
                        "False returned when collision was resolved")

        self.assertEqual(0, first.physics.velocity.x, "X velocity not reset")
        self.assertEqual(20, first.physics.velocity.y, "Y velocity was reset")
        self.assertEqual(0, first.physics.acceleration.x, "X accel not reset")
        self.assertEqual(20, first.physics.acceleration.y, "Y accel was reset")

    @patch(collision_2d_module + '.get_nonoverlapping_coordinates_2d')
    def test_y_velocity_is_reset_moving_along_y_axis(self, mock_2d_resolve):
        """First object's y velocity is cancelled when moved along y axis."""
        first = Mock(x=1, y=2, coordinates=(1, 2),
                     physics=Mock(
                         velocity=Mock(x=10, y=20),
                         acceleration=Mock(x=10, y=20)))
        second = Mock(physics=None)

        mock_2d_resolve.return_value = (1, 3)
        self.assertTrue(resolve_game_object_collision(first, second),
                        "False returned when collision was resolved")

        self.assertEqual(10, first.physics.velocity.x, "X velocity was reset")
        self.assertEqual(0, first.physics.velocity.y, "Y velocity not reset")
        self.assertEqual(10, first.physics.acceleration.x, "X accel was reset")
        self.assertEqual(0, first.physics.acceleration.y, "Y accel not reset")

    @patch(collision_2d_module + '.get_nonoverlapping_coordinate_1d')
    @patch(collision_2d_module + '.detect_overlap_1d')
    def test_resolve_x_collision_no_overlap(self, mock_1d_detect,
                                            mock_1d_resolve):
        """Resolving x axis does nothing if no overlap exists."""
        first = Mock(x=1, y=2, width=3, height=4,
                     physics=Mock(
                         velocity=Mock(x=1, y=2),
                         acceleration=Mock(x=1, y=2)))
        second = Mock(x=1, y=2, width=3, height=4,
                      physics=Mock(
                         velocity=Mock(x=1, y=2),
                         acceleration=Mock(x=1, y=2)))

        mock_1d_detect.return_value = False
        resolve_game_object_x_collision(first, second)

        mock_1d_detect.assert_called_once_with(
            first.y - first.physics.velocity.y, first.height,
            second.y, second.height)

        mock_1d_resolve.assert_not_called()

        self.assertEqual(
            (1, 2, 3, 4),
            (first.x, first.y, first.width, first.height))
        self.assertEqual(
            (1, 2),
            (first.physics.velocity.x, first.physics.velocity.y))
        self.assertEqual(
            (1, 2),
            (first.physics.acceleration.x, first.physics.acceleration.y))

        self.assertEqual(
            (1, 2, 3, 4),
            (second.x, second.y, second.width, second.height))
        self.assertEqual(
            (1, 2),
            (second.physics.velocity.x, second.physics.velocity.y))
        self.assertEqual(
            (1, 2),
            (second.physics.acceleration.x, second.physics.acceleration.y))

    @patch(collision_2d_module + '.get_nonoverlapping_coordinate_1d')
    @patch(collision_2d_module + '.detect_overlap_1d')
    def test_resolve_x_collision_with_overlap(self, mock_1d_detect,
                                              mock_1d_resolve):
        """Resolving x axis repositions x coordinate if overlap exists."""
        first = Mock(x=1, y=2, width=3, height=4,
                     physics=Mock(
                         velocity=Mock(x=1, y=2),
                         acceleration=Mock(x=1, y=2)))
        second = Mock(x=1, y=2, width=3, height=4,
                      physics=Mock(
                         velocity=Mock(x=1, y=2),
                         acceleration=Mock(x=1, y=2)))

        mock_1d_detect.return_value = True
        mock_1d_resolve.return_value = 10
        resolve_game_object_x_collision(first, second)

        mock_1d_detect.assert_called_once_with(
            first.y - first.physics.velocity.y, first.height,
            second.y, second.height)

        # Hardcode original values because this method has side effects
        mock_1d_resolve.assert_called_once_with(1, 3, 1, 1, 3)

        self.assertEqual(
            (10, 2, 3, 4),
            (first.x, first.y, first.width, first.height))
        self.assertEqual(
            (0, 2),
            (first.physics.velocity.x, first.physics.velocity.y))
        self.assertEqual(
            (0, 2),
            (first.physics.acceleration.x, first.physics.acceleration.y))

        self.assertEqual(
            (1, 2, 3, 4),
            (second.x, second.y, second.width, second.height))
        self.assertEqual(
            (1, 2),
            (second.physics.velocity.x, second.physics.velocity.y))
        self.assertEqual(
            (1, 2),
            (second.physics.acceleration.x, second.physics.acceleration.y))

    @patch(collision_2d_module + '.get_nonoverlapping_coordinate_1d')
    @patch(collision_2d_module + '.detect_overlap_1d')
    def test_resolve_y_collision_no_overlap(self, mock_1d_detect,
                                            mock_1d_resolve):
        """Resolving y axis does nothing if no overlap exists."""
        first = Mock(x=1, y=2, width=3, height=4,
                     physics=Mock(
                         velocity=Mock(x=1, y=2),
                         acceleration=Mock(x=1, y=2)))
        second = Mock(x=1, y=2, width=3, height=4,
                      physics=Mock(
                         velocity=Mock(x=1, y=2),
                         acceleration=Mock(x=1, y=2)))

        mock_1d_detect.return_value = False
        resolve_game_object_y_collision(first, second)

        mock_1d_detect.assert_called_once_with(first.x, first.width,
                                               second.x, second.width)

        mock_1d_resolve.assert_not_called()

        self.assertEqual(
            (1, 2, 3, 4),
            (first.x, first.y, first.width, first.height))
        self.assertEqual(
            (1, 2),
            (first.physics.velocity.x, first.physics.velocity.y))
        self.assertEqual(
            (1, 2),
            (first.physics.acceleration.x, first.physics.acceleration.y))

        self.assertEqual(
            (1, 2, 3, 4),
            (second.x, second.y, second.width, second.height))
        self.assertEqual(
            (1, 2),
            (second.physics.velocity.x, second.physics.velocity.y))
        self.assertEqual(
            (1, 2),
            (second.physics.acceleration.x, second.physics.acceleration.y))

    @patch(collision_2d_module + '.get_nonoverlapping_coordinate_1d')
    @patch(collision_2d_module + '.detect_overlap_1d')
    def test_resolve_y_collision_with_overlap(self, mock_1d_detect,
                                              mock_1d_resolve):
        """Resolving y axis repositions y coordinate if overlap exists."""
        first = Mock(x=1, y=2, width=3, height=4,
                     physics=Mock(
                         velocity=Mock(x=1, y=2),
                         acceleration=Mock(x=1, y=2)))
        second = Mock(x=1, y=2, width=3, height=4,
                      physics=Mock(
                         velocity=Mock(x=1, y=2),
                         acceleration=Mock(x=1, y=2)))

        mock_1d_detect.return_value = True
        mock_1d_resolve.return_value = 20
        resolve_game_object_y_collision(first, second)

        mock_1d_detect.assert_called_once_with(first.x, first.width,
                                               second.x, second.width)

        # Hardcode original values because this method has side effects
        mock_1d_resolve.assert_called_once_with(2, 4, 2, 2, 4)

        self.assertEqual(
            (1, 20, 3, 4),
            (first.x, first.y, first.width, first.height))
        self.assertEqual(
            (1, 0),
            (first.physics.velocity.x, first.physics.velocity.y))
        self.assertEqual(
            (1, 0),
            (first.physics.acceleration.x, first.physics.acceleration.y))

        self.assertEqual(
            (1, 2, 3, 4),
            (second.x, second.y, second.width, second.height))
        self.assertEqual(
            (1, 2),
            (second.physics.velocity.x, second.physics.velocity.y))
        self.assertEqual(
            (1, 2),
            (second.physics.acceleration.x, second.physics.acceleration.y))
