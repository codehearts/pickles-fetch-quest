from ..tmx_layer_loader import TmxLayerLoader
from defusedxml import ElementTree
from io import StringIO
from unittest.mock import call, Mock, patch
import unittest


class TestTmxLayer(unittest.TestCase):
    """Test loading TMX layers."""

    @patch('engine.tiled_editor.tmx_layer_loader.load_tmx_tile_layer')
    @patch('engine.tiled_editor.tmx_layer_loader.GraphicsObject')
    @patch('engine.tiled_editor.tmx_layer_loader.RoomLayer')
    def test_graphics_are_created_for_tile_layers(self, MockLayer,
                                                  MockGraphics,
                                                  mock_load_tile_layer):
        """Graphics are created when loading tile layers."""
        # 2x2 tiles on a 6x3 map
        mock_xml = '<map width="6" height="3" tilewidth="2">\n'
        mock_xml += '\t<layer name="test" width="6" height="3" />\n'
        mock_xml += '</map>\n'
        mock_map_node = ElementTree.parse(StringIO(mock_xml)).getroot()
        mock_layer_node = mock_map_node.find('layer')

        # Mock tileset only has indices 0 and 1
        mock_tileset = {0: Mock(), 1: Mock()}

        # Mock returns a list of (tile_x, tile_y, tileset_index) tuples
        mock_load_tile_layer.return_value = [(1, 2, 0), (3, 4, 1), (5, 6, 2)]

        # Load the TMX layer
        loader = TmxLayerLoader(
            mock_layer_node, mock_map_node, mock_tileset, {}, None)

        # Tile layer was loaded
        mock_load_tile_layer.assert_called_once_with(mock_layer_node)

        # Graphics were created for each tile within the tileset
        # Positions are in pixels rather than tiles
        MockGraphics.assert_has_calls([
            call(mock_tileset[0], (2, 4), batch=MockLayer().batch),
            call(mock_tileset[1], (6, 8), batch=MockLayer().batch)])

        # Layer had both graphics added to it
        MockLayer().add_object.assert_has_calls([
            call(MockGraphics.return_value),
            call(MockGraphics.return_value)])

        self.assertEqual('test', loader.name)
        self.assertEqual(MockLayer(), loader.layer)

    @patch('engine.tiled_editor.tmx_layer_loader.load_tmx_object_layer')
    @patch('engine.tiled_editor.tmx_layer_loader.GraphicsObject')
    @patch('engine.tiled_editor.tmx_layer_loader.RoomLayer')
    def test_objects_are_created_for_obj_layers(self, MockLayer, MockGraphics,
                                                mock_load_object_layer):
        """Objects are created when loading object layers."""
        # 2x2 tiles on a 6x3 map
        mock_xml = '<map width="6" height="3" tilewidth="2">\n'
        mock_xml += '\t<objectgroup name="test" width="6" height="3" />\n'
        mock_xml += '</map>\n'
        mock_map_node = ElementTree.parse(StringIO(mock_xml)).getroot()
        mock_layer_node = mock_map_node.find('objectgroup')

        # Mock factory can't create object with name 'c'
        mock_factory = Mock()
        mock_factory.can_create.side_effect = lambda name: name != 'c'

        mock_load_object_layer.return_value = [
            {'type': 'a', 'x': 0, 'y': 1, 'width': 2, 'height': 3},
            {'type': 'b', 'x': 4, 'y': 5, 'width': 6, 'height': 7},
            {'type': 'c', 'x': 8, 'y': 9, 'width': 10, 'height': 11}]

        # Load the TMX layer
        loader = TmxLayerLoader(
            mock_layer_node, mock_map_node, None, {}, mock_factory)

        # Object layer was loaded with correct dimensions
        mock_load_object_layer.assert_called_once_with(
            10, 4, mock_layer_node, {})

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

    @patch('engine.tiled_editor.tmx_layer_loader.load_tmx_object_layer')
    @patch('engine.tiled_editor.tmx_layer_loader.GraphicsObject')
    @patch('engine.tiled_editor.tmx_layer_loader.RoomLayer')
    def test_object_layer_tiles_have_graphics_created(self, MockLayer,
                                                      MockGraphics,
                                                      mock_load_object_layer):
        """Graphics are created when loading tile objects on object layers."""
        # 2x2 tiles on a 6x3 map
        mock_xml = '<map width="6" height="3" tilewidth="2">\n'
        mock_xml += '\t<objectgroup name="test" width="6" height="3" />\n'
        mock_xml += '</map>\n'
        mock_map_node = ElementTree.parse(StringIO(mock_xml)).getroot()
        mock_layer_node = mock_map_node.find('objectgroup')

        # Mock factory can't create object with name 'c'
        mock_factory = Mock()
        mock_factory.can_create.side_effect = lambda name: name != 'b'

        mock_load_object_layer.return_value = [
            {'type': 'a', 'x': 0, 'y': 1, 'width': 2, 'height': 3, 'tile': 1},
            {'type': 'b', 'x': 4, 'y': 5, 'width': 6, 'height': 7, 'tile': 2}]

        # Mock tileset only has indices 1 and 2
        mock_tileset = {1: Mock(), 2: Mock()}
        tile_objects = {1: 'a', 2: 'b'}

        # Load the TMX layer
        loader = TmxLayerLoader(
            mock_layer_node, mock_map_node, mock_tileset, tile_objects,
            mock_factory)

        # Object layer was loaded with correct dimensions
        mock_load_object_layer.assert_called_once_with(
            10, 4, mock_layer_node, tile_objects)

        # Factory was queried for recipes for all objects
        mock_factory.can_create.assert_has_calls([call('a'), call('b')])

        # Objects were created for 'a', but not 'b' because it can't be created
        mock_factory.create.assert_called_once_with(
            **mock_load_object_layer()[0], batch=MockLayer().batch)

        # Graphics were created for 'a', but not 'b' because it wasn't created
        # Positions are in pixels rather than tiles
        MockGraphics.assert_called_once_with(
            mock_tileset[1], (0, 1), batch=MockLayer().batch)

        # Layer had all objects and graphics added to it
        MockLayer().add_object.assert_has_calls([
            call(mock_factory.create.return_value),
            call(MockGraphics())])

        self.assertEqual('test', loader.name)
        self.assertEqual(MockLayer(), loader.layer)
