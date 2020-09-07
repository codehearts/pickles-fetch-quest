from ..graphics_object import GraphicsObject
from engine.geometry import Point2d
from unittest.mock import Mock, patch
import unittest


class TestGraphicsObject(unittest.TestCase):
    """Test display states of on-screen graphics."""

    @patch('pyglet.sprite.Sprite')
    def test_create_graphics_object(self, MockSprite):
        """Creates a pyglet.sprite.Sprite object using the graphic."""
        graphic = Mock()
        mock_coordinates = Point2d(x=400, y=300)
        kwargs = {
            'batch': Mock(),
            'group': Mock()
        }

        GraphicsObject(graphic, mock_coordinates, **kwargs)
        MockSprite.assert_called_once_with(
            graphic, 400, 300, **kwargs)

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
    def test_update(self, MockSprite):
        """Coordinates and scaling are set on pyglet.sprite.Sprite object."""
        graphic = GraphicsObject(None, (400, 300))

        graphic.update(0)
        MockSprite.return_value.update.assert_called_once_with(
            x=400, y=300, scale_x=1, scale_y=1)

    @patch('pyglet.sprite.Sprite')
    def test_update_sets_coordinates(self, MockSprite):
        """Coordinates are updated to new values."""
        graphic = GraphicsObject(None, Point2d(12, 34))

        # Update the coordinates (as if by `set_position`)
        graphic.coordinates.x = 56
        graphic.coordinates.y = 78

        graphic.update(0)
        MockSprite.return_value.update.assert_called_once_with(
            x=56, y=78, scale_x=1, scale_y=1)

    @patch('pyglet.sprite.Sprite')
    def test_update_sets_positive_scaling(self, MockSprite):
        """Positive scaling is updated to new values."""
        graphic = GraphicsObject(None)

        graphic.scale_x(2)
        graphic.scale_y(3)

        graphic.update(0)
        MockSprite.return_value.update.assert_called_once_with(
            x=0, y=0, scale_x=2, scale_y=3)

    @patch('pyglet.sprite.Sprite')
    def test_update_sets_negative_scaling_with_offset(self, MockSprite):
        """Negative scaling is updated to new values with offsets."""
        graphic = GraphicsObject(None)

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
        graphic = GraphicsObject(None, Point2d(0, 0))
        graphic.set_position((400, 300))

        self.assertEqual((400, 300), graphic.coordinates)

    @patch('pyglet.sprite.Sprite')
    def test_reading_batch(self, MockSprite):
        """Batch is read from internal Sprite object."""
        graphic = GraphicsObject(None)

        self.assertEqual(MockSprite().batch, graphic.batch)

    @patch('pyglet.sprite.Sprite')
    def test_setting_batch(self, MockSprite):
        """Batch is set on internal Sprite object."""
        mock_batch = Mock()
        graphic = GraphicsObject(None)
        graphic.batch = mock_batch

        self.assertEqual(mock_batch, graphic.batch)
