from ..room import Room
from unittest.mock import Mock
import unittest


class TestRoom(unittest.TestCase):
    """Test collections of rendering layers and objects."""

    def test_room_provides_layer_dimensions(self):
        """A room provides access to its layers' dimensions."""
        mock_layer_collection = Mock(width=123, height=456)

        room = Room(mock_layer_collection)

        self.assertEqual(123, room.width)
        self.assertEqual(456, room.height)

    def test_layers_are_updated(self):
        """Layer collections are updated when updating a room."""
        mock_layer_collection = Mock()

        room = Room(mock_layer_collection)
        room.update(123)

        mock_layer_collection.update.assert_called_once_with(123)

    def test_layers_are_drawn(self):
        """Layer collections are drawn when drawing a room."""
        mock_layer_collection = Mock()

        room = Room(mock_layer_collection)
        room.draw()

        mock_layer_collection.draw.assert_called_once()
