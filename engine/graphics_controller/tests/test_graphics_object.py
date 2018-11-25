from ..graphics_object import GraphicsObject
from unittest.mock import Mock, patch
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
        mock_coordinates = Mock(x=400, y=300)
        kwargs = {
            'batch': Mock(),
            'group': Mock()
        }

        GraphicsObject(mock_coordinates, states, **kwargs)
        MockSprite.assert_called_once_with(
            states['default'], x=400, y=300, **kwargs)

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
        mock_coordinates = Mock(x=400, y=300)
        kwargs = {
            'batch': Mock(),
            'group': Mock()
        }

        with self.assertRaises(KeyError):
            GraphicsObject(mock_coordinates, states, **kwargs)

    @patch('pyglet.sprite.Sprite')
    def test_update(self, MockSprite):
        """Coordinates and scaling are set on pyglet.sprite.Sprite object."""
        graphic = GraphicsObject(Mock(x=400, y=300), {'default': None})

        graphic.update(0)
        MockSprite.return_value.update.assert_called_once_with(
            x=400, y=300, scale_x=1, scale_y=1)

    @patch('pyglet.sprite.Sprite')
    def test_update_sets_coordinates(self, MockSprite):
        """Coordinates are updated to new values."""
        mock_coordinates = Mock(x=12, y=34)
        graphic = GraphicsObject(mock_coordinates, {'default': None})

        # Update the coordinates (as if by `set_position`)
        mock_coordinates.x = 56
        mock_coordinates.y = 78

        graphic.update(0)
        MockSprite.return_value.update.assert_called_once_with(
            x=56, y=78, scale_x=1, scale_y=1)

    @patch('pyglet.sprite.Sprite')
    def test_update_sets_positive_scaling(self, MockSprite):
        """Positive scaling is updated to new values."""
        graphic = GraphicsObject(Mock(x=0, y=0), {'default': None})

        graphic.scale_x(2)
        graphic.scale_y(3)

        graphic.update(0)
        MockSprite.return_value.update.assert_called_once_with(
            x=0, y=0, scale_x=2, scale_y=3)

    @patch('pyglet.sprite.Sprite')
    def test_update_sets_negative_scaling_with_offset(self, MockSprite):
        """Negative scaling is updated to new values with offsets."""
        graphic = GraphicsObject(Mock(x=0, y=0), {'default': None})

        # Set sprite dimensions for negative scaling offset
        MockSprite.return_value.width = 10
        MockSprite.return_value.height = 20

        graphic.scale_x(-1)
        graphic.scale_y(-2)
        graphic.update(0)

        # Sprite position is offset to keep anchor point at bottom left corner
        MockSprite.return_value.update.assert_called_once_with(
            x=10, y=40, scale_x=-1, scale_y=-2)

        # Actual coordinates are not offset, only the sprite coordinates
        self.assertEqual(0, graphic.coordinates.x)
        self.assertEqual(0, graphic.coordinates.y)

    @patch('pyglet.sprite.Sprite')
    def test_set_coordinates(self, MockSprite):
        """Coordinates are stored internally and publicly accessible."""
        mock_coordinates = Mock(x=0, y=0)
        graphic = GraphicsObject(mock_coordinates, {'default': None})

        graphic.set_position((400, 300))
        mock_coordinates.set.assert_called_once_with((400, 300))

        self.assertEqual(mock_coordinates, graphic.coordinates)
