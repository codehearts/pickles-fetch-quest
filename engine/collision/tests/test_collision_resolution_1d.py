from ..collision_resolution_1d import get_nonoverlapping_coordinate_1d
from unittest.mock import patch
import unittest


class TestGetNonOverlappingCoordinate1d(unittest.TestCase):
    """Test functionality of get_nonoverlapping_coordinate_1d function."""

    @patch('engine.geometry.detect_overlap_1d')
    def test_1d_no_collision(self, mock_overlap):
        """Non-overlapping lines resolve to original position."""
        mock_overlap.return_value = False
        actual = get_nonoverlapping_coordinate_1d(
            first=0, first_length=5, first_velocity=0,
            second=10, second_length=15)
        self.assertEqual(0, actual, "First line was repositioned")
        mock_overlap.assert_called_once_with(0, 5, 10, 15)

    @patch('engine.geometry.detect_overlap_1d')
    def test_1d_collision_negative_velocity(self, mock_overlap):
        """First line should be moved forward with negative velocity."""
        mock_overlap.return_value = True
        actual = get_nonoverlapping_coordinate_1d(
            first=0, first_length=10, first_velocity=-5,
            second=5, second_length=15)
        self.assertEqual(20, actual, "First line was not moved forward")
        mock_overlap.assert_called_once_with(0, 10, 5, 15)

    @patch('engine.geometry.detect_overlap_1d')
    def test_1d_collision_zero_velocity(self, mock_overlap):
        """First line should be moved back with zero velocity."""
        mock_overlap.return_value = True
        actual = get_nonoverlapping_coordinate_1d(
            first=0, first_length=10, first_velocity=0,
            second=5, second_length=15)
        self.assertEqual(-5, actual, "First line was not moved back")
        mock_overlap.assert_called_once_with(0, 10, 5, 15)

    @patch('engine.geometry.detect_overlap_1d')
    def test_1d_collision_positive_velocity(self, mock_overlap):
        """First line should be moved back with positive velocity."""
        mock_overlap.return_value = True
        actual = get_nonoverlapping_coordinate_1d(
            first=0, first_length=10, first_velocity=5,
            second=5, second_length=15)
        self.assertEqual(-5, actual, "First line was not moved back")
        mock_overlap.assert_called_once_with(0, 10, 5, 15)
