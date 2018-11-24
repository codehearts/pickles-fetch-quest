from ..disk_loader import DiskLoader
from unittest.mock import Mock, patch
import unittest
import io


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

    @patch('pyglet.resource.file')
    def test_load_csv(self, mock_file):
        """Loads a CSV file into a two dimensional list."""
        # Stub the file object for the CSV
        csv_iter = (x for x in ('1,2,3', '4,5,6', '-1,-1,-1'))
        mock_file.return_value.__enter__().__iter__ = lambda x: x
        mock_file.return_value.__enter__().__next__ = lambda x: next(csv_iter)

        csv_contents = DiskLoader.load_csv('abc.csv')

        # CSV was opened in readonly mode
        mock_file.assert_called_once_with('abc.csv', mode='r')

        # Returned list is as expected
        self.assertEqual(
            [['1', '2', '3'], ['4', '5', '6'], ['-1', '-1', '-1']],
            csv_contents)

    @patch('pyglet.resource.file')
    def test_load_json(self, mock_file):
        """Loads a JSON file into a dict."""
        # Stub the mock JSON data
        mock_json_data = '{ "a": 1, "b": true, "3": "c" }'
        mock_file.return_value.__enter__().read.return_value = mock_json_data

        json_contents = DiskLoader.load_json('abc.json')

        # JSON was opened in readonly mode
        mock_file.assert_called_once_with('abc.json', mode='r')

        # Returned dict is as expected
        self.assertEqual({'a': 1, 'b': True, '3': 'c'}, json_contents)

    @patch('pyglet.resource.file')
    def test_load_xml(self, mock_file):
        """Loads an XML file into an ElementTree."""
        # Stub the mock XML file
        mock_xml = '<?xml version="1.0" encoding="UTF-8"?>'
        mock_xml += '<data>'
        mock_xml += '\t<element name="first">\n'
        mock_xml += '\t\t<value>1</value>\n'
        mock_xml += '\t</element>\n'
        mock_xml += '\t<element name="second">\n'
        mock_xml += '\t\t<value>2</value>\n'
        mock_xml += '\t</element>\n'
        mock_xml += '</data>'
        mock_file.return_value.__enter__.return_value = io.StringIO(mock_xml)

        root_node = DiskLoader.load_xml('abc.xml')

        # XML was opened in readonly mode
        mock_file.assert_called_once_with('abc.xml', mode='r')

        # The returned tree structure is as expected
        self.assertEqual('data', root_node.tag)

        first_child = list(root_node)[0]
        self.assertEqual('element', first_child.tag)
        self.assertEqual('first', first_child.attrib['name'])

        self.assertEqual('value', list(first_child)[0].tag)
        self.assertEqual('1', list(first_child)[0].text)

        second_child = list(root_node)[1]
        self.assertEqual('element', second_child.tag)
        self.assertEqual('second', second_child.attrib['name'])

        self.assertEqual('value', list(second_child)[0].tag)
        self.assertEqual('2', list(second_child)[0].text)
