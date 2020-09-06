from ..world_2d_debug import World2dDebug
from ..world_object import WorldObject, COLLIDER, TRIGGER
from unittest.mock import call, Mock, patch, ANY
import unittest


class TestWorld2dDebug(unittest.TestCase):
    """Test functionality of the ``World2dDebug`` class."""

    def setUp(self):
        """Creates the following for each test:

        * ``self.collider``: Object for a collider.
        * ``self.trigger``: Object for a trigger.
        * ``self.world``: World with the collider and trigger, in that order.
        """
        self.collider = Mock()
        self.trigger = Mock()
        self.world = Mock(_objects=[
            WorldObject(self.collider, COLLIDER),
            WorldObject(self.trigger, TRIGGER)])

    @patch('engine.world.world_2d_debug.CrossBox')
    @patch('engine.world.world_2d_debug.GraphicsBatch')
    def test_existing_objects_create_shapes(self, MockBatch, MockBox):
        """Existing objects in the world have debug shapes created for them."""
        World2dDebug(self.world)

        MockBox.assert_has_calls([
            call(self.collider, ANY, ANY),
            call(self.trigger, ANY, ANY)])

    @patch('engine.world.world_2d_debug.CrossBox')
    @patch('engine.world.world_2d_debug.GraphicsBatch')
    def test_existing_objects_use_color_for_type(self, MockBatch, MockBox):
        """Existing objects use the given color for their type."""
        World2dDebug(
            self.world, collider_color=(1, 2, 3), trigger_color=(4, 5, 6))

        MockBox.assert_has_calls([
            call(self.collider, (1, 2, 3), ANY),
            call(self.trigger, (4, 5, 6), ANY)])

    @patch('engine.world.world_2d_debug.CrossBox')
    @patch('engine.world.world_2d_debug.GraphicsBatch')
    def test_existing_objects_are_batched_by_type(self, MockBatch, MockBox):
        """Existing objects are added to the graphics batch for their type."""
        batch_1, batch_2 = Mock(), Mock()
        MockBatch.side_effect = [batch_1, batch_2]

        World2dDebug(self.world)

        collider_batch = MockBox.mock_calls[0].args[2]
        trigger_batch = MockBox.mock_calls[1].args[2]

        self.assertNotEqual(trigger_batch, collider_batch)
        self.assertIn(collider_batch, (batch_1, batch_2))
        self.assertIn(trigger_batch, (batch_1, batch_2))

    @patch('engine.world.world_2d_debug.CrossBox')
    @patch('engine.world.world_2d_debug.GraphicsBatch')
    def test_new_triggers_added_to_trigger_batch(self, MockBatch, MockBox):
        """New triggers are added to the trigger graphics batch."""
        mock_trigger = Mock()
        batch_1, batch_2 = Mock(), Mock()
        MockBatch.side_effect = [batch_1, batch_2]

        World2dDebug(self.world)

        # Get the registered on_trigger_add listener
        trigger_listener = list(filter(
            lambda call: 'on_trigger_add' in call.kwargs,
            self.world.add_listeners.mock_calls
        ))[0].kwargs['on_trigger_add']

        # Call the listener that fires when on_trigger_add occurs
        trigger_listener(mock_trigger)

        trigger_batch = MockBox.mock_calls[1].args[2]

        MockBox.assert_any_call(mock_trigger, ANY, trigger_batch)

    @patch('engine.world.world_2d_debug.CrossBox')
    @patch('engine.world.world_2d_debug.GraphicsBatch')
    def test_new_colliders_added_to_collider_batch(self, MockBatch, MockBox):
        """New colliders are added to the collider graphics batch."""
        mock_collider = Mock()
        batch_1, batch_2 = Mock(), Mock()
        MockBatch.side_effect = [batch_1, batch_2]

        World2dDebug(self.world)

        # Get the registered on_collider_add listener
        collider_listener = list(filter(
            lambda call: 'on_collider_add' in call.kwargs,
            self.world.add_listeners.mock_calls
        ))[0].kwargs['on_collider_add']

        # Call the listener that fires when on_collider_add occurs
        collider_listener(mock_collider)

        collider_batch = MockBox.mock_calls[0].args[2]

        MockBox.assert_any_call(mock_collider, ANY, collider_batch)

    @patch('engine.world.world_2d_debug.CrossBox')
    @patch('engine.world.world_2d_debug.GraphicsBatch')
    def test_updates_objects_after_world_update(self, MockBatch, MockBox):
        """The world debugger updates when the world has finished updating."""
        mock_collider, mock_trigger = Mock(), Mock()

        World2dDebug(self.world)

        trigger_listener = list(filter(
            lambda call: 'on_trigger_add' in call.kwargs,
            self.world.add_listeners.mock_calls
        ))[0].kwargs['on_trigger_add']

        collider_listener = list(filter(
            lambda call: 'on_collider_add' in call.kwargs,
            self.world.add_listeners.mock_calls
        ))[0].kwargs['on_collider_add']

        update_listener = list(filter(
            lambda call: 'on_update_exit' in call.kwargs,
            self.world.add_listeners.mock_calls
        ))[0].kwargs['on_update_exit']

        trigger_listener(mock_trigger)
        collider_listener(mock_collider)

        # Call the listener that fires when on_update_exit occurs
        update_listener(self.world)

        MockBox.return_value.set_position.assert_has_calls([
            call(self.collider.coordinates),
            call(mock_collider.coordinates),
            call(self.trigger.coordinates),
            call(mock_trigger.coordinates),
        ], any_order=True)

    @patch('engine.world.world_2d_debug.CrossBox')
    @patch('engine.world.world_2d_debug.GraphicsBatch')
    def test_collider_batch_is_drawn_normally(self, MockBatch, MockBox):
        """The collider batch is drawn normally during a debug draw."""
        batch_1, batch_2 = Mock(), Mock()
        MockBatch.side_effect = [batch_1, batch_2]

        world_debug = World2dDebug(self.world)
        world_debug.draw()

        collider_batch = MockBox.mock_calls[0].args[2]
        collider_batch.draw.assert_called_once_with()

    @patch('engine.world.world_2d_debug.CrossBox')
    @patch('engine.world.world_2d_debug.GraphicsBatch')
    def test_trigger_batch_is_drawn_with_dashed_line(self, MockBatch, MockBox):
        """The trigger batch is drawn with dashed lines during a debug draw."""
        batch_1, batch_2 = Mock(), Mock()
        MockBatch.side_effect = [batch_1, batch_2]

        world_debug = World2dDebug(self.world)
        world_debug.draw()

        trigger_batch = MockBox.mock_calls[1].args[2]
        trigger_batch.draw_special.assert_called_once_with(
            MockBatch.DASHED_LINES)
