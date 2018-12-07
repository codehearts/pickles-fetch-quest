from ..collision_resolution_2d import get_nonoverlapping_coordinates_2d
from unittest.mock import call, Mock, patch
import unittest


class TestGetNonOverlappingCoordinates2d(unittest.TestCase):
    """Test functionality of get_nonoverlapping_coordinates_2d function."""

    collision_2d_module = 'engine.collision.collision_resolution_2d'

    @patch(collision_2d_module + '.get_nonoverlapping_coordinate_1d')
    @patch('engine.geometry.detect_overlap_1d')
    def test_2d_no_overlap(self, mock_1d_detect, mock_1d_resolution):
        """First rectangle is not moved if no overlap exists."""
        # Before    Current   After
        #
        # 3|11..    3|11..    3|11..
        # 2|1122 => 2|1122 => 2|1122
        # 1|..22    1|..22    1|..22
        #   ----      ----      ----
        #   1234      1234      1234
        first = Mock()
        first.x, first.y = 1, 2
        first.width, first.height = 2, 2

        second = Mock()
        second.x, second.y = 3, 1
        second.width, second.height = 2, 2

        first_velocity = Mock()
        first_velocity.x, first_velocity.y = 10, 20

        mock_1d_detect.side_effect = [False, False]  # Return value sequence

        actual = get_nonoverlapping_coordinates_2d(
            first, first_velocity, second)

        self.assertEqual((first.x, first.y), actual, "Coordinates were moved")

        mock_1d_detect.assert_has_calls([
            call(first.y - first_velocity.y, first.height,
                 second.y, second.height),
            call(first.x, first.width,
                 second.x, second.width)])

        mock_1d_resolution.assert_not_called()

    @patch(collision_2d_module + '.get_nonoverlapping_coordinate_1d')
    @patch('engine.geometry.detect_overlap_1d')
    def test_2d_overlap_on_y_not_x(self, mock_1d_detect, mock_1d_resolution):
        """First rectangle is moved on x-axis if overlap exists on y-axis."""
        # Before    Current   After
        #
        # 4|11..    4|....    4|....
        # 3|1122 => 3|..22 => 3|..22
        # 2|..22    2|.1x2    2|1122
        # 1|....    1|.11.    1|11..
        #   ----      ----      ----
        #   1234      1234      1234
        first = Mock()
        first.x, first.y = 2, 1
        first.width, first.height = 2, 2

        second = Mock()
        second.x, second.y = 3, 3
        second.width, second.height = 2, 2

        first_velocity = Mock()
        first_velocity.x, first_velocity.y = 1, -2

        mock_1d_detect.side_effect = [True, False]  # Return value sequence
        mock_1d_resolution.return_value = 1

        actual = get_nonoverlapping_coordinates_2d(
            first, first_velocity, second)

        self.assertEqual((1, first.y), actual,
                         "X coordinate was not moved based on 1d resolution")

        mock_1d_detect.assert_has_calls([
            call(first.y - first_velocity.y, first.height,
                 second.y, second.height),
            call(1, first.width,
                 second.x, second.width)])

        mock_1d_resolution.assert_called_once_with(first.x, first.width,
                                                   first_velocity.x,
                                                   second.x, second.width)

    @patch(collision_2d_module + '.get_nonoverlapping_coordinate_1d')
    @patch('engine.geometry.detect_overlap_1d')
    def test_2d_overlap_on_x_not_y(self, mock_1d_detect, mock_1d_resolution):
        """First rectangle is moved on y-axis if overlap exists on x-axis."""
        # Before    Current   After
        #
        # 4|..22    4|..22    4|..22
        # 3|..22 => 3|.1x2 => 3|..22
        # 2|11..    2|.11.    2|.11.
        # 1|11..    1|....    1|.11.
        #   ----      ----      ----
        #   1234      1234      1234
        first = Mock()
        first.x, first.y = 2, 2
        first.width, first.height = 2, 2

        second = Mock()
        second.x, second.y = 3, 3
        second.width, second.height = 2, 2

        first_velocity = Mock()
        first_velocity.x, first_velocity.y = 1, 1

        mock_1d_detect.side_effect = [False, True]  # Return value sequence
        mock_1d_resolution.return_value = 1

        actual = get_nonoverlapping_coordinates_2d(
            first, first_velocity, second)

        self.assertEqual((first.x, 1), actual,
                         "Y coordinate was not moved based on 1d resolution")

        mock_1d_detect.assert_has_calls([
            call(first.y - first_velocity.y, first.height,
                 second.y, second.height),
            call(first.x, first.width,
                 second.x, second.width)])

        mock_1d_resolution.assert_called_once_with(first.y, first.height,
                                                   first_velocity.y,
                                                   second.y, second.height)
