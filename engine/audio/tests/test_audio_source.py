from ..audio_source import AudioSource
from unittest.mock import Mock, patch
import unittest
import gc


class TestAudioSource(unittest.TestCase):
    """Test management of audio source playback."""

    def setUp(self):
        """Provides each test case with the following properties::

            self.mock_source: Mock for the audio source from disk.
        """
        self.mock_source = Mock()

    def test_create_audio_source(self):
        """Creating an AudioSource applies constructor arguments."""
        mock_streaming = Mock()
        mock_position = Mock()
        audio_source = AudioSource(
            self.mock_source, streaming=mock_streaming, position=mock_position)

        self.assertEqual(
            mock_streaming, audio_source.streaming,
            'Streaming property was not set by constructor')
        self.assertEqual(
            mock_position, audio_source.position,
            'Position property was not set by constructor')

    @patch('engine.audio.audio_source.AudioPlayer')
    def test_playing_source_sets_properties(self, MockPlayer):
        """Playing an audio source sets its properties on the player."""
        mock_player_instance = MockPlayer.return_value
        audio_source = AudioSource(self.mock_source)

        mock_attenuation_distance = Mock()
        mock_position = Mock()
        mock_looping = Mock()
        mock_volume = Mock()

        audio_source.attenuation_distance = mock_attenuation_distance
        audio_source.position = mock_position
        audio_source.looping = mock_looping
        audio_source.volume = mock_volume

        audio_source.play()

        self.assertEqual(
            mock_attenuation_distance,
            mock_player_instance.attenuation_distance,
            'Player was not initialized with source attenuation distance')
        self.assertEqual(
            mock_position, mock_player_instance.position,
            'Player was not initialized with source position')
        self.assertEqual(
            mock_looping, mock_player_instance.looping,
            'Player was not initialized with source looping')
        self.assertEqual(
            mock_volume, mock_player_instance.volume,
            'Player was not initialized with source volume')

    @patch('engine.audio.audio_source.AudioPlayer')
    def test_playing_source_sets_on_stop_listener(self, MockPlayer):
        """Playing an audio source sets an on_stop listener to remove it."""
        audio_source = AudioSource(self.mock_source)
        audio_source.play()

        MockPlayer.return_value.add_listeners.assert_called_once_with(
            on_stop=audio_source._remove_instance)

    @patch('engine.audio.audio_source.AudioPlayer')
    def test_first_play_of_streaming_source(self, MockPlayer):
        """The first play of a streaming source creates a new player."""
        audio_source = AudioSource(self.mock_source, streaming=True)

        audio_source.play()

        MockPlayer.assert_called_once_with(self.mock_source)
        MockPlayer.return_value.play.assert_called_once()

    @patch('engine.audio.audio_source.AudioPlayer')
    def test_second_play_of_streaming_source(self, MockPlayer):
        """The second play of a streaming source returns existing player."""
        # Return a different mock on each instantiation of AudioPlayer
        instance_1, instance_2 = Mock(), Mock()
        MockPlayer.side_effect = [instance_1, instance_2]

        audio_source = AudioSource(self.mock_source, streaming=True)

        player_1 = audio_source.play()
        player_2 = audio_source.play()

        self.assertEqual(
            player_1, player_2,
            'Multiple plays of streaming sources did not return same instance')

        # Verify only one instance was constructed
        MockPlayer.assert_called_once_with(self.mock_source)
        self.assertEqual(
            2, instance_1.play.call_count,
            'Calling play on source did not call play on player each time')

    @patch('engine.audio.audio_source.AudioPlayer')
    def test_first_play_of_non_streaming_source(self, MockPlayer):
        """The first play of a non-streaming source creates a new player."""
        audio_source = AudioSource(self.mock_source, streaming=False)

        audio_source.play()

        MockPlayer.assert_called_once_with(self.mock_source)
        MockPlayer.return_value.play.assert_called_once()

    @patch('engine.audio.audio_source.AudioPlayer')
    def test_second_play_of_non_streaming_source(self, MockPlayer):
        """Each play of a streaming source creates a new player."""
        # Return a different mock on each instantiation of AudioPlayer
        instance_1, instance_2 = Mock(), Mock()
        MockPlayer.side_effect = [instance_1, instance_2]

        audio_source = AudioSource(self.mock_source, streaming=False)

        player_1 = audio_source.play()
        player_2 = audio_source.play()

        self.assertNotEqual(
            player_1, player_2,
            'Multiple plays of non-streaming source did not create new player')

        # Verify two instance were constructed
        self.assertEqual(
            2, MockPlayer.call_count,
            'Two player instances were not created')
        instance_1.play.assert_called_once()
        instance_2.play.assert_called_once()

    @patch('engine.audio.audio_source.AudioPlayer')
    def test_pausing_source_pauses_all_instances(self, MockPlayer):
        """Pausing a source pauses all instances."""
        # Return a different mock on each instantiation of AudioPlayer
        instance_1, instance_2 = Mock(), Mock()
        MockPlayer.side_effect = [instance_1, instance_2]

        # Create two playing instances and then pause the source
        audio_source = AudioSource(self.mock_source)
        audio_source.play()
        audio_source.play()
        audio_source.pause()

        instance_1.pause.assert_called_once()
        instance_2.pause.assert_called_once()

    @patch('engine.audio.audio_source.AudioPlayer')
    def test_resuming_source_pauses_all_instances(self, MockPlayer):
        """Resuming a source resumes all paused instances."""
        # Return a different mock on each instantiation of AudioPlayer
        instance_1, instance_2, instance_3 = Mock(), Mock(), Mock()
        MockPlayer.side_effect = [instance_1, instance_2, instance_3]

        # Mock instance 1 and 3 to be paused
        mock_pause = Mock()
        instance_1.PAUSE = mock_pause
        instance_2.PAUSE = mock_pause
        instance_3.PAUSE = mock_pause
        instance_1.state = instance_1.PAUSE
        instance_3.state = instance_2.PAUSE

        # Create three playing instances
        audio_source = AudioSource(self.mock_source, streaming=False)
        audio_source.play()
        audio_source.play()
        audio_source.play()

        # Instance 1 and 3 are mocked as paused, so only they should resume
        audio_source.resume()

        self.assertEqual(
            2, instance_1.play.call_count,
            'First player was not resumed despite being paused')
        self.assertEqual(
            1, instance_2.play.call_count,
            'Second player was resumed despite not being paused')
        self.assertEqual(
            2, instance_3.play.call_count,
            'Third player was not resumed despite being paused')

    @patch('engine.audio.audio_source.AudioPlayer')
    def test_stopping_source_pauses_all_instances(self, MockPlayer):
        """Stopping a source stops all instances."""
        # Return a different mock on each instantiation of AudioPlayer
        instance_1, instance_2 = Mock(), Mock()
        MockPlayer.side_effect = [instance_1, instance_2]

        # Create two playing instances and then stop the source
        audio_source = AudioSource(self.mock_source)
        audio_source.play()
        audio_source.play()
        audio_source.stop()

        instance_1.stop.assert_called_once()
        instance_2.stop.assert_called_once()

    @patch('engine.audio.audio_source.AudioPlayer')
    def test_setting_volume_updates_instances(self, MockPlayer):
        """Setting source volume sets volume on all instances."""
        # Return a different mock on each instantiation of AudioPlayer
        instance_1, instance_2 = Mock(), Mock()
        MockPlayer.side_effect = [instance_1, instance_2]

        # Create two playing instances and then set the source volume
        audio_source = AudioSource(self.mock_source)
        audio_source.play()
        audio_source.play()
        audio_source.volume = 0.5

        self.assertEqual(0.5, audio_source.volume, 'Source volume not set')
        self.assertEqual(0.5, instance_1.volume, 'Instance 1 volume not set')
        self.assertEqual(0.5, instance_2.volume, 'Instance 2 volume not set')

    @patch('engine.audio.audio_source.AudioPlayer')
    def test_setting_attenuation_distance_updates_instances(self, MockPlayer):
        """Setting attenuation distance sets distance on all instances."""
        # Return a different mock on each instantiation of AudioPlayer
        instance_1, instance_2 = Mock(), Mock()
        MockPlayer.side_effect = [instance_1, instance_2]

        # Create two playing instances and then set the source volume
        audio_source = AudioSource(self.mock_source)
        audio_source.play()
        audio_source.play()
        audio_source.attenuation_distance = 50

        self.assertEqual(
            50, audio_source.attenuation_distance, 'Source distance not set')
        self.assertEqual(
            50, instance_1.attenuation_distance, 'Instance 1 distance not set')
        self.assertEqual(
            50, instance_2.attenuation_distance, 'Instance 2 distance not set')

    @patch('engine.audio.audio_source.AudioPlayer')
    def test_removes_reference_to_stopped_players(self, MockPlayer):
        """The on_stop listener set on each player frees its reference."""
        # Initial references to the player object, held by mock framework
        initial_refs = gc.get_referrers(MockPlayer.return_value)

        # Playing an audio source creates references to the player object
        audio_source = AudioSource(self.mock_source)
        audio_source.play()

        # Get a list of all player object references added after calling play
        refs_after_play = gc.get_referrers(MockPlayer.return_value)
        added_refs = [ref
                      for ref in refs_after_play
                      if ref not in initial_refs]

        # Obtain the on_stop listener callback from the call args
        listeners = MockPlayer.return_value.add_listeners.call_args
        on_stop_listener = listeners[1]['on_stop']

        # Call the on_stop listener and reset the mock player object's calls
        on_stop_listener(MockPlayer.return_value)
        MockPlayer.reset_mock(return_value=True)
        gc.collect()

        # Get a list of all player object references removed after on_stop
        refs_after_listener = gc.get_referrers(MockPlayer.return_value)
        removed_refs = [ref
                        for ref in added_refs
                        if ref not in refs_after_listener]

        # Expect the added references to have been removed
        self.assertEqual(
            added_refs, removed_refs,
            'Player on_stop event did not free refs held by audio source')

    @patch('engine.audio.audio_source.AudioPlayer')
    def test_removes_player_references_on_destruction(self, MockPlayer):
        """Destroying an audio source frees its player references."""
        # Initial references to the player object, held by mock framework
        initial_refs = gc.get_referrers(MockPlayer.return_value)

        # Playing an audio source creates references to the player object
        audio_source = AudioSource(self.mock_source)
        audio_source.play()

        # Get a list of all player object references added after calling play
        refs_after_play = gc.get_referrers(MockPlayer.return_value)
        added_refs = [ref
                      for ref in refs_after_play
                      if ref not in initial_refs]

        # Destroy the audio source object and mock player object's calls
        MockPlayer.reset_mock(return_value=True)
        audio_source = None
        gc.collect()

        # Get a list of all player object references removed after destruction
        refs_after_destruction = gc.get_referrers(MockPlayer.return_value)
        removed_refs = [ref
                        for ref in added_refs
                        if ref not in refs_after_destruction]

        # Expect the added references to have been removed
        self.assertEqual(
            added_refs, removed_refs,
            'Audio source destruction did not free refs to player object')
