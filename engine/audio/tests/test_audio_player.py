from ..exceptions import DuplicateAudioStreamException
from ..audio_player import AudioPlayer
from unittest.mock import call, Mock, patch
import pyglet.media
import unittest


class TestAudioPlayer(unittest.TestCase):
    """Test playback of audio files."""

    @patch('pyglet.media.Player.queue')
    def setUp(self, mock_queue):
        """Provides each test case with the following properties::

            self.mock_audio: Mock for the audio file from disk.
            self.mock_queue: Mock for pyglet.media.Player.queue.
            self.player: An AudioPlayer created using ``self.mock_audio``.
        """
        self.mock_audio = Mock()
        self.mock_queue = mock_queue
        self.player = AudioPlayer(self.mock_audio)

    def test_create_audio_player(self):
        """Creates a pyglet.media.Player object from the audio file."""
        self.mock_queue.assert_called_once_with(self.mock_audio)

    @patch('pyglet.media.Player.queue')
    def test_create_duplicate_streaming_audio_player(self, local_mock_queue):
        """Multiple players for a streaming source raises an exception."""
        # `queue` raises MediaException when streaming audio was already queued
        local_mock_queue.side_effect = pyglet.media.MediaException

        # Creating a new `AudioPlayer` will raise the exeption
        with self.assertRaises(DuplicateAudioStreamException):
            AudioPlayer(self.mock_audio)
            local_mock_queue.assert_called_once_with(self.mock_audio)

    @patch('pyglet.media.Player.play')
    def test_playing_audio(self, mock_play):
        """Audio plays from where it left off."""
        self.player.play()

        mock_play.assert_called_once()

    def test_playing_audio_dispatches_event(self):
        """Playing audio dispatches the on_play event."""
        mock_listener = Mock()
        self.player.add_listeners(on_play=mock_listener)

        self.player.play()

        mock_listener.assert_called_once_with(self.player)

    @patch('pyglet.media.Player.pause')
    def test_pausing_audio(self, mock_pause):
        """Audio pauses at its current timestamp."""
        self.player.pause()

        mock_pause.assert_called_once()

    def test_pausing_audio_dispatches_event(self):
        """Pausing audio dispatches the on_pause event."""
        mock_listener = Mock()
        self.player.add_listeners(on_pause=mock_listener)

        self.player.pause()

        mock_listener.assert_called_once_with(self.player)

    @patch('pyglet.media.Player.seek')
    @patch('pyglet.media.Player.pause')
    def test_stopping_audio(self, mock_pause, mock_seek):
        """Audio stops and resets to the beginning."""
        self.player.stop()

        mock_pause.assert_called_once()
        mock_seek.assert_called_once_with(0)

    def test_stopping_audio_dispatches_event(self):
        """Stopping audio dispatches the on_pause event."""
        mock_listener = Mock()
        self.player.add_listeners(on_stop=mock_listener)

        self.player.stop()

        mock_listener.assert_called_once_with(self.player)

    @patch('pyglet.media.Player.seek')
    @patch('pyglet.media.Player.play')
    def test_restarting_audio(self, mock_play, mock_seek):
        """Audio plays from the beginning."""
        self.player.restart()

        mock_seek.assert_called_once_with(0)
        mock_play.assert_called_once()

    def test_restarting_audio_dispatches_event(self):
        """Restarting audio dispatches on_stop followed by on_play."""
        mock_listener = Mock()
        mock_listener.on_stop = Mock()
        mock_listener.on_play = Mock()

        self.player.add_listeners(on_stop=mock_listener.on_stop)
        self.player.add_listeners(on_play=mock_listener.on_play)

        self.player.restart()

        mock_listener.assert_has_calls(
            [call.on_stop(self.player), call.on_play(self.player)])

    def test_audio_completion_dispatches_event(self):
        """An on_finish event is dispatched when audio playback completes."""
        mock_listener = Mock()
        self.player.add_listeners(on_finish=mock_listener)

        self.player.dispatch_event('on_player_eos')

        mock_listener.assert_called_once_with(self.player)

    def test_setting_position(self):
        """Setting the position updates the returned position."""
        self.player.position = (1, 2, 3)
        self.assertEqual(
            (1, 2, 3), self.player.position, 'Position was not updated')

    def test_setting_volume(self):
        """Setting the volume updates the returned volume."""
        self.player.volume = 0.5
        self.assertEqual(0.5, self.player.volume, 'Volume was not updated')
