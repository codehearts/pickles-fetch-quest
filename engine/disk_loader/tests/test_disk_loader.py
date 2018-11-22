from ..disk_loader import DiskLoader
from unittest.mock import Mock, patch
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

    @patch('pyglet.resource.image')
    def test_load_image(self, mock_image):
        """Loads an image resource from disk."""
        image = DiskLoader.load_image('abc.png')
        mock_image.assert_called_once_with('abc.png')
        self.assertEqual(mock_image.return_value, image)

    @patch('pyglet.image.ImageGrid')
    @patch('pyglet.resource.image')
    def test_load_image_grid(self, mock_image, mock_image_grid):
        """Loads an image grid resource from disk."""
        image_grid = DiskLoader.load_image_grid('abc.png', 2, 8)
        mock_image.assert_called_once_with('abc.png')
        mock_image_grid.assert_called_once_with(mock_image.return_value, 2, 8)

        self.assertEqual(mock_image_grid.return_value, image_grid)

    @patch('pyglet.image.ImageGrid')
    @patch('pyglet.resource.image')
    def test_load_image_grid_passes_kwargs(self, mock_image, mock_image_grid):
        """Image grid loading supports all kwargs."""
        mock_item_width = Mock()
        mock_item_height = Mock()
        mock_row_padding = Mock()
        mock_column_padding = Mock()
        DiskLoader.load_image_grid(
            'abc.png', 2, 8,
            item_width=mock_item_width, item_height=mock_item_height,
            row_padding=mock_row_padding, column_padding=mock_column_padding)

        mock_image_grid.assert_called_once_with(
            mock_image.return_value, 2, 8,
            item_width=mock_item_width, item_height=mock_item_height,
            row_padding=mock_row_padding, column_padding=mock_column_padding)

    @patch('pyglet.resource.media')
    def test_load_audio_with_streaming(self, mock_audio):
        """Loads an audio resource from disk with streaming enabled."""
        audio = DiskLoader.load_audio('abc.wav', streaming=True)
        mock_audio.assert_called_once_with('abc.wav', streaming=True)
        self.assertEqual(mock_audio.return_value, audio)

    @patch('pyglet.resource.media')
    def test_load_audio_without_streaming(self, mock_audio):
        """Loads an audio resource from disk entirely into memory."""
        audio = DiskLoader.load_audio('abc.wav', streaming=False)
        mock_audio.assert_called_once_with('abc.wav', streaming=False)
        self.assertEqual(mock_audio.return_value, audio)
