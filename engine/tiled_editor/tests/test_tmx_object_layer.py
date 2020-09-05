from ..tmx_object_layer import load_tmx_object_layer
from defusedxml import ElementTree
from io import StringIO
import unittest


class TestTmxObjectLayer(unittest.TestCase):
    """Test loading TMX object layer entries."""

    def test_flips_y_coordinate(self):
        """Y coordinates are flipped so the origin is at the bottom left."""
        mock_xml = '<objectgroup>\n'
        mock_xml += '\t<object type="a" x="1" y="2" width="3" height="4"/>\n'
        mock_xml += '\t<object type="b" x="5" y="6" width="7" height="8"/>\n'
        mock_xml += '</objectgroup>'
        object_layer_node = ElementTree.parse(StringIO(mock_xml)).getroot()

        width = 10
        height = 20

        # Right-down order: (0, 0) is the top left corner of the map
        expected = [
            {'type': 'a', 'x': 1, 'y': height - 2, 'width': 3, 'height': 4},
            {'type': 'b', 'x': 5, 'y': height - 6, 'width': 7, 'height': 8}]

        # Load the object layer
        actual = list(
            load_tmx_object_layer(
                width, height, object_layer_node, {}))

        self.assertEqual(expected, actual)

    def test_provides_tile_for_tile_objects(self):
        """Tile objects have a special tile property."""
        mock_xml = '<objectgroup>\n'
        mock_xml += '\t<object gid="1" x="1" y="2" width="3" height="4"/>\n'
        mock_xml += '\t<object gid="2" x="5" y="6" width="7" height="8"/>\n'
        mock_xml += '</objectgroup>'
        object_layer_node = ElementTree.parse(StringIO(mock_xml)).getroot()

        tile_objects = {1: 'a', 2: 'b'}
        width = 10
        height = 20

        # Right-down order: (0, 0) is the top left corner of the map
        expected = [{
                'type': 'a',
                'x': 1,
                'y': height - 2 + 4,  # Tile objects have their height added
                'width': 3,
                'height': 4,
                'tile': 1
            }, {
                'type': 'b',
                'x': 5,
                'y': height - 6 + 8,
                'width': 7,
                'height': 8,
                'tile': 2
        }]

        # Load the object layer
        actual = list(
            load_tmx_object_layer(
                width, height, object_layer_node, tile_objects))

        self.assertEqual(expected, actual)
