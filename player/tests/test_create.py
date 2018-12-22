from ..create import create_player
from unittest.mock import call, Mock, patch
from pyglet.window import key
import unittest


class TestCreatePlayer(unittest.TestCase):
    """Test player creation function."""

    @patch('engine.graphics.GraphicsObject')
    @patch('engine.disk.DiskLoader')
    def test_loads_animation_from_disk(self, mock_disk, mock_graphics):
        """Animations for the player are loaded from disk."""
        create_player(Mock())

        mock_graphics.create_animation.assert_called_once_with(
            mock_disk.load_image_grid.return_value, 1, loop=True)

    @patch('player.create.PlatformerController')
    @patch('engine.graphics.GraphicsObject')
    @patch('engine.game_object.GameObject')
    @patch('engine.disk.DiskLoader')
    def test_adds_graphics_and_collision_listeners(self, mock_disk,
                                                   mock_game_object,
                                                   mock_graphics,
                                                   mock_controller):
        """Graphic updates and collision processing listeners are added."""
        create_player(Mock())

        mock_game_object.return_value.add_listeners.assert_has_calls([
            call(on_move=mock_graphics.return_value.set_position),
            call(on_collision=mock_controller.return_value.process_collision)])

    @patch('player.create.PlatformerController')
    @patch('engine.graphics.GraphicsObject')
    @patch('engine.game_object.GameObject')
    @patch('engine.disk.DiskLoader')
    def test_registers_keys_for_walking(self, mock_disk, mock_game_object,
                                        mock_graphics, mock_controller):
        """Key handlers for walking are registered."""
        mock_key_handler = Mock()
        create_player(mock_key_handler)

        mock_key_handler.on_key_down.assert_has_calls([
            call(key.LEFT, mock_controller.return_value.walk_left),
            call(key.RIGHT, mock_controller.return_value.walk_right)])

        mock_key_handler.on_key_release.assert_has_calls([
            call(key.LEFT, mock_controller.return_value.stop_walking),
            call(key.RIGHT, mock_controller.return_value.stop_walking)])

    @patch('player.create.PlatformerController')
    @patch('engine.graphics.GraphicsObject')
    @patch('engine.game_object.GameObject')
    @patch('engine.disk.DiskLoader')
    def test_registers_keys_for_jumping(self, mock_disk, mock_game_object,
                                        mock_graphics, mock_controller):
        """Key handlers for jumping are registered."""
        mock_key_handler = Mock()
        create_player(mock_key_handler)

        mock_key_handler.on_key_down.assert_has_calls([
            call(key.UP, mock_controller.return_value.jump)])

        mock_key_handler.on_key_release.assert_has_calls([
            call(key.UP, mock_controller.return_value.cancel_jump)])

    @patch('player.create.PlatformerController')
    @patch('engine.graphics.GraphicsObject')
    @patch('engine.game_object.GameObject')
    @patch('engine.disk.DiskLoader')
    def test_returns_game_object_and_graphics(self, mock_disk,
                                              mock_game_object, mock_graphics,
                                              mock_controller):
        """Both the game object and graphics are returned."""
        self.assertEqual(
            (mock_game_object.return_value, mock_graphics.return_value),
            create_player(Mock()))
