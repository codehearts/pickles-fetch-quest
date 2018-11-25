from ..tmx_tileset import load_tmx_tileset
from defusedxml import ElementTree
from io import StringIO
from unittest.mock import patch
import unittest


class TestTmxTileset(unittest.TestCase):
    """Test loading TMX tileset entries."""

    @patch('engine.tmx_loader.tmx_tileset.DiskLoader')
    def test_loads_image_relative_to_resource_dir(self, MockDiskLoader):
        """Tileset image sources are loaded relative to the resource dir."""
        # Tile map is located at rooms/map.tmx, image is at ../tiles/tiles.png
        mock_xml = '<tileset firstgid="1" name="a" tilecount="32" columns="8">'
        mock_xml += '\n\t<image source="../tiles/tiles.png" />'
        mock_xml += '\n</tileset>'
        tileset_node = ElementTree.parse(StringIO(mock_xml)).getroot()

        # Load the tileset
        list(load_tmx_tileset('rooms/map.tmx', tileset_node))

        # Image was loaded from tiles/tiles.png
        MockDiskLoader.load_image_grid.assert_called_once_with(
            'tiles/tiles.png', 4, 8)

    @patch('engine.tmx_loader.tmx_tileset.DiskLoader')
    def test_indexes_image_grid_correctly(self, MockDiskLoader):
        """Tilesets index into the image grid correctly."""
        mock_xml = '<tileset firstgid="1" name="a" tilecount="6" columns="2">'
        mock_xml += '\n\t<image source="../tiles/tiles.png" />'
        mock_xml += '\n</tileset>'
        tileset_node = ElementTree.parse(StringIO(mock_xml)).getroot()

        MockDiskLoader.load_image_grid.return_value = [
            0, 1,
            2, 3,
            4, 5]

        # Right-down order: gid 1 is the bottom left corner of the image grid
        expected = [
            (1, 4), (2, 5),
            (3, 2), (4, 3),
            (5, 0), (6, 1)]

        # Load the tileset
        actual = list(load_tmx_tileset('map.tmx', tileset_node))

        self.assertEqual(expected, actual)

    @patch('engine.tmx_loader.tmx_tileset.DiskLoader')
    def test_map_starts_at_first_gid(self, MockDiskLoader):
        """Tileset indices begin at the first gid of the tileset element."""
        mock_xml = '<tileset firstgid="10" name="a" tilecount="6" columns="2">'
        mock_xml += '\n\t<image source="../tiles/tiles.png" />'
        mock_xml += '\n</tileset>'
        tileset_node = ElementTree.parse(StringIO(mock_xml)).getroot()

        MockDiskLoader.load_image_grid.return_value = [
            0, 1,
            2, 3,
            4, 5]

        # First gid is 10, so map indices begin at 10
        expected = [
            (10, 4), (11, 5),
            (12, 2), (13, 3),
            (14, 0), (15, 1)]

        # Load the tileset
        actual = list(load_tmx_tileset('map.tmx', tileset_node))

        self.assertEqual(expected, actual)
