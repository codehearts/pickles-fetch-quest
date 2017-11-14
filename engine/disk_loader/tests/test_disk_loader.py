from ..disk_loader import DiskLoader
from unittest.mock import patch
import unittest


class TestDiskLoader(unittest.TestCase):
    """Test loading resources from disk."""

    @patch('pyglet.resource')
    def test_set_resource_paths(self, mock_resource):
        """Sets paths and reindexes."""
        test_paths = ['a', 'b', 'c']
        DiskLoader.set_resource_paths(test_paths)
        self.assertEqual(test_paths, mock_resource.path)
        mock_resource.reindex.assert_called()

    @patch('pyglet.resource.image', return_value='image loaded')
    def test_load_image(self, mock_image):
        """Loads an image resource from disk."""
        image = DiskLoader.load_image('abc.png')
        mock_image.assert_called_once_with('abc.png')
        self.assertEqual('image loaded', image)
