from ..collision_resolution_game_object import resolve_game_object_collision
from ..collision_resolution_game_object import resolve_game_object_x_collision
from ..collision_resolution_game_object import resolve_game_object_y_collision
from unittest.mock import Mock, patch
import unittest


class TestResolveGameObjectCollision(unittest.TestCase):
    """Test functionality of resolve_game_object_collision function."""

    collision_2d_module = 'engine.collision.collision_resolution_game_object'

    @patch(collision_2d_module + '.resolve_game_object_y_collision')
    @patch(collision_2d_module + '.resolve_game_object_x_collision')
    @patch(collision_2d_module + '.detect_overlap_2d')
    def test_no_overlap(self, mock_2d_detect, mock_x_resolve, mock_y_resolve):
        """No work is performed if neither object overlaps."""
        first = Mock(physics=Mock(velocity=Mock()))
        second = Mock(physics=Mock(velocity=Mock()))

        mock_2d_detect.return_value = False
        self.assertEqual((0, 0), resolve_game_object_collision(first, second))

        mock_2d_detect.assert_called_once_with(first, second)
        mock_x_resolve.assert_not_called()
        mock_y_resolve.assert_not_called()
        first.set_position.assert_not_called()
        second.set_position.assert_not_called()

    @patch(collision_2d_module + '.resolve_game_object_y_collision')
    @patch(collision_2d_module + '.resolve_game_object_x_collision')
    @patch(collision_2d_module + '.detect_overlap_2d')
    def test_first_is_lighter(self, mock_2d_detect, mock_x_resolve,
                              mock_y_resolve):
        """First object moves when mass is less than second's."""
        first = Mock(x=1, y=2, width=3, height=4,
                     physics=Mock(mass=1, velocity=Mock(x=1, y=2)))
        second = Mock(x=1, y=2, width=3, height=4,
                      physics=Mock(mass=2, velocity=Mock(x=1, y=2)))

        mock_2d_detect.return_value = True
        mock_x_resolve.return_value = 1
        mock_y_resolve.return_value = 2
        self.assertEqual((1, 2), resolve_game_object_collision(first, second))

        mock_2d_detect.assert_called_once()
        mock_x_resolve.assert_called_once_with(first, second)
        mock_y_resolve.assert_called_once_with(first, second)

        first.set_position.assert_not_called()
        second.set_position.assert_not_called()

    @patch(collision_2d_module + '.resolve_game_object_y_collision')
    @patch(collision_2d_module + '.resolve_game_object_x_collision')
    @patch(collision_2d_module + '.detect_overlap_2d')
    def test_first_has_equal_mass(self, mock_2d_detect, mock_x_resolve,
                                  mock_y_resolve):
        """First object moves when mass is equal to second's."""
        first = Mock(x=1, y=2, width=3, height=4,
                     physics=Mock(mass=1, velocity=Mock(x=-1, y=2)))
        second = Mock(x=1, y=2, width=3, height=4,
                      physics=Mock(mass=1, velocity=Mock(x=1, y=2)))

        mock_2d_detect.return_value = True
        mock_x_resolve.return_value = 1
        mock_y_resolve.return_value = 2
        self.assertEqual((1, 2), resolve_game_object_collision(first, second))

        mock_2d_detect.assert_called_once()
        mock_x_resolve.assert_called_once_with(first, second)
        mock_y_resolve.assert_called_once_with(first, second)

        first.set_position.assert_not_called()
        second.set_position.assert_not_called()

    @patch(collision_2d_module + '.resolve_game_object_y_collision')
    @patch(collision_2d_module + '.resolve_game_object_x_collision')
    @patch(collision_2d_module + '.detect_overlap_2d')
    def test_first_is_heavier(self, mock_2d_detect, mock_x_resolve,
                              mock_y_resolve):
        """Second object moves when mass is less than first's."""
        first = Mock(x=1, y=2, width=3, height=4,
                     physics=Mock(mass=2, velocity=Mock(x=-1, y=-2)))
        second = Mock(x=1, y=2, width=3, height=4,
                      physics=Mock(mass=1, velocity=Mock(x=1, y=2)))

        mock_2d_detect.return_value = True
        mock_x_resolve.return_value = 1
        mock_y_resolve.return_value = 2
        self.assertEqual((1, 2), resolve_game_object_collision(first, second))

        mock_2d_detect.assert_called_once()
        mock_x_resolve.assert_called_once_with(second, first)
        mock_y_resolve.assert_called_once_with(second, first)

        first.set_position.assert_not_called()
        second.set_position.assert_not_called()

    @patch(collision_2d_module + '.get_nonoverlapping_coordinate_1d')
    @patch(collision_2d_module + '.detect_overlap_1d')
    def test_velocity_is_reset_along_x(self, mock_1d_detect, mock_1d_resolve):
        """X velocity is cancelled when moved along x axis."""
        moving = Mock(
            x=1, y=2, width=3, height=4,
            physics=Mock(
                velocity=Mock(x=10, y=20),
                acceleration=Mock(x=10, y=20)))

        resting = Mock(
            x=1, y=2, width=3, height=4,
            physics=Mock(
                velocity=Mock(x=10, y=20),
                acceleration=Mock(x=10, y=20)))

        # Resolve the objects along the x axis
        mock_1d_detect.return_value = True
        mock_1d_resolve.return_value = 3
        self.assertEqual(10, resolve_game_object_x_collision(moving, resting))

        # Resolution was performed with correct dimensions
        mock_1d_detect.assert_called_once_with(-18, 4, 2, 4)
        mock_1d_resolve.assert_called_once_with(1, 3, 10, 1, 3)

        # Only the x velocity of the moving object was cancelled
        self.assertEqual(
            (0, 20),
            (moving.physics.velocity.x, moving.physics.velocity.y),
            "Only moving x velocity should have been reset")
        self.assertEqual(
            (0, 20),
            (moving.physics.acceleration.x, moving.physics.acceleration.y),
            "Only moving x acceleration should have been reset")

        # No velocity on the resting object was cancelled
        self.assertEqual(
            (10, 20),
            (resting.physics.velocity.x, resting.physics.velocity.y),
            "Resting velocities should not have been reset")
        self.assertEqual(
            (10, 20),
            (resting.physics.acceleration.x, resting.physics.acceleration.y),
            "Resting accelerations should not have been reset")

    @patch(collision_2d_module + '.get_nonoverlapping_coordinate_1d')
    @patch(collision_2d_module + '.detect_overlap_1d')
    def test_velocity_is_reset_along_y(self, mock_1d_detect, mock_1d_resolve):
        """Y velocity is cancelled when moved along y axis."""
        moving = Mock(
            x=1, y=2, width=3, height=4,
            physics=Mock(
                velocity=Mock(x=10, y=20),
                acceleration=Mock(x=10, y=20)))

        resting = Mock(
            x=1, y=2, width=3, height=4,
            physics=Mock(
                velocity=Mock(x=10, y=20),
                acceleration=Mock(x=10, y=20)))

        # Resolve the objects along the y axis
        mock_1d_detect.return_value = True
        mock_1d_resolve.return_value = 4
        self.assertEqual(20, resolve_game_object_y_collision(moving, resting))

        # Resolution was performed with correct dimensions
        mock_1d_detect.assert_called_once_with(1, 3, 1, 3)
        mock_1d_resolve.assert_called_once_with(2, 4, 20, 2, 4)

        # Only the y velocity of the moving object was cancelled
        self.assertEqual(
            (10, 0),
            (moving.physics.velocity.x, moving.physics.velocity.y),
            "Only moving y velocity should have been reset")
        self.assertEqual(
            (10, 0),
            (moving.physics.acceleration.x, moving.physics.acceleration.y),
            "Only moving y acceleration should have been reset")

        # No velocity on the resting object was cancelled
        self.assertEqual(
            (10, 20),
            (resting.physics.velocity.x, resting.physics.velocity.y),
            "Resting velocities should not have been reset")
        self.assertEqual(
            (10, 20),
            (resting.physics.acceleration.x, resting.physics.acceleration.y),
            "Resting accelerations should not have been reset")

    @patch(collision_2d_module + '.get_nonoverlapping_coordinate_1d')
    @patch(collision_2d_module + '.detect_overlap_1d')
    def test_resolve_x_axis_no_overlap(self, mock_1d_detect, mock_1d_resolve):
        """Resolving x axis does nothing if no overlap exists."""
        moving = Mock(x=1, y=2, width=3, height=4,
                      physics=Mock(velocity=Mock(y=5)))
        resting = Mock(x=10, y=20, width=30, height=40)

        # Resolve the objects along the x axis
        mock_1d_detect.return_value = False
        self.assertEqual(0, resolve_game_object_x_collision(moving, resting))

        mock_1d_detect.assert_called_once_with(-3, 4, 20, 40)
        mock_1d_resolve.assert_not_called()

        # Moving and resting objects were not repositioned
        self.assertEqual(
            (1, 2, 3, 4),
            (moving.x, moving.y, moving.width, moving.height))
        self.assertEqual(
            (10, 20, 30, 40),
            (resting.x, resting.y, resting.width, resting.height))

    @patch(collision_2d_module + '.get_nonoverlapping_coordinate_1d')
    @patch(collision_2d_module + '.detect_overlap_1d')
    def test_object_is_moved_along_x(self, mock_1d_detect, mock_1d_resolve):
        """X coordinate is changed when moved along x axis."""
        moving = Mock(x=1, y=2, width=3, height=4,
                      physics=Mock(velocity=Mock(x=5, y=6)))
        resting = Mock(x=1, y=2, width=3, height=4)

        # Resolve the objects along the x axis
        mock_1d_detect.return_value = True
        mock_1d_resolve.return_value = -2
        self.assertEqual(5, resolve_game_object_x_collision(moving, resting))

        # Resolution was performed with correct dimensions
        mock_1d_detect.assert_called_once_with(-4, 4, 2, 4)
        mock_1d_resolve.assert_called_once_with(1, 3, 5, 1, 3)

        # Only the moving object's x coordinate was repositioned
        self.assertEqual(
            (-2, 2, 3, 4),
            (moving.x, moving.y, moving.width, moving.height))
        self.assertEqual(
            (1, 2, 3, 4),
            (resting.x, resting.y, resting.width, resting.height))

    @patch(collision_2d_module + '.get_nonoverlapping_coordinate_1d')
    @patch(collision_2d_module + '.detect_overlap_1d')
    def test_resolve_y_axis_no_overlap(self, mock_1d_detect, mock_1d_resolve):
        """Resolving y axis does nothing if no overlap exists."""
        moving = Mock(x=1, y=2, width=3, height=4)
        resting = Mock(x=10, y=20, width=30, height=40)

        # Resolve the objects along the y axis
        mock_1d_detect.return_value = False
        self.assertEqual(0, resolve_game_object_y_collision(moving, resting))

        mock_1d_detect.assert_called_once_with(1, 3, 10, 30)
        mock_1d_resolve.assert_not_called()

        # Moving and resting objects were not repositioned
        self.assertEqual(
            (1, 2, 3, 4),
            (moving.x, moving.y, moving.width, moving.height))
        self.assertEqual(
            (10, 20, 30, 40),
            (resting.x, resting.y, resting.width, resting.height))

    @patch(collision_2d_module + '.get_nonoverlapping_coordinate_1d')
    @patch(collision_2d_module + '.detect_overlap_1d')
    def test_object_is_moved_along_y(self, mock_1d_detect, mock_1d_resolve):
        """Y coordinate is changed when moved along y axis."""
        moving = Mock(x=1, y=2, width=3, height=4,
                      physics=Mock(velocity=Mock(y=5)))
        resting = Mock(x=1, y=2, width=3, height=4)

        # Resolve the objects along the y axis
        mock_1d_detect.return_value = True
        mock_1d_resolve.return_value = -2
        self.assertEqual(5, resolve_game_object_y_collision(moving, resting))

        # Resolution was performed with correct dimensions
        mock_1d_detect.assert_called_once_with(1, 3, 1, 3)
        mock_1d_resolve.assert_called_once_with(2, 4, 5, 2, 4)

        # Only the moving object's y coordinate was repositioned
        self.assertEqual(
            (1, -2, 3, 4),
            (moving.x, moving.y, moving.width, moving.height))
        self.assertEqual(
            (1, 2, 3, 4),
            (resting.x, resting.y, resting.width, resting.height))
