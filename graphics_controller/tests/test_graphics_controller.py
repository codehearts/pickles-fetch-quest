from ..graphics_controller import GraphicsController
from unittest.mock import patch
import unittest

RESIZABLE_DEFAULT = False
CAPTION_DEFAULT = None


class TestGraphicsController(unittest.TestCase):
    """Test creation and functionality of the GraphicsController class."""

    @patch('pyglet.window.Window')
    def test_create_window_no_kwargs(self, MockPygletWindow):
        """Default window caption and resizable arguments."""
        GraphicsController(400, 300)
        MockPygletWindow.assert_called_with(
                width=400,
                height=300,
                caption=CAPTION_DEFAULT,
                resizable=RESIZABLE_DEFAULT)

    @patch('pyglet.window.Window')
    def test_create_window_title_kwarg(self, MockPygletWindow):
        """Window caption is set to the title kwarg."""
        GraphicsController(400, 300, title='Test')
        MockPygletWindow.assert_called_with(
                width=400,
                height=300,
                caption='Test',
                resizable=RESIZABLE_DEFAULT)

    @patch('pyglet.window.Window')
    def test_create_window_resizable_kwargs(self, MockPygletWindow):
        """Resizable kwarg is given to the pyglet.window.Window constructor."""
        non_default = (not RESIZABLE_DEFAULT)
        GraphicsController(400, 300, resizable=non_default)
        MockPygletWindow.assert_called_with(
                width=400,
                height=300,
                caption=CAPTION_DEFAULT,
                resizable=non_default)
