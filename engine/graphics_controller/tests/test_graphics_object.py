from ..graphics_object import GraphicsObject
from unittest.mock import Mock, PropertyMock, patch
import unittest


class TestGraphicsObject(unittest.TestCase):
    """Test display states of on-screen graphics."""

    @patch('pyglet.sprite.Sprite')
    def test_create_graphics_object(self, MockSprite):
        """Creates a pyglet.sprite.Sprite object using default state."""
        states = {
            'default': Mock(),
            'activated': Mock()
        }
        kwargs = {
            'x': 400,
            'y': 300,
            'batch': Mock(),
            'group': Mock()
        }

        GraphicsObject(states, **kwargs)
        MockSprite.assert_called_once_with(states['default'], **kwargs)

    @patch('pyglet.image.Animation')
    @patch('pyglet.image.atlas.TextureBin')
    def test_create_animation(self, mock_texture_bin, mock_animation):
        """Creates an animation object from a list of frames."""
        frames = [Mock(), Mock(), Mock(), Mock()]
        animation = GraphicsObject.create_animation(frames[:2], 1, loop=False)

        self.assertEqual(
            mock_animation.from_image_sequence.return_value,
            animation)

        mock_animation.from_image_sequence.assert_called_once_with(
            frames[:2], 1, loop=False)

    @patch('pyglet.sprite.Sprite')
    def test_create_graphics_object_without_default_state(self, MockSprite):
        """KeyError is raised when default display state is omitted."""
        states = {
            'activated': Mock()
        }
        kwargs = {
            'x': 400,
            'y': 300,
            'batch': Mock(),
            'group': Mock()
        }

        with self.assertRaises(KeyError):
            GraphicsObject(states, **kwargs)

    @patch('pyglet.sprite.Sprite')
    def test_set_coordinates(self, MockSprite):
        """Coordinates are set on underlying pyglet.sprite.Sprite object."""

        # Create a mock for the pyglet.sprite.Sprite.position property
        mock_position = PropertyMock()
        type(MockSprite()).position = mock_position

        graphic = GraphicsObject({'default': None})

        graphic.set_position((400, 300))
        mock_position.assert_called_once_with((400, 300))
