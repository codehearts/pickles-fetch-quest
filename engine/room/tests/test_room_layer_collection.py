from ..room_layer_collection import RoomLayerCollection
from unittest.mock import call, Mock
import unittest


class TestRoomLayerCollection(unittest.TestCase):
    """Test collections of object layers."""

    def test_layers_can_be_fetched_by_name(self):
        """Layers can be fetched by their name."""
        mock_layers = Mock(a=Mock(), b=Mock(), c=Mock())

        # Create a collection with 3 layers (a, b, and c)
        collection = RoomLayerCollection(1, 1)
        collection.add_layer('a', mock_layers.a)
        collection.add_layer('b', mock_layers.b)
        collection.add_layer('c', mock_layers.c)

        self.assertEqual(mock_layers.a, collection.get_layer('a'))
        self.assertEqual(mock_layers.b, collection.get_layer('b'))
        self.assertEqual(mock_layers.c, collection.get_layer('c'))

    def test_layers_are_updated_in_order(self):
        """Layers are updated in insertion order."""
        mock_layers = Mock(a=Mock(), b=Mock(), c=Mock())

        # Create a collection with 3 layers
        collection = RoomLayerCollection(1, 1)
        collection.add_layer('a', mock_layers.a)
        collection.add_layer('b', mock_layers.b)
        collection.add_layer('c', mock_layers.c)

        collection.update(123)

        mock_layers.assert_has_calls(
            [call.a.update(123), call.b.update(123), call.c.update(123)])

    def test_layers_are_drawn_in_order(self):
        """Layers are drawn in insertion order."""
        mock_layers = Mock(a=Mock(), b=Mock(), c=Mock())

        # Create a collection with 3 layers
        collection = RoomLayerCollection(1, 1)
        collection.add_layer('a', mock_layers.a)
        collection.add_layer('b', mock_layers.b)
        collection.add_layer('c', mock_layers.c)

        collection.draw()

        mock_layers.assert_has_calls(
            [call.a.draw(), call.b.draw(), call.c.draw()])

    def test_collection_width_is_read_only(self):
        """Layer collection width is read-only."""
        collection = RoomLayerCollection(1, 0)

        self.assertEqual(1, collection.width)

        with self.assertRaises(AttributeError, msg='can\'t set attribute'):
            collection.width = 2

    def test_collection_height_is_read_only(self):
        """Layer collection height is read-only."""
        collection = RoomLayerCollection(0, 1)

        self.assertEqual(1, collection.height)

        with self.assertRaises(AttributeError, msg='can\'t set attribute'):
            collection.height = 2
