from ..audio_player import AudioPlayer
from unittest.mock import Mock, patch
import unittest
import gc


class TestAudioPlayer(unittest.TestCase):
    """Test playback of audio files."""

    @patch('pyglet.media.Player')
    def setUp(self, mock_player):
        """Provides each test case with the following properties::

            self.mock_source: Mock for the audio source.
            self.mock_queue: Mock for pyglet.media.Player.
            self.player: An AudioPlayer created using ``self.mock_source``.
        """
        self.mock_source = Mock()
        self.mock_player = mock_player.return_value
        self.player = AudioPlayer(self.mock_source)

    def test_create_audio_player(self):
        """Creates a pyglet.media.Player object from the audio source."""
        self.mock_player.queue.assert_called_once_with(self.mock_source)

    def test_create_audio_player_sets_state(self):
        """New players start in the 'stop' state."""
        self.assertEqual(
            AudioPlayer.STOP, self.player.state,
            'State of new audio player is not "stop"')

    @patch('pyglet.media.Player')
    def test_create_audio_player_with_position(self, MockPlayer):
        """Passing a position on construction sets the position."""
        mock_position = Mock()
        self.player = AudioPlayer(self.mock_source, position=mock_position)

        self.assertEqual(
            mock_position, self.player.position,
            'Passing position on construction did not set position')

    def test_playing_audio(self):
        """Audio plays from where it left off."""
        self.player.play()

        self.mock_player.play.assert_called_once()

    def test_playing_audio_sets_state(self):
        """Playing an audio player sets its state to 'play'."""
        self.player.play()

        self.assertEqual(
            AudioPlayer.PLAY, self.player.state,
            'State of playing audio is not "play"')

    def test_playing_audio_dispatches_event(self):
        """Playing audio dispatches the on_play event."""
        mock_listener = Mock()
        self.player.add_listeners(on_play=mock_listener)

        self.player.play()

        mock_listener.assert_called_once_with(self.player)

    def test_pausing_audio(self):
        """Audio pauses at its current timestamp."""
        self.player.pause()

        self.mock_player.pause.assert_called_once()

    def test_pausing_audio_sets_state(self):
        """Pausing an audio player sets its state to 'pause'."""
        self.player.pause()

        self.assertEqual(
            AudioPlayer.PAUSE, self.player.state,
            'State of paused audio is not "pause"')

    def test_pausing_audio_dispatches_event(self):
        """Pausing audio dispatches the on_pause event."""
        mock_listener = Mock()
        self.player.add_listeners(on_pause=mock_listener)

        self.player.pause()

        mock_listener.assert_called_once_with(self.player)

    def test_stopping_audio(self):
        """Audio stops and resets to the beginning."""
        self.player.stop()

        self.mock_player.pause.assert_called_once()
        self.mock_player.seek.assert_called_once_with(0)

    def test_stopping_audio_sets_state(self):
        """Stopping an audio player sets its state to 'stop'."""
        self.player.stop()

        self.assertEqual(
            AudioPlayer.STOP, self.player.state,
            'State of paused audio is not "stop"')

    def test_stopping_audio_dispatches_event(self):
        """Stopping audio dispatches the on_stop event."""
        mock_listener = Mock()
        self.player.add_listeners(on_stop=mock_listener)

        self.player.stop()

        mock_listener.assert_called_once_with(self.player)

    def test_looping_audio_restarts_on_finished(self):
        """Looping audio restarts playback when the source finishes."""
        self.player.looping = True

        # Get the callback for when the source playback is finished and call it
        player_event_listeners = self.mock_player.push_handlers.call_args[1]
        playback_finished_callback = player_event_listeners['on_player_eos']

        playback_finished_callback()

        # Verify playback was reset to the beginning
        self.mock_player.seek.assert_called_once_with(0)
        self.mock_player.play.assert_called_once()

    def test_non_looping_audio_dispatches_event_on_finished(self):
        """Non-looping audio dispatches the on_stop event on completion."""
        self.player.looping = False

        # Listen for the on_stop event
        mock_listener = Mock()
        self.player.add_listeners(on_stop=mock_listener)

        # Get the callback for when the source playback is finished and call it
        player_event_listeners = self.mock_player.push_handlers.call_args[1]
        playback_finished_callback = player_event_listeners['on_player_eos']

        playback_finished_callback()

        # Verify the state was set to STOP and the on_stop event dispatched
        self.assertEqual(
            AudioPlayer.STOP, self.player.state,
            'State of paused audio is not "stop"')
        mock_listener.assert_called_once_with(self.player)

    def test_setting_volume_sets_player_volume(self):
        """Setting volume sets the volume of the underlying player object."""
        self.player.volume = 0.5

        self.assertEqual(
            0.5, self.player.volume,
            'Volume was not set on player')

        self.assertEqual(
            0.5, self.mock_player.volume,
            'Volume was not set on underlying player')

    def test_setting_position_updates_player_in_3d(self):
        """Setting a 2d position sets the underlying player object in 3d."""
        self.player.position = (1, 2)

        self.assertEqual(
            (1, 2), self.player.position,
            'Player position was not set')

        self.assertEqual(
            (1, 2, 0), self.mock_player.position,
            'Underlying player position was not set in 3d')

    def test_setting_attenuation_distance_updates_player(self):
        """Setting attenuation distance sets the underlying player object."""
        self.player.attenuation_distance = 50

        self.assertEqual(
            50, self.player.attenuation_distance,
            'Player attenuation distance was not set')

        self.assertEqual(
            50, self.mock_player.min_distance,
            'Underlying player attenuation distance was not set')

    @patch('pyglet.media.Player')
    def test_removes_player_reference_on_destruction(self, MockPlayer):
        """Destroying an audio player frees its player reference."""
        # Initial references to the player object, held by mock framework
        initial_refs = gc.get_referrers(MockPlayer.return_value)

        # Instantiating an audio player creates references to the player object
        audio_player = AudioPlayer(self.mock_source)

        # Get a list of all player object references added after instantiation
        refs_after_init = gc.get_referrers(MockPlayer.return_value)
        added_refs = [ref
                      for ref in refs_after_init
                      if ref not in initial_refs]

        # Destroy the audio player object and mock player object's calls
        MockPlayer.reset_mock(return_value=True)
        del audio_player
        gc.collect()

        # Get a list of all player object references removed after destruction
        refs_after_destruction = gc.get_referrers(MockPlayer.return_value)
        removed_refs = [ref
                        for ref in added_refs
                        if ref not in refs_after_destruction]

        # Expect the added references to have been removed
        self.assertEqual(
            added_refs, removed_refs,
            'Audio player destruction did not free refs to player object')

    @patch('pyglet.media.Player')
    def test_removes_source_reference_on_destruction(self, MockPlayer):
        """Destroying an audio player frees its player reference."""
        mock_source = Mock()

        # Initial references to the sourc object, held by mock framework
        initial_refs = gc.get_referrers(mock_source.return_value)

        # Instantiating an audio player creates references to the source object
        audio_player = AudioPlayer(mock_source)

        # Get a list of all source object references added after instantiation
        refs_after_init = gc.get_referrers(mock_source.return_value)
        added_refs = [ref
                      for ref in refs_after_init
                      if ref not in initial_refs]

        # Destroy the audio player object and mock sources object's calls
        mock_source.reset_mock(return_value=True)
        del audio_player
        gc.collect()

        # Get a list of all player object references removed after destruction
        refs_after_destruction = gc.get_referrers(mock_source.return_value)
        removed_refs = [ref
                        for ref in added_refs
                        if ref not in refs_after_destruction]

        # Expect the added references to have been removed
        self.assertEqual(
            added_refs, removed_refs,
            'Audio player destruction did not free refs to source object')
