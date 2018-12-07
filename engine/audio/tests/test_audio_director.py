from ..audio_director import AudioDirector
from unittest.mock import Mock, patch
import unittest


class TestAudioDirector(unittest.TestCase):
    """Test management of audio director sources."""

    @patch('pyglet.media.get_audio_driver')
    def setUp(self, mock_get_audio_driver):
        """Provides each test case with the following properties::

            self.director: An `AudioDirector` object.
        """
        # Stub the listener during construction in tests
        mock_listener = Mock()
        mock_get_audio_driver.return_value.get_listener = Mock(
            return_value=mock_listener)

        self.director = AudioDirector()

    @patch('pyglet.media.get_audio_driver')
    def test_position_can_be_set_via_constructor(self, mock_get_audio_driver):
        """Listener position can be set via the constructor."""
        mock_listener = Mock()
        mock_get_audio_driver.return_value.get_listener = Mock(
            return_value=mock_listener)

        director = AudioDirector(position=(1, 2))

        self.assertEqual(
            (1, 2), director.position, 'Director position was not set')
        self.assertEqual(
            (1, 2, 0), mock_listener.position, '3d listener position not set')

    @patch('pyglet.media.get_audio_driver')
    def test_volume_can_be_set_via_constructor(self, mock_get_audio_driver):
        """Master volume can be set via the constructor."""
        mock_listener = Mock()
        mock_get_audio_driver.return_value.get_listener = Mock(
            return_value=mock_listener)

        director = AudioDirector(master_volume=0.5)

        self.assertEqual(
            0.5, director.master_volume, 'Director volume was not set')
        self.assertEqual(
            0.5, mock_listener.volume, 'Listener volume not set')

    @patch('engine.audio.audio_director.AudioSource')
    @patch('engine.disk.DiskLoader')
    def test_load_creates_audio_source_from_disk(self, MockLoader, MockSource):
        """Audio files are read from disk on initial load."""
        stream_mock = Mock()

        loaded_source = self.director.load('audio.wav', streaming=stream_mock)

        # Audio file was read from disk
        MockLoader.load_audio.assert_called_once_with(
            'audio.wav', stream_mock)

        # Audio source was initialized from disk object
        MockSource.assert_called_once_with(
            MockLoader.load_audio.return_value, stream_mock)

        self.assertEqual(
            MockSource.return_value, loaded_source,
            'Loaded audio source was not returned from disk')

    @patch('engine.audio.audio_director.AudioSource')
    @patch('engine.disk.DiskLoader')
    def test_load_caches_audio_sources_from_disk(self, MockLoader, MockSource):
        """Audio files are returned from cache on subsequent loads."""
        loaded_source = self.director.load('audio.wav')

        # Reset mocks after initial load
        MockLoader.load_audio.reset_mock()
        MockSource.reset_mock()

        # Load the same file again
        self.director.load('audio.wav')

        # Nothing was loaded from disk, only cache was used
        MockLoader.load_audio.assert_not_called()
        MockSource.assert_not_called()

        self.assertEqual(
            MockSource.return_value, loaded_source,
            'Loaded audio source was not returned from cache')

    @patch('engine.audio.audio_director.AudioSource')
    @patch('engine.disk.DiskLoader')
    def test_load_adds_audio_source_to_all_group(self, MockLoader, MockSource):
        """Audio files are added to the 'all' group when loaded."""
        self.director.load('audio.wav')

        # Playing the 'all' group should play the loaded audio
        self.director.play()
        MockSource.return_value.play.assert_called_once()

    @patch('engine.audio.audio_director.AudioSource')
    @patch('engine.disk.DiskLoader')
    def test_load_sets_attenuation_distance(self, MockLoader, MockSource):
        """Audio files have their attenuation distance set when loaded."""
        self.director.attenuation_distance = 1234
        self.director.load('audio.wav')

        self.assertEqual(
            1234, MockSource.return_value.attenuation_distance,
            'Attenuation distance not set on loaded audio')

    def test_add_defaults_to_all_group(self):
        """Adding an audio source defaults to the 'all' group."""
        # Adding a source without a group should default to 'all' group
        mock_source = Mock()
        self.director.add(mock_source)

        # Playing the 'all' group should play the added source
        self.director.play()
        mock_source.play.assert_called_once()

    def test_add_to_group(self):
        """Adding an audio source places it in the specified group."""
        # Add a source to the 'test' group
        mock_source = Mock()
        self.director.add(mock_source, group='test')

        # Playing the 'test' group should play the added source
        self.director.play(group='test')
        mock_source.play.assert_called_once()

    def test_play_default_group(self):
        """Playing the default group plays all sources in the 'all' group."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock()
        mock_all_2 = Mock()
        mock_test_1 = Mock()
        mock_test_2 = Mock()

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        # Playing the default group should only play sources in 'all'
        self.director.play()

        mock_all_1.play.assert_called_once()
        mock_all_2.play.assert_called_once()
        mock_test_1.play.assert_not_called()
        mock_test_2.play.assert_not_called()

    def test_play_non_default_group(self):
        """Playing a non-default group plays all sources in that group."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock()
        mock_all_2 = Mock()
        mock_test_1 = Mock()
        mock_test_2 = Mock()

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        # Playing the 'test' group should only play sources in that group
        self.director.play(group='test')

        mock_all_1.play.assert_not_called()
        mock_all_2.play.assert_not_called()
        mock_test_1.play.assert_called_once()
        mock_test_2.play.assert_called_once()

    def test_play_empty_group(self):
        """Playing an empty group does nothing."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock()
        mock_all_2 = Mock()
        mock_test_1 = Mock()
        mock_test_2 = Mock()

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        # Playing the 'test' group should only play sources in that group
        self.director.play(group='empty')

        mock_all_1.play.assert_not_called()
        mock_all_2.play.assert_not_called()
        mock_test_1.play.assert_not_called()
        mock_test_2.play.assert_not_called()

    @patch('engine.audio.audio_director.AudioSource')
    def test_pause_only_pauses_playing_players(self, MockSource):
        """Only playing audio sources are paused."""
        # Add a playing and a paused source
        mock_all_1 = Mock(state=MockSource.PLAY)
        mock_all_2 = Mock(state=MockSource.PAUSE)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)

        self.director.pause()

        mock_all_1.pause.assert_called_once()
        mock_all_2.pause.assert_not_called()

    @patch('engine.audio.audio_director.AudioSource')
    def test_pause_default_group(self, MockSource):
        """Pausing the default group pauses all sources in the 'all' group."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock(state=MockSource.PLAY)
        mock_all_2 = Mock(state=MockSource.PLAY)
        mock_test_1 = Mock(state=MockSource.PLAY)
        mock_test_2 = Mock(state=MockSource.PLAY)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        # Pausing the default group should only pause sources in 'all'
        self.director.pause()

        mock_all_1.pause.assert_called_once()
        mock_all_2.pause.assert_called_once()
        mock_test_1.pause.assert_not_called()
        mock_test_2.pause.assert_not_called()

    @patch('engine.audio.audio_director.AudioSource')
    def test_pause_non_default_group(self, MockSource):
        """Pausing a non-default group pauses all sources in that group."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock(state=MockSource.PLAY)
        mock_all_2 = Mock(state=MockSource.PLAY)
        mock_test_1 = Mock(state=MockSource.PLAY)
        mock_test_2 = Mock(state=MockSource.PLAY)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        # Pausing the 'test' group should only pause sources in that group
        self.director.pause(group='test')

        mock_all_1.pause.assert_not_called()
        mock_all_2.pause.assert_not_called()
        mock_test_1.pause.assert_called_once()
        mock_test_2.pause.assert_called_once()

    @patch('engine.audio.audio_director.AudioSource')
    def test_pause_empty_group(self, MockSource):
        """Pausing an empty group does nothing."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock(state=MockSource.PLAY)
        mock_all_2 = Mock(state=MockSource.PLAY)
        mock_test_1 = Mock(state=MockSource.PLAY)
        mock_test_2 = Mock(state=MockSource.PLAY)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        # Pausing an empty group will do nothing
        self.director.pause(group='empty')

        mock_all_1.pause.assert_not_called()
        mock_all_2.pause.assert_not_called()
        mock_test_1.pause.assert_not_called()
        mock_test_2.pause.assert_not_called()

    @patch('engine.audio.audio_director.AudioSource')
    def test_stop_ignores_stopped_players(self, MockSource):
        """Sources which are currently stopped will not be stopped."""
        # Add a playing, paused, and stopped source
        mock_playing = Mock(state=MockSource.PLAY)
        mock_paused = Mock(state=MockSource.PAUSE)
        mock_stopped = Mock(state=MockSource.STOP)

        self.director.add(mock_playing)
        self.director.add(mock_paused)
        self.director.add(mock_stopped)

        # Only the playing and paused sources should be stopped
        self.director.stop()

        mock_playing.stop.assert_called_once()
        mock_paused.stop.assert_called_once()
        mock_stopped.stop.assert_not_called()

    @patch('engine.audio.audio_director.AudioSource')
    def test_stop_default_group(self, MockSource):
        """Stopping the default group stops all sources in the 'all' group."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock(state=MockSource.PLAY)
        mock_all_2 = Mock(state=MockSource.PLAY)
        mock_test_1 = Mock(state=MockSource.PLAY)
        mock_test_2 = Mock(state=MockSource.PLAY)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        # Stopping the default group should only stop sources in 'all'
        self.director.stop()

        mock_all_1.stop.assert_called_once()
        mock_all_2.stop.assert_called_once()
        mock_test_1.stop.assert_not_called()
        mock_test_2.stop.assert_not_called()

    @patch('engine.audio.audio_director.AudioSource')
    def test_stop_non_default_group(self, MockSource):
        """Stopping a non-default group stops all sources in that group."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock(state=MockSource.PLAY)
        mock_all_2 = Mock(state=MockSource.PLAY)
        mock_test_1 = Mock(state=MockSource.PLAY)
        mock_test_2 = Mock(state=MockSource.PLAY)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        # Stopping the 'test' group should only stop sources in that group
        self.director.stop(group='test')

        mock_all_1.stop.assert_not_called()
        mock_all_2.stop.assert_not_called()
        mock_test_1.stop.assert_called_once()
        mock_test_2.stop.assert_called_once()

    @patch('engine.audio.audio_director.AudioSource')
    def test_stop_empty_group(self, MockSource):
        """Stopping an empty group does nothing."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock(state=MockSource.PLAY)
        mock_all_2 = Mock(state=MockSource.PLAY)
        mock_test_1 = Mock(state=MockSource.PLAY)
        mock_test_2 = Mock(state=MockSource.PLAY)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        # Stopping an empty group will do nothing
        self.director.stop(group='empty')

        mock_all_1.stop.assert_not_called()
        mock_all_2.stop.assert_not_called()
        mock_test_1.stop.assert_not_called()
        mock_test_2.stop.assert_not_called()

    @patch('engine.audio.audio_director.AudioSource')
    def test_resume_only_resumes_paused_players(self, MockSource):
        """Only paused sources are resumed."""
        # Add a playing, paused, and stopped source
        mock_playing = Mock(state=MockSource.PLAY)
        mock_paused = Mock(state=MockSource.PAUSE)
        mock_stopped = Mock(state=MockSource.STOP)

        self.director.add(mock_playing)
        self.director.add(mock_paused)
        self.director.add(mock_stopped)

        # Only the paused sources should be resumed
        self.director.resume()

        mock_playing.play.assert_not_called()
        mock_paused.play.assert_called_once()
        mock_stopped.play.assert_not_called()

    @patch('engine.audio.audio_director.AudioSource')
    def test_resume_default_group(self, MockSource):
        """Resuming the default group resumes every source in 'all' group."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock(state=MockSource.PAUSE)
        mock_all_2 = Mock(state=MockSource.PAUSE)
        mock_test_1 = Mock(state=MockSource.PAUSE)
        mock_test_2 = Mock(state=MockSource.PAUSE)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        # Resuming the default group should only resume sources in 'all'
        self.director.resume()

        mock_all_1.play.assert_called_once()
        mock_all_2.play.assert_called_once()
        mock_test_1.play.assert_not_called()
        mock_test_2.play.assert_not_called()

    @patch('engine.audio.audio_director.AudioSource')
    def test_resume_non_default_group(self, MockSource):
        """Resuming a non-default group resumes all sources in that group."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock(state=MockSource.PAUSE)
        mock_all_2 = Mock(state=MockSource.PAUSE)
        mock_test_1 = Mock(state=MockSource.PAUSE)
        mock_test_2 = Mock(state=MockSource.PAUSE)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        # Resuming the 'test' group should only resume sources in that group
        self.director.resume(group='test')

        mock_all_1.play.assert_not_called()
        mock_all_2.play.assert_not_called()
        mock_test_1.play.assert_called_once()
        mock_test_2.play.assert_called_once()

    @patch('engine.audio.audio_director.AudioSource')
    def test_resume_empty_group(self, MockSource):
        """Resuming an empty group does nothing."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock(state=MockSource.PAUSE)
        mock_all_2 = Mock(state=MockSource.PAUSE)
        mock_test_1 = Mock(state=MockSource.PAUSE)
        mock_test_2 = Mock(state=MockSource.PAUSE)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        # Resuming an empty group will do nothing
        self.director.resume(group='empty')

        mock_all_1.play.assert_not_called()
        mock_all_2.play.assert_not_called()
        mock_test_1.play.assert_not_called()
        mock_test_2.play.assert_not_called()

    def test_set_volume_on_default_group(self):
        """Setting volume on the default group sets all sources in 'all'."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock(volume=1)
        mock_all_2 = Mock(volume=1)
        mock_test_1 = Mock(volume=1)
        mock_test_2 = Mock(volume=1)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        self.director.set_volume(0.5)

        self.assertEqual(
            0.5, mock_all_1.volume,
            'Volume not set on source in default group')
        self.assertEqual(
            0.5, mock_all_2.volume,
            'Volume not set on source in default group')
        self.assertEqual(
            1, mock_test_1.volume,
            'Volume set on source outside default group')
        self.assertEqual(
            1, mock_test_2.volume,
            'Volume set on source outside default group')

    def test_set_volume_on_non_default_group(self):
        """Setting volume on a non-default group sets all sources in it."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock(volume=1)
        mock_all_2 = Mock(volume=1)
        mock_test_1 = Mock(volume=1)
        mock_test_2 = Mock(volume=1)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        self.director.set_volume(0.5, group='test')

        self.assertEqual(
            1, mock_all_1.volume,
            'Volume set on source in different group')
        self.assertEqual(
            1, mock_all_2.volume,
            'Volume set on source in different group')
        self.assertEqual(
            0.5, mock_test_1.volume,
            'Volume not set on source in specified group')
        self.assertEqual(
            0.5, mock_test_2.volume,
            'Volume not set on source in specified group')

    def test_set_volume_on_empty_group(self):
        """Setting volume on an empty group does nothing."""
        mock_all_1 = Mock(volume=1)
        mock_all_2 = Mock(volume=1)
        mock_test_1 = Mock(volume=1)
        mock_test_2 = Mock(volume=1)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        self.director.set_volume(0.5, group='empty')

        self.assertEqual(
            1, mock_all_1.volume,
            'Volume set on source in different group')
        self.assertEqual(
            1, mock_all_2.volume,
            'Volume set on source in different group')
        self.assertEqual(
            1, mock_test_1.volume,
            'Volume set on source in different group')
        self.assertEqual(
            1, mock_test_2.volume,
            'Volume set on source in different group')

    def test_set_attenuation_distance_on_default_group(self):
        """Attenuation distance on the default group affects 'all' group."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock(attenuation_distance=1)
        mock_all_2 = Mock(attenuation_distance=1)
        mock_test_1 = Mock(attenuation_distance=1)
        mock_test_2 = Mock(attenuation_distance=1)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        self.director.set_attenuation_distance(50)

        self.assertEqual(
            50, mock_all_1.attenuation_distance,
            'Attenuation distance not set on source in default group')
        self.assertEqual(
            50, mock_all_2.attenuation_distance,
            'Attenuation distance not set on source in default group')
        self.assertEqual(
            1, mock_test_1.attenuation_distance,
            'Attenuation distance set on source outside default group')
        self.assertEqual(
            1, mock_test_2.attenuation_distance,
            'Attenuation distance set on source outside default group')

    def test_set_attenuation_distance_on_non_default_group(self):
        """Attenuation distance on non-default group sets all sources in it."""
        # Add 2 sources to the 'all' group and 2 to the 'test' group
        mock_all_1 = Mock(attenuation_distance=1)
        mock_all_2 = Mock(attenuation_distance=1)
        mock_test_1 = Mock(attenuation_distance=1)
        mock_test_2 = Mock(attenuation_distance=1)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        self.director.set_attenuation_distance(50, group='test')

        self.assertEqual(
            1, mock_all_1.attenuation_distance,
            'Attenuation distance not set on source in default group')
        self.assertEqual(
            1, mock_all_2.attenuation_distance,
            'Attenuation distance not set on source in default group')
        self.assertEqual(
            50, mock_test_1.attenuation_distance,
            'Attenuation distance set on source outside default group')
        self.assertEqual(
            50, mock_test_2.attenuation_distance,
            'Attenuation distance set on source outside default group')

    def test_set_attenuation_distance_on_empty_group(self):
        """Attenuation distance on an empty group does nothing."""
        mock_all_1 = Mock(attenuation_distance=1)
        mock_all_2 = Mock(attenuation_distance=1)
        mock_test_1 = Mock(attenuation_distance=1)
        mock_test_2 = Mock(attenuation_distance=1)

        self.director.add(mock_all_1)
        self.director.add(mock_all_2)
        self.director.add(mock_test_1, group='test')
        self.director.add(mock_test_2, group='test')

        self.director.set_attenuation_distance(50, group='empty')

        self.assertEqual(
            1, mock_all_1.attenuation_distance,
            'Attenuation distance not set on source in default group')
        self.assertEqual(
            1, mock_all_2.attenuation_distance,
            'Attenuation distance not set on source in default group')
        self.assertEqual(
            1, mock_test_1.attenuation_distance,
            'Attenuation distance set on source outside default group')
        self.assertEqual(
            1, mock_test_2.attenuation_distance,
            'Attenuation distance set on source outside default group')

    @patch('pyglet.media.get_audio_driver')
    def test_setting_position_sets_listener(self, mock_get_audio_driver):
        """Listener position is updated in 3d when setting position."""
        mock_listener = Mock()
        mock_get_audio_driver.return_value.get_listener = Mock(
            return_value=mock_listener)

        self.director.position = (1, 2)

        self.assertEqual(
            (1, 2), self.director.position, 'Director position was not set')
        self.assertEqual(
            (1, 2, 0), mock_listener.position, '3d listener position not set')

    @patch('pyglet.media.get_audio_driver')
    def test_setting_master_volume_sets_listener(self, mock_get_audio_driver):
        """Master volume is set on listener."""
        mock_listener = Mock()
        mock_get_audio_driver.return_value.get_listener = Mock(
            return_value=mock_listener)

        self.director.master_volume = 0.5

        self.assertEqual(
            0.5, self.director.master_volume, 'Director volume was not set')
        self.assertEqual(
            0.5, mock_listener.volume, 'Listener volume not set')
