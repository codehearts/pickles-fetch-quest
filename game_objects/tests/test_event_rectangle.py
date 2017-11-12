from ..event_rectangle import EventRectangle
from unittest.mock import Mock
import unittest


class TestEventRectangle(unittest.TestCase):
    """Test properties and event handling of an EventRectangle object.

    Each test case is provided the following properties::

        self.event_handler: The Mock for the rectangle's event handler.
        self.rect: An EventRectangle created with the following:
            x: 1
            y: 2
            width: 3
            height: 4
            event_handler: self.event_handler
    """

    def setUp(self):
        self.event_handler = Mock()
        self.rect = EventRectangle(1, 2, 3, 4, self.event_handler)

    def test_create_event_rectangle(self):
        """Creates an EventRectangle object and verifies the event handling."""
        self.assertEqual(1, self.rect.x)
        self.assertEqual(2, self.rect.y)
        self.assertEqual(3, self.rect.width)
        self.assertEqual(4, self.rect.height)
        self.event_handler.assert_any_call(
                EventRectangle.SIZE_CHANGED_EVENT, self.rect)
        self.event_handler.assert_any_call(
                EventRectangle.POSITION_CHANGED_EVENT, self.rect)

    def test_set_x(self):
        """Setting x coordinate triggers a position_changed event."""
        self.event_handler.reset_mock()  # Reset call history after __init__

        self.rect.x = 100
        self.assertEqual(100, self.rect.x)
        self.assertEqual(2, self.rect.y)
        self.assertEqual(3, self.rect.width)
        self.assertEqual(4, self.rect.height)
        self.event_handler.assert_called_once_with(
                EventRectangle.POSITION_CHANGED_EVENT, self.rect)

    def test_set_x_no_change(self):
        """No position_changed event is fired when x value does not change."""
        self.event_handler.reset_mock()  # Reset call history after __init__

        self.rect.x = 1
        self.assertEqual(1, self.rect.x)
        self.assertEqual(2, self.rect.y)
        self.assertEqual(3, self.rect.width)
        self.assertEqual(4, self.rect.height)
        self.event_handler.assert_not_called()

    def test_set_y(self):
        """Setting y coordinate triggers a position_changed event."""
        self.event_handler.reset_mock()  # Reset call history after __init__

        self.rect.y = 100
        self.assertEqual(1, self.rect.x)
        self.assertEqual(100, self.rect.y)
        self.assertEqual(3, self.rect.width)
        self.assertEqual(4, self.rect.height)
        self.event_handler.assert_called_once_with(
                EventRectangle.POSITION_CHANGED_EVENT, self.rect)

    def test_set_y_no_change(self):
        """No position_changed event is fired when y value does not change."""
        self.event_handler.reset_mock()  # Reset call history after __init__

        self.rect.y = 2
        self.assertEqual(1, self.rect.x)
        self.assertEqual(2, self.rect.y)
        self.assertEqual(3, self.rect.width)
        self.assertEqual(4, self.rect.height)
        self.event_handler.assert_not_called()

    def test_set_width(self):
        """Setting width triggers a size_changed event."""
        self.event_handler.reset_mock()  # Reset call history after __init__

        self.rect.width = 100
        self.assertEqual(1, self.rect.x)
        self.assertEqual(2, self.rect.y)
        self.assertEqual(100, self.rect.width)
        self.assertEqual(4, self.rect.height)
        self.event_handler.assert_called_once_with(
                EventRectangle.SIZE_CHANGED_EVENT, self.rect)

    def test_set_width_no_change(self):
        """No position_changed event is fired when width does not change."""
        self.event_handler.reset_mock()  # Reset call history after __init__

        self.rect.width = 3
        self.assertEqual(1, self.rect.x)
        self.assertEqual(2, self.rect.y)
        self.assertEqual(3, self.rect.width)
        self.assertEqual(4, self.rect.height)
        self.event_handler.assert_not_called()

    def test_set_height(self):
        """Setting height triggers a size_changed event."""
        self.event_handler.reset_mock()  # Reset call history after __init__

        self.rect.height = 100
        self.assertEqual(1, self.rect.x)
        self.assertEqual(2, self.rect.y)
        self.assertEqual(3, self.rect.width)
        self.assertEqual(100, self.rect.height)
        self.event_handler.assert_called_once_with(
                EventRectangle.SIZE_CHANGED_EVENT, self.rect)

    def test_set_height_no_change(self):
        """No position_changed event is fired when height does not change."""
        self.event_handler.reset_mock()  # Reset call history after __init__

        self.rect.height = 4
        self.assertEqual(1, self.rect.x)
        self.assertEqual(2, self.rect.y)
        self.assertEqual(3, self.rect.width)
        self.assertEqual(4, self.rect.height)
        self.event_handler.assert_not_called()
