from ..overlap_detection_1d import detect_overlap_1d
import unittest


class TestOverlap1d(unittest.TestCase):
    """Test one dimensional overlap detection functions."""

    def test_1d_lines_no_overlap_first_lt_second(self):
        """False when first < second line with no overlap."""
        # first:  123---
        # second: ---456
        actual = detect_overlap_1d(
            first=1, first_length=3, second=4, second_length=3)
        self.assertFalse(actual, "False positive with first < second")

    def test_1d_lines_no_overlap_second_lt_first(self):
        """False when second < first line with no overlap."""
        # first:  ---456
        # second: 123---
        actual = detect_overlap_1d(
            first=4, first_length=3, second=1, second_length=3)
        self.assertFalse(actual, "False positive with second < first")

    def test_1d_lines_boundary_overlap_first_lt_second(self):
        """True when first < second line with edges overlapping."""
        # first:  123--
        # second: --345
        actual = detect_overlap_1d(
            first=1, first_length=3, second=3, second_length=3)
        self.assertTrue(actual, "False negative with first < second")

    def test_1d_lines_boundary_overlap_second_lt_first(self):
        """True when second < first line with edges overlapping."""
        # first:  --345
        # second: 123--
        actual = detect_overlap_1d(
            first=3, first_length=3, second=1, second_length=3)
        self.assertTrue(actual, "False negative with second < first")

    def test_1d_lines_boundary_overlap_first_within_second(self):
        """True when first line is contained within second."""
        # first:  -234-
        # second: 12345
        actual = detect_overlap_1d(
            first=2, first_length=3, second=1, second_length=5)
        self.assertTrue(actual, "False negative with first within second")

    def test_1d_lines_boundary_overlap_second_within_first(self):
        """True when second line is contained within first."""
        # first:  12345
        # second: -234-
        actual = detect_overlap_1d(
            first=1, first_length=5, second=2, second_length=3)
        self.assertTrue(actual, "False negative with second within first")
