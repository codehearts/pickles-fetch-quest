from ..room_layer import RoomLayer
from unittest.mock import call, Mock
import unittest


class TestRoomLayer(unittest.TestCase):
    """Test object layers within a room."""

    def test_batch_is_optional(self):
        """Layers can be created without a graphics batch."""
        layer = RoomLayer()

        self.assertEqual(None, layer.batch)

    def test_correct_batch_is_used(self):
        """The batch passed to a layer is the batch returned from it."""
        mock_batch = Mock()
        layer = RoomLayer(batch=mock_batch)

        self.assertEqual(mock_batch, layer.batch)

    def test_draws_using_batch_when_available(self):
        """The layer batch is used to draw when available."""
        mock_batch = Mock()
        mock_object_1 = Mock()
        mock_object_2 = Mock()
        mock_object_3 = Mock()

        # Create a layer with a batch and all 3 objects
        layer = RoomLayer(batch=mock_batch)
        layer.add_object(mock_object_1)
        layer.add_object(mock_object_2)
        layer.add_object(mock_object_3)

        layer.draw()

        mock_batch.draw.assert_called_once()
        mock_object_1.draw.assert_not_called()
        mock_object_2.draw.assert_not_called()
        mock_object_3.draw.assert_not_called()

    def test_draws_each_object_when_batch_is_unavailable(self):
        """Each object is drawn in order when a batch is not available."""
        mock_objects = Mock(a=Mock(), b=Mock(), c=Mock())

        # Create a layer without a batch and all 3 objects
        layer = RoomLayer()
        layer.add_object(mock_objects.a)
        layer.add_object(mock_objects.b)
        layer.add_object(mock_objects.c)

        layer.draw()

        mock_objects.assert_has_calls(
            [call.a.draw(), call.b.draw(), call.c.draw()])

    def test_updates_each_object_in_order(self):
        """Each object is updated in order when the layer is updated."""
        mock_objects = Mock(a=Mock(), b=Mock(), c=Mock())

        # Create a layer with 3 objects
        layer = RoomLayer()
        layer.add_object(mock_objects.a)
        layer.add_object(mock_objects.b)
        layer.add_object(mock_objects.c)

        layer.update(123)

        mock_objects.assert_has_calls(
            [call.a.update(123), call.b.update(123), call.c.update(123)])

    def test_layer_is_empty_without_objects(self):
        """Layers are empty when they have no objects."""
        # Create a layer with no objects
        layer = RoomLayer()

        self.assertTrue(layer.is_empty())

    def test_layer_is_not_empty_with_objects(self):
        """Layers are not empty when they have objects."""
        # Create a layer with an object
        layer = RoomLayer()
        layer.add_object(Mock())

        self.assertFalse(layer.is_empty())
