from engine import event_dispatcher
import pyglet.media


class AudioPlayer(event_dispatcher.EventDispatcher):
    """Playback control for an audio source.

    See :cls:`engine.event_dispatcher.EventDispatcher` for usage information on
    the event dispatcher.

    Attributes:
        position (tuple of int): The position of the audio source in
            two-dimensional space. :obj:`engine.audio.AudioDirector` uses this
            property to determine the volume of audio based on its distance
            from the listener.
        looping (bool): Whether the audio source loops its playback.
        volume (float): 0 for silence, 1 for nominal volume.
        state (int): The current state of the audio playback. Will be one of
            ``AudioPlayer.PLAY``, ``AudioPlayer.PAUSE``, ``AudioPlayer.STOP``.

    Events:
        on_play: The audio player has begun playing.
            The player will be passed to the listener.
        on_pause: The audio player has been paused.
            The player will be passed to the listener.
        on_stop: The audio player has been stopped or finished playback.
            The player will be passed to the listener.
    """

    PLAY = 0
    PAUSE = 1
    STOP = 2

    def __init__(self, source, position=(0, 0)):
        """Creates an audio player to control playback of an audio source.

        Args:
            source (:obj:`pyglet.media.Source`): Audio source for playback.

        Kwargs:
            position (tuple of int, optional): The location of this audio
                player in two-dimensional space. Defaults to (0, 0).
        """
        super(AudioPlayer, self).__init__()

        self.register_event_type('on_play')
        self.register_event_type('on_pause')
        self.register_event_type('on_stop')

        self._player = pyglet.media.Player()
        self._player.push_handlers(on_player_eos=self._playback_finished)
        self._player.queue(source)

        self.looping = False
        self.state = AudioPlayer.STOP
        self._position = position

    def play(self):
        """Plays audio from where it left off.

        Dispatches an ``on_play`` event with this player.
        """
        self._player.play()
        self.state = AudioPlayer.PLAY
        self.dispatch_event('on_play', self)

    def pause(self):
        """Pauses the audio source at its current timestamp.

        Dispatches an ``on_pause`` event with this player.
        """
        self._player.pause()
        self.state = AudioPlayer.PAUSE
        self.dispatch_event('on_pause', self)

    def stop(self):
        """Stops the audio source, resetting its timestamp to the beginning.

        Dispatches an ``on_stop`` event with this player.
        """
        self._player.pause()
        self._player.seek(0)

        self.state = AudioPlayer.STOP
        self.dispatch_event('on_stop', self)

    def _playback_finished(self):
        """Called when playback of the audio source has finished.

        If the player is looping, playback will resume from the beginning of
        the audio source. If the player is not looping, an ``on_stop`` event
        will be dispatched with this player instance.
        """
        if self.looping:
            self._player.seek(0)
            self._player.play()
        else:
            self.state = AudioPlayer.STOP
            self.dispatch_event('on_stop', self)

    @property
    def volume(self):
        """The volume level of the player as a float between 0 and 1."""
        return self._player.volume

    @volume.setter
    def volume(self, level):
        """Sets the volume of the audio player."""
        self._player.volume = level

    @property
    def position(self):
        """The position of the player in 2d space as a tuple-like type."""
        return self._position

    @position.setter
    def position(self, position):
        """Sets the player's location in 2d space using a tuple-like object."""
        self._position = position

        # Pyglet uses 3d coordinates, convert 2d to a 3d tuple
        self._player.position = (position[0], position[1], 0)

    @property
    def attenuation_distance(self):
        """Distance from the listener before the player volume attenuates."""
        return self._player.min_distance

    @attenuation_distance.setter
    def attenuation_distance(self, distance):
        """Sets the attenuation distance of the player."""
        self._player.min_distance = distance
