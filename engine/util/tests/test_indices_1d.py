from ..indices_1d import flip_1d_index_vertically
import unittest


class Test1dIndicesUtils(unittest.TestCase):
    """Test one dimensional indices utility functions."""

    def test_flip_1d_index_vertically(self):
        """Gives index for corresponding value in vertically flipped matrix."""
        rows = 3
        columns = 4

        original_list = [
            1, 2, 3, 4,
            5, 6, 7, 8,
            9, 10, 11, 12]

        expected_list = [
            9, 10, 11, 12,
            5, 6, 7, 8,
            1, 2, 3, 4]

        def convert(i):
            return original_list[flip_1d_index_vertically(i, rows, columns)]

        actual_list = [convert(index) for index in range(rows * columns)]

        self.assertEqual(expected_list, actual_list)
