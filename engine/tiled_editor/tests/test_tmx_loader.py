from ..tmx_loader import TmxLoader
from defusedxml import ElementTree
from io import StringIO
from unittest.mock import Mock, patch
import unittest


class TestTmxLoader(unittest.TestCase):
    """Test loading TMX files."""

    @patch('engine.disk.DiskLoader')
    def test_older_versions_raise_exception(self, MockDiskLoader):
        """Older TMX formats raise an exception."""
        # Version 1.1 is too old
        mock_xml = '<map version="1.1" orientation="orthogonal" infinite="0"/>'
        mock_root_node = ElementTree.parse(StringIO(mock_xml)).getroot()
        MockDiskLoader.load_xml.return_value = mock_root_node

        with self.assertRaises(AttributeError):
            TmxLoader('map.tmx', None)

    @patch('engine.disk.DiskLoader')
    def test_non_orthogonal_maps_raise_exception(self, MockDiskLoader):
        """Orthogonal maps raise an exception."""
        # Map is not orthogonal
        mock_xml = '<map version="1.2" orientation="isometric" infinite="0"/>'
        mock_root_node = ElementTree.parse(StringIO(mock_xml)).getroot()
        MockDiskLoader.load_xml.return_value = mock_root_node

        with self.assertRaises(NotImplementedError):
            TmxLoader('map.tmx', None)

    @patch('engine.disk.DiskLoader')
    def test_infinite_maps_raise_exception(self, MockDiskLoader):
        """Infinite maps raise an exception."""
        # Map is infinite
        mock_xml = '<map version="1.2" orientation="orthogonal" infinite="1"/>'
        mock_root_node = ElementTree.parse(StringIO(mock_xml)).getroot()
        MockDiskLoader.load_xml.return_value = mock_root_node

        with self.assertRaises(NotImplementedError):
            TmxLoader('map.tmx', None)

    @patch('engine.tiled_editor.tmx_loader.load_tmx_tileset')
    @patch('engine.tiled_editor.tmx_loader.TmxLayerLoader')
    @patch('engine.disk.DiskLoader')
    def test_tile_layers_use_tilesets(self, MockDiskLoader, MockLayerLoader,
                                      mock_load_tileset):
        """Tile layers are loaded using the loaded tilesets."""
        mock_xml = '<map version="1.2" orientation="orthogonal" infinite="0" '
        mock_xml += 'tilewidth="10" tileheight="10" width="1" height="2">\n'
        mock_xml += '\t<tileset/>\n'
        mock_xml += '\t<layer/>\n'
        mock_xml += '</map>\n'
        mock_root_node = ElementTree.parse(StringIO(mock_xml)).getroot()
        mock_layer_node = mock_root_node.find('layer')

        MockDiskLoader.load_xml.return_value = mock_root_node

        # Return mock tileset indices and graphics
        mock_image_0, mock_image_1 = Mock(), Mock()
        mock_load_tileset.return_value = [(0, mock_image_0), (1, mock_image_1)]

        # Layer loader creates a layer named 'test'
        MockLayerLoader.return_value.name = 'test'
        MockLayerLoader.return_value.layer = Mock()

        # Create a TMX loader with no object factory
        tmx_loader = TmxLoader('map.tmx', None)

        # Tileset node was loaded
        mock_load_tileset.assert_called_once_with(
            'map.tmx', mock_root_node.find('tileset'))

        # Tile layer node was loaded
        MockLayerLoader.assert_called_once_with(
            mock_layer_node,
            mock_root_node,
            {0: mock_image_0, 1: mock_image_1},
            None)

        # Loaded layer was added to the collection
        self.assertEqual(
            MockLayerLoader().layer, tmx_loader.layers.get_layer('test'))

    @patch('engine.tiled_editor.tmx_loader.TmxLayerLoader')
    @patch('engine.disk.DiskLoader')
    def test_object_layers_are_loaded(self, MockDiskLoader, MockLayerLoader):
        """Tile layers are loaded using the loaded tilesets."""
        mock_xml = '<map version="1.2" orientation="orthogonal" infinite="0" '
        mock_xml += 'tilewidth="10" tileheight="10" width="1" height="2">\n'
        mock_xml += '\t<objectgroup/>\n'
        mock_xml += '</map>\n'
        mock_root_node = ElementTree.parse(StringIO(mock_xml)).getroot()
        mock_layer_node = mock_root_node.find('objectgroup')

        MockDiskLoader.load_xml.return_value = mock_root_node

        mock_factory = Mock()

        # Layer loader creates a layer named 'test'
        MockLayerLoader.return_value.name = 'test'
        MockLayerLoader.return_value.layer = Mock()

        # Create a TMX loader with no object factory
        tmx_loader = TmxLoader('map.tmx', mock_factory)

        # Object layer node was loaded
        MockLayerLoader.assert_called_once_with(
            mock_layer_node, mock_root_node, {}, mock_factory)

        # Loaded layer was added to the collection
        self.assertEqual(
            MockLayerLoader().layer, tmx_loader.layers.get_layer('test'))

    @patch('engine.tiled_editor.tmx_loader.load_tmx_tileset')
    @patch('engine.tiled_editor.tmx_loader.TmxLayerLoader')
    @patch('engine.disk.DiskLoader')
    def test_layer_collection_has_map_dimensions(self, MockDiskLoader,
                                                 MockLayerLoader,
                                                 mock_load_tileset):
        """Tile layer collection has the pixel dimensions of the map."""
        mock_xml = '<map version="1.2" orientation="orthogonal" infinite="0" '
        mock_xml += 'tilewidth="10" tileheight="10" width="1" height="2">\n'
        mock_xml += '\t<tileset/>\n'
        mock_xml += '\t<layer/>\n'
        mock_xml += '</map>\n'
        mock_root_node = ElementTree.parse(StringIO(mock_xml)).getroot()

        MockDiskLoader.load_xml.return_value = mock_root_node

        # Create a TMX loader with no object factory
        tmx_loader = TmxLoader('map.tmx', None)

        # Layer collection has pixel dimensions of the map
        self.assertEqual(10, tmx_loader.layers.width)
        self.assertEqual(20, tmx_loader.layers.height)
