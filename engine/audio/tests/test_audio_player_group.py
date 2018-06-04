from ..audio_player_group import AudioPlayerGroup
from unittest.mock import call, Mock
import unittest


class TestAudioPlayerGroup(unittest.TestCase):
    """Test controlling playback of a group of audio players."""

    def setUp(self):
        """Provides each test case with the following properties::

            self.mock: Mock containing mocked players.
            self.mock.a: Mock for an audio player.
            self.mock.b: Mock for an audio player.
            self.mock.c: Mock for an audio player.
            self.group: An AudioPlayerGroup created with mocks a, b, and c.
        """
        self.mock = Mock()
        self.mock.a = Mock()
        self.mock.b = Mock()
        self.mock.c = Mock()

        self.group = AudioPlayerGroup([self.mock.a, self.mock.b, self.mock.c])

    def test_audio_player_group_can_be_added_to(self):
        """More players can be added to an existing group."""
        self.mock.d = Mock()
        self.group.add(self.mock.d)

        self.group.pause()

        # Assert that the new player mock D is called last
        self.mock.assert_has_calls([
            call.a.pause(), call.b.pause(), call.c.pause(), call.d.pause()])

    def test_audio_player_group_resumes_playing_audio(self):
        """Resuming a group plays only member players that were playing."""
        # Call the on_play listener for mock B
        self.mock.b.method_calls[0][2]['on_play'](self.mock.b)

        self.group.resume()

        # Assert only player mock B had its play method called
        self.mock.a.play.assert_not_called()
        self.mock.b.play.assert_called_once()
        self.mock.c.play.assert_not_called()

    def test_audio_player_group_does_not_resume_stopped_audio(self):
        """Resuming a group doesn't play stopped audio."""
        # Call the on_play listener followed by the on_stop for mock C
        self.mock.c.method_calls[0][2]['on_play'](self.mock.c)
        self.mock.c.method_calls[0][2]['on_stop'](self.mock.c)

        self.group.resume()

        # Assert no player mocks had their play method called
        self.mock.a.play.assert_not_called()
        self.mock.b.play.assert_not_called()
        self.mock.c.play.assert_not_called()

    def test_audio_player_group_does_not_resume_finished_audio(self):
        """Resuming a group doesn't play audio that finished playback."""
        # Call the on_play listener followed by the on_finish for mock A
        self.mock.a.method_calls[0][2]['on_play'](self.mock.a)
        self.mock.a.method_calls[0][2]['on_finish'](self.mock.a)

        self.group.resume()

        # Assert no player mocks had their play method called
        self.mock.a.play.assert_not_called()
        self.mock.b.play.assert_not_called()
        self.mock.c.play.assert_not_called()

    def test_audio_player_group_pauses(self):
        """Pausing a group pauses all member players in order."""
        self.group.pause()
        self.mock.assert_has_calls([
            call.a.pause(), call.b.pause(), call.c.pause()])

    def test_audio_player_group_stops(self):
        """Stopping a group stops all member players in order."""
        self.group.stop()
        self.mock.assert_has_calls([
            call.a.stop(), call.b.stop(), call.c.stop()])

    def test_audio_player_group_sets_volume(self):
        """Setting volume of a group set volume for all member players."""
        self.group.set_volume(0.5)
        self.assertEqual(0.5, self.mock.a.volume, "Mock A volume was not set")
        self.assertEqual(0.5, self.mock.b.volume, "Mock B volume was not set")
        self.assertEqual(0.5, self.mock.c.volume, "Mock C volume was not set")
