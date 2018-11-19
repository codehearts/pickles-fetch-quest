from ..graphics_controller import GraphicsController
from unittest.mock import call, Mock, patch
import unittest

UPDATE_RATE_DEFAULT = 120
RESIZABLE_DEFAULT = False
CAPTION_DEFAULT = None


class TestGraphicsController(unittest.TestCase):
    """Test creation and functionality of the GraphicsController class."""

    def setUp(self):
        """Provides each test with the following patches::

            self.MockPygletWindow:
                Patch of pyglet.window.Window
            self.mock_schedule_interval:
                Patch of pyglet.clock.schedule_interval
        """
        WindowPatch = patch('pyglet.window.Window')
        schedule_interval_patch = patch('pyglet.clock.schedule_interval')

        self.MockPygletWindow = WindowPatch.start()
        self.mock_schedule_interval = schedule_interval_patch.start()

        self.addCleanup(WindowPatch.stop)
        self.addCleanup(schedule_interval_patch.stop)

    def test_create_window_no_kwargs(self):
        """Default window caption and resizable arguments."""
        controller = GraphicsController(400, 300)
        self.MockPygletWindow.assert_called_once_with(
                width=400,
                height=300,
                caption=CAPTION_DEFAULT,
                resizable=RESIZABLE_DEFAULT)
        self.mock_schedule_interval.assert_called_once_with(
                controller._dispatch_update, 1.0/UPDATE_RATE_DEFAULT)

    def test_create_window_title_kwarg(self):
        """Window caption is set to the title kwarg."""
        controller = GraphicsController(400, 300, title='Test')
        self.MockPygletWindow.assert_called_once_with(
                width=400,
                height=300,
                caption='Test',
                resizable=RESIZABLE_DEFAULT)
        self.mock_schedule_interval.assert_called_once_with(
                controller._dispatch_update, 1.0/UPDATE_RATE_DEFAULT)

    def test_create_window_resizable_kwarg(self):
        """Resizable kwarg is given to the pyglet.window.Window constructor."""
        non_default = (not RESIZABLE_DEFAULT)
        controller = GraphicsController(400, 300, resizable=non_default)
        self.MockPygletWindow.assert_called_once_with(
                width=400,
                height=300,
                caption=CAPTION_DEFAULT,
                resizable=non_default)
        self.mock_schedule_interval.assert_called_once_with(
                controller._dispatch_update, 1.0/UPDATE_RATE_DEFAULT)

    def test_create_window_update_rate_kwarg(self):
        """Update rate kwarg is passed to pyglet.clock.schedule_interval."""
        controller = GraphicsController(400, 300, update_rate=60)
        self.MockPygletWindow.assert_called_once_with(
                width=400,
                height=300,
                caption=CAPTION_DEFAULT,
                resizable=RESIZABLE_DEFAULT)
        self.mock_schedule_interval.assert_called_once_with(
                controller._dispatch_update, 1.0/60)

    def test_on_update_event(self):
        """Update rate kwarg is passed to pyglet.clock.schedule_interval."""
        controller = GraphicsController(400, 300)
        on_update_mock = Mock()

        controller.add_listeners(on_update=on_update_mock)
        controller._dispatch_update(0.12345)
        on_update_mock.assert_called_once_with(123)

    def test_key_handlers_are_added_to_window(self):
        """Key handlers are pushed to the controller's window."""
        controller = GraphicsController(400, 300)
        window_mock = self.MockPygletWindow.return_value
        handler_mock = Mock()
        press_mock = Mock()
        release_mock = Mock()

        controller.add_key_handler(
            handler_mock, on_press=press_mock, on_release=release_mock)
        window_mock.push_handlers.assert_has_calls([
            call(handler_mock),
            call(on_key_press=press_mock, on_key_release=release_mock)])
