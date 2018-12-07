from ..tmx_layer_loader import TmxLayerLoader
from defusedxml import ElementTree
from io import StringIO
from unittest.mock import call, Mock, patch
import unittest


class TestTmxLayer(unittest.TestCase):
    """Test loading TMX layers."""

    @patch('engine.tiled_editor.tmx_layer_loader.load_tmx_tile_layer')
    @patch('engine.graphics.GraphicsObject')
    @patch('engine.room.RoomLayer')
    def test_graphics_are_created_for_tile_layers(self, MockLayer,
                                                  MockGraphics,
                                                  mock_load_tile_layer):
        """Graphics are created when loading tile layers."""
        # 2x2 tiles on a 6x3 map
        mock_xml = '<map width="6" height="3" tilewidth="2">\n'
        mock_xml += '\t<layer name="test" />\n'
        mock_xml += '</map>\n'
        mock_map_node = ElementTree.parse(StringIO(mock_xml)).getroot()
        mock_layer_node = mock_map_node.find('layer')

        # Mock tileset only has indices 0 and 1
        mock_tileset = {0: Mock(), 1: Mock()}

        # Mock returns a list of (tile_x, tile_y, tileset_index) tuples
        mock_load_tile_layer.return_value = [(1, 2, 0), (3, 4, 1), (5, 6, 2)]

        # Load the TMX layer
        loader = TmxLayerLoader(
            mock_layer_node, mock_map_node, mock_tileset, None)

        # Tile layer was loaded
        mock_load_tile_layer.assert_called_once_with(mock_layer_node)

        # Graphics were created for each tile within the tileset
        # Positions are in pixels rather than tiles
        MockGraphics.assert_has_calls([
            call((2, 4),
                 {'default': mock_tileset[0]},
                 batch=MockLayer().batch),
            call((6, 8),
                 {'default': mock_tileset[1]},
                 batch=MockLayer().batch)])

        # Layer had both graphics added to it
        MockLayer().add_object.assert_has_calls([
            call(MockGraphics.return_value),
            call(MockGraphics.return_value)])

        self.assertEqual('test', loader.name)
        self.assertEqual(MockLayer(), loader.layer)

    @patch('engine.tiled_editor.tmx_layer_loader.load_tmx_object_layer')
    @patch('engine.graphics.GraphicsObject')
    @patch('engine.room.RoomLayer')
    def test_graphics_are_created_for_obj_layers(self, MockLayer, MockGraphics,
                                                 mock_load_object_layer):
        """Objects are created when loading object layers."""
        # 2x2 tiles on a 6x3 map
        mock_xml = '<map width="6" height="3" tilewidth="2">\n'
        mock_xml += '\t<objectgroup name="test" />\n'
        mock_xml += '</map>\n'
        mock_map_node = ElementTree.parse(StringIO(mock_xml)).getroot()
        mock_layer_node = mock_map_node.find('objectgroup')

        # Mock factory can't create object with name 'c'
        mock_factory = Mock()
        mock_factory.can_create.side_effect = lambda name: name != 'c'

        mock_load_object_layer.return_value = [
            {'name': 'a', 'x': 0, 'y': 1, 'width': 2, 'height': 3},
            {'name': 'b', 'x': 4, 'y': 5, 'width': 6, 'height': 7},
            {'name': 'c', 'x': 8, 'y': 9, 'width': 10, 'height': 11}]

        # Load the TMX layer
        loader = TmxLayerLoader(
            mock_layer_node, mock_map_node, None, mock_factory)

        # Object layer was loaded with correct dimensions
        mock_load_object_layer.assert_called_once_with(
            10, 4, mock_layer_node)

        # Factory was queried for recipes for all objects
        mock_factory.can_create.assert_has_calls([
            call('a'), call('b'), call('c')])

        # Objects were created for 'a' and 'b', but not 'c'
        mock_factory.create.assert_has_calls([
            call(**mock_load_object_layer()[0], batch=MockLayer().batch),
            call(**mock_load_object_layer()[1], batch=MockLayer().batch)])

        # Layer had both objects added to it
        MockLayer().add_object.assert_has_calls([
            call(mock_factory.create.return_value),
            call(mock_factory.create.return_value)])

        self.assertEqual('test', loader.name)
        self.assertEqual(MockLayer(), loader.layer)
