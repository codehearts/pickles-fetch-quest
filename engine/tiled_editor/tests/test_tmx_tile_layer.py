from ..tmx_tile_layer import load_tmx_tile_layer
from defusedxml import ElementTree
from io import StringIO
import unittest


class TestTmxTileLayer(unittest.TestCase):
    """Test loading TMX tile layer entries."""

    def test_flips_y_coordinate(self):
        """Y coordinates are flipped to place origin at bottom left."""
        mock_xml = '<layer width="3" height="2">\n'
        mock_xml += '\t<data encoding="csv">\n'
        mock_xml += '\t\t1,2,3,\n'
        mock_xml += '\t\t4,5,6\n'
        mock_xml += '\t</data>\n'
        mock_xml += '</layer>'
        tile_layer_node = ElementTree.parse(StringIO(mock_xml)).getroot()

        # Right-up order: (0, 0) is the top left corner of the map
        expected = [
            (0, 1, 1), (1, 1, 2),
            (2, 1, 3), (0, 0, 4),
            (1, 0, 5), (2, 0, 6)]

        # Load the tile layer
        actual = list(load_tmx_tile_layer(tile_layer_node))

        self.assertEqual(expected, actual)
