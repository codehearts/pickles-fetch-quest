from ..key_handler import KeyHandler
from unittest.mock import call, Mock, patch
import unittest


class TestKeyHandler(unittest.TestCase):
    """Test creation and key mappings of the KeyHandler class."""

    @patch('pyglet.window.key.KeyStateHandler')
    def setUp(self, Handler_mock):
        """Provides each test case with the following properties::

            self.key_down_mock: Mock dict of held-down keys.
            self.graphics_mock: Mock `GraphicsController` object.
            self.handler: Mock `KeyHandler` object.
        """
        self.key_down_mock = {}
        Handler_mock.return_value = self.key_down_mock
        self.graphics_mock = Mock()
        self.handler = KeyHandler(self.graphics_mock)

    @patch('pyglet.window.key.KeyStateHandler')
    def test_handler_adds_itself_to_graphics_controller(self, Handler_mock):
        """Key handlers add themselves to the given graphics controller."""
        mock_graphics = Mock()

        KeyHandler(mock_graphics)

        mock_add_handlers = mock_graphics.add_key_handler
        key_handlers = mock_add_handlers.call_args[1]

        mock_graphics.add_key_handler.assert_called_once_with(
            Handler_mock.return_value,
            on_press=key_handlers['on_press'],
            on_release=key_handlers['on_release'])

    def test_key_down_handlers_called_when_key_down(self):
        """Key down handlers are called on update when the key is held down."""
        callback_1_mock = Mock()
        callback_2_mock = Mock()
        self.handler.on_key_down(1, callback_1_mock)
        self.handler.on_key_down(1, callback_2_mock)

        # Register the key as held down
        self.key_down_mock[1] = True

        self.handler.update(1234)
        callback_1_mock.assert_called_once_with(1234)
        callback_2_mock.assert_called_once_with(1234)

    def test_key_down_handlers_not_called_when_key_not_down(self):
        """Key down handlers aren't called when the key is not held down."""
        callback_1_mock = Mock()
        callback_2_mock = Mock()
        self.handler.on_key_down(1, callback_1_mock)
        self.handler.on_key_down(1, callback_2_mock)

        # Register the key as not held down
        self.key_down_mock[1] = False

        self.handler.update(1234)
        callback_1_mock.assert_not_called()
        callback_2_mock.assert_not_called()

    def test_key_down_handlers_called_as_long_as_key_down(self):
        """Key down handlers are called constantly until key is released."""
        callback_mock = Mock()
        self.handler.on_key_down(1, callback_mock)

        # Register the key as held down
        self.key_down_mock[1] = True

        # Held for 2 updates
        self.handler.update(1234)
        self.handler.update(1234)

        # Register the key as not held down
        self.key_down_mock[1] = False

        # Released on 3rd update
        self.handler.update(1234)

        # Called twice: first update and second update only
        callback_mock.assert_has_calls([call(1234), call(1234)])

    def test_key_press_handlers_called_when_key_pressed_initially(self):
        """Key press handlers are only called when the key is first pressed."""
        # Capture the on_key_press callback from the graphics controller
        mock_add_handlers = self.graphics_mock.add_key_handler
        mock_add_handlers.assert_called_once()
        key_press_handler = mock_add_handlers.call_args[1]['on_press']

        callback_1_mock = Mock()
        callback_2_mock = Mock()
        self.handler.on_key_press(1, callback_1_mock)
        self.handler.on_key_press(1, callback_2_mock)

        key_press_handler(1, None)

        callback_1_mock.assert_called_once()
        callback_2_mock.assert_called_once()

    def test_key_release_handlers_called_when_key_released_initially(self):
        """Key release handlers are only called when the key is released."""
        # Capture the on_key_release callback from the graphics controller
        mock_add_handlers = self.graphics_mock.add_key_handler
        mock_add_handlers.assert_called_once()
        key_release_handler = mock_add_handlers.call_args[1]['on_release']

        callback_1_mock = Mock()
        callback_2_mock = Mock()
        self.handler.on_key_release(1, callback_1_mock)
        self.handler.on_key_release(1, callback_2_mock)

        key_release_handler(1, None)

        callback_1_mock.assert_called_once()
        callback_2_mock.assert_called_once()
