from .audio_player import AudioPlayer


class AudioSource(object):
    """Configures playback parameters for an audio source.

    Playing an :obj:`audio.AudioSource` creates a new :obj:`audio.AudioPlayer`
    from its playback parameters, and provides control for all existing player
    instances.

    Attributes:
        streaming (bool, read only): True if the audio source is streaming from
            disk, False if the audio source is loaded into memory. Streaming
            audio sources only support one instance of an
            :obj:`audio.AudioPlayer` as a time.
        attenuation_distance (int): The distance from the listener before the
            audio source has attenuation applied. The volume of the source
            will remain nominal within this distance, and approach zero as it
            moves further away beyond this distance.
        position (tuple of int): The position of the audo source in
            two-dimensional space. :obj:`engine.audio.AudioDirector` uses this
            property to determine the volume of audio based on its distance
            from the listener.
        looping (bool): Whether the audio source loops its playback.
        volume (float): 0 for silence, 1 for nominal volume.
    """

    def __init__(self, source, streaming=False, position=(0, 0)):
        """Creates an audio source with default playback parameters.

        Args:
            source (:obj:`pyglet.media.Source`): Audio source to set playback
                parameters for.

        Kwargs:
            streaming (bool, optional): Whether this audio source is streaming.
                Defaults to False.
            position (tuple of int, optional): The location of this audio
                source in two-dimensional space. Defaults to (0, 0)
        """
        super(AudioSource, self).__init__()

        self._instances = []
        self._streaming = streaming
        self._source = source

        self._attenuation_distance = 1
        self.position = position
        self.looping = False
        self._volume = 1

    def play(self):
        """Plays an audio source, tracking the player internally.

        When the player's ``on_stop`` event is dispatched, the source will
        discard its strong reference to the player.

        If there are no instances playing, a new :obj:`audio.AudioPlayer`
        will be initialized and played. Otherwise, the first existing instance
        will be returned for streaming sources, and a new instance will be
        created for non-streaming sources.

        The returned instance will have the same properties as this source.
        The properties on the :obj:`audio.AudioPlayer` can be set directly to
        control the individual playback.

        Returns:
            An :obj:`audio.AudioPlayer` instance which has begun playback.
        """
        player = self._get_player()
        player.attenuation_distance = self._attenuation_distance
        player.position = self.position
        player.looping = self.looping
        player.volume = self.volume
        player.play()

        return player

    def pause(self):
        """Pauses all playback instances of this audio source."""
        for instance in self._instances:
            instance.pause()

    def resume(self):
        """Resumes all playback instances of this audio source."""
        for instance in self._instances:
            if instance.state is instance.PAUSE:
                instance.play()

    def stop(self):
        """Stops all playback instances of this audio source.

        Stopped instances are no longer tracked by this class to free memory.
        """
        for instance in self._instances:
            instance.stop()

    @property
    def streaming(self):
        """Whether the audio source is streaming. Read-only."""
        return self._streaming

    def _get_player(self):
        """Returns a player instance for playback and tracks it.

        If a new instance is created, a listener for its ``on_stop`` event will
        be added to untrack it once it stops.

        A new :obj:`audio.AudioPlayer` will always be returned if the source
        is not streaming or if no instance already exists for a streaming
        source. The existing instance will be returned if an instance already
        exists for a streaming source.

        Returns:
            A :obj:`audio.AudioPlayer` instance.
        """
        # Ensure no more than 1 player exists for streaming audio at a time
        if self._streaming and self._instances:
            player = self._instances[0]
        else:
            player = AudioPlayer(self._source)
            player.add_listeners(on_stop=self._remove_instance)
            self._instances.append(player)

        return player

    def _remove_instance(self, instance):
        """Removes tracking for the given player instance."""
        self._instances.remove(instance)

    @property
    def volume(self):
        """The volume level of the source as a float between 0 and 1."""
        return self._volume

    @volume.setter
    def volume(self, level):
        """Sets the volume of the source and all existing instances."""
        self._volume = level

        for instance in self._instances:
            instance.volume = self._volume

    @property
    def attenuation_distance(self):
        """Distance from the listener before the source volume attenuates."""
        return self._attenuation_distance

    @attenuation_distance.setter
    def attenuation_distance(self, distance):
        """Sets the attenuation distance of the source and all instances."""
        self._attenuation_distance = distance

        for instance in self._instances:
            instance.attenuation_distance = self._attenuation_distance
