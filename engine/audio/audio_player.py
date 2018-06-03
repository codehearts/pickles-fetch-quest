from .exceptions import DuplicateAudioStreamException
from ..event_dispatcher import EventDispatcher
import pyglet.media


class AudioPlayer(pyglet.media.Player, EventDispatcher):
    """Audio player with playback control for audio files on disk.

    See :cls:`event_dispatcher.EventDispatcher` for usage information on the
    event dispatcher.

    Attributes:
        loop (bool): True to loop playback of the audio. Defaults to False.
        volume (float): 0 for silence, 1 for full volume.
            Affected by the ``position`` attribute. Defaults to 1.
        position (tuple of float): 3D coordinates for audio location in space.
            Affects the volume attribute based on the listener source.
            Defaults to (0, 0, 0).

    Events:
        on_play: The audio player has begun playing.
            The player will be passed to the listeners.
        on_pause: The audio player has been paused.
            The player will be passed to the listeners.
        on_stop: The audio player has been stopped.
            The player will be passed to the listeners.
        on_finish: The audio player has completed playback.
    """

    def __init__(self, audio, loop=False):
        """Creates an audio player for controlling playback of audio files.

        Args:
            audio (:obj:`pyglet.media.Source`): An audio file read from disk.

        Kwargs:
            loop (bool, optional): True to loop when audio playback completes.
        """
        super(AudioPlayer, self).__init__()

        self.register_event_type('on_play')
        self.register_event_type('on_pause')
        self.register_event_type('on_stop')
        self.register_event_type('on_finish')

        self.add_listeners(on_player_eos=self._playback_finished)

        self._position = (0, 0, 0)
        self._volume = 1
        self.loop = loop

        try:
            self.queue(audio)
        except pyglet.media.MediaException as e:
            raise DuplicateAudioStreamException(
                'Only one player can exist for streaming audio.')

    def play(self):
        """Plays audio from where it left off.

        Dispatches an ``on_play`` event with this player.
        """
        super(AudioPlayer, self).play()
        self.dispatch_event('on_play', self)

    def pause(self):
        """Pauses the audio source at its current timestamp.

        Dispatches an ``on_pause`` event with this player.
        """
        super(AudioPlayer, self).pause()
        self.dispatch_event('on_pause', self)

    def stop(self):
        """Stops the audio source, resetting its timestamp to the beginning.

        Dispatches an ``on_stop`` event with this player.
        """
        super(AudioPlayer, self).pause()
        super(AudioPlayer, self).seek(0)
        self.dispatch_event('on_stop', self)

    def restart(self):
        """Plays the audio source from the beginning.

        Dispatches an ``on_stop`` event with this player followed by an
        ``on_play`` event with this player.
        """
        self.stop()
        self.play()

    def _playback_finished(self):
        """Called when playback of the audio source has finished.

        Dispatches an ``on_finish`` event with this player.
        """
        self.dispatch_event('on_finish', self)

    @property
    def position(self):
        """The three dimensional location in space of this player's audio.

        Returns:
            A tuple of floats representing the x, y, and z coordinates.
        """
        return self._position

    @position.setter
    def position(self, coordinates):
        """Sets the position of this player's audio in space.

        Args:
            coordinates (tuple of float): The x, y, and z coordinates in space.
        """
        self._position = coordinates

    @property
    def volume(self):
        """Sets the volume of this player.

        Returns:
            The volume level as a float; 0 for silence and 1 for full volume.
        """
        return self._volume

    @volume.setter
    def volume(self, level):
        """Sets the volume of this player.

        Args:
            level (float): A value between 0.0 (silence) and 1.0 (full volume).
        """
        self._volume = level
