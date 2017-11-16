from ..event_dispatcher import EventDispatcher, EventException
from unittest.mock import Mock
import unittest


class TestEventDispatcher(unittest.TestCase):
    """Test attaching event listeners and dispatching events.

    All tests will already have an `on_test_event` and an `on_test_event_2`
    event registered with the event dispatcher.
    """

    @classmethod
    def setUpClass(cls):
        """Registers `on_test_event` event for all tests."""
        test_dispatcher = EventDispatcher()
        test_dispatcher.register_event('on_test_event')
        test_dispatcher.register_event('on_test_event_2')

    def test_add_listener_without_registering(self):
        """Exception raised when adding listener without registering events."""
        test_dispatcher = EventDispatcher()
        test_mock = Mock()

        with self.assertRaises(EventException):
            test_dispatcher.add_listeners(on_unregistered_event=test_mock)

    def test_add_listener_via_arg(self):
        """Event listeners can be attached using arguments."""
        test_dispatcher = EventDispatcher()
        on_test_event = Mock()

        test_dispatcher.add_listeners(on_test_event)
        test_dispatcher.dispatch_event('on_test_event')
        on_test_event.assert_called_once

    def test_add_multiple_listeners_via_arg(self):
        """Multiple event listeners can be attached using arguments."""
        test_dispatcher = EventDispatcher()
        on_test_event = Mock()
        on_test_event_2 = Mock()

        test_dispatcher.add_listeners(on_test_event, on_test_event_2)
        test_dispatcher.dispatch_event('on_test_event')
        on_test_event.assert_called_once
        test_dispatcher.dispatch_event('on_test_event_2')
        on_test_event_2.assert_called_once

    def test_add_listener_via_kwarg(self):
        """Event listeners can be attached using keyword arguments."""
        test_dispatcher = EventDispatcher()
        test_mock = Mock()

        test_dispatcher.add_listeners(on_test_event=test_mock)
        test_dispatcher.dispatch_event('on_test_event')
        test_mock.assert_called_once

    def test_add_multiple_listeners_via_kwarg(self):
        """Multiple event listeners can be attached using keyword arguments."""
        test_dispatcher = EventDispatcher()
        test_mock = Mock()
        test_mock_2 = Mock()

        test_dispatcher.add_listeners(
                on_test_event=test_mock, on_test_event_2=test_mock_2)
        test_dispatcher.dispatch_event('on_test_event')
        test_mock.assert_called_once
        test_dispatcher.dispatch_event('on_test_event_2')
        test_mock_2.assert_called_once
