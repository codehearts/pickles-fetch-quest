from ..overlap_detection_2d import detect_overlap_2d
from unittest.mock import call, Mock, patch
import unittest


class TestOverlap2d(unittest.TestCase):
    """Test two dimensional overlap detection functions."""

    def setUp(self):
        """Creates a ``self.first`` and ``self.second`` Mock object."""
        self.first = Mock(x=1, y=2, width=3, height=4)
        self.second = Mock(x=5, y=6, width=7, height=8)

    @patch('engine.geometry.overlap_detection_2d.detect_overlap_1d')
    def test_2d_rectangles_no_overlap(self, mock_detect_1d):
        """False when no overlap exists on x and y axes."""
        mock_detect_1d.side_effect = [False, False]  # Return value sequence

        self.assertFalse(detect_overlap_2d(self.first, self.second),
                         "False positive with no axes overlapping")

        mock_detect_1d.assert_has_calls([
            call(self.first.x, self.first.width,
                 self.second.x, self.second.width),
            call(self.first.y, self.first.height,
                 self.second.y, self.second.height),
        ])

    @patch('engine.geometry.overlap_detection_2d.detect_overlap_1d')
    def test_2d_rectangles_x_axis_overlap(self, mock_detect_1d):
        """False when overlap only exists on x axis."""
        mock_detect_1d.side_effect = [True, False]  # Return value sequence

        self.assertFalse(detect_overlap_2d(self.first, self.second),
                         "False positive with only one axis overlapping")

        mock_detect_1d.assert_has_calls([
            call(self.first.x, self.first.width,
                 self.second.x, self.second.width),
            call(self.first.y, self.first.height,
                 self.second.y, self.second.height),
        ])

    @patch('engine.geometry.overlap_detection_2d.detect_overlap_1d')
    def test_2d_rectangles_y_axis_overlap(self, mock_detect_1d):
        """False when overlap only exists on y axis."""
        mock_detect_1d.side_effect = [False, True]  # Return value sequence

        self.assertFalse(detect_overlap_2d(self.first, self.second),
                         "False positive with only one axis overlapping")

        mock_detect_1d.assert_has_calls([
            call(self.first.x, self.first.width,
                 self.second.x, self.second.width),
            call(self.first.y, self.first.height,
                 self.second.y, self.second.height),
        ])

    @patch('engine.geometry.overlap_detection_2d.detect_overlap_1d')
    def test_2d_rectangles_both_axes_overlap(self, mock_detect_1d):
        """True when overlap exists on both axes."""
        mock_detect_1d.side_effect = [True, True]  # Return value sequence

        self.assertTrue(detect_overlap_2d(self.first, self.second),
                        "False negative with only both axes overlapping")

        mock_detect_1d.assert_has_calls([
            call(self.first.x, self.first.width,
                 self.second.x, self.second.width),
            call(self.first.y, self.first.height,
                 self.second.y, self.second.height),
        ])
