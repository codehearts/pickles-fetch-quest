from ..disk_loader import DiskLoader
from .audio_source import AudioSource
import pyglet.media


class AudioDirector(object):
    """Director for loading audio and controlling playback.

    Attributes:
        attenuation_distance (int): The default attenuation distance for newly
            loaded audio. Existing audio will retain its attenuation distance,
            see :fn:`set_attenuation_distance` for setting distance on existing
            sources.
        master_volume (float): The master volume for audio playback.
            0 for silence, 1 for nominal volume. A value of 1 disables
            audio attenuation and ignore the position of audio sources.
            To avoid this, set volume to 0.99 or lower.
        position (tuple of int): The location of the audio listener in
            two-dimensional space. Listeners close to this position will be
            louder than those further away.
    """

    def __init__(self, master_volume=1, position=(0, 0)):
        """Creates a director for grouping and controlling audio playback.

        Kwargs:
            master_volume (float, optional): Master volume for audio playback.
                0 for silence, 1 for nominal volume. A value of 1 will disable
                audio attenuation and ignore the position of audio sources.
                To avoid this, set volume to 0.99 or lower. Defaults to 1.
            position (tuple of int, optional): The location of the audio
                listener in two-dimensional space. Listeners close to this
                position will be louder than those farther. Defaults to (0, 0).
        """
        super(AudioDirector, self).__init__()

        self.attenuation_distance = 1
        self.master_volume = master_volume
        self.position = position

        # Cache of loaded resources from disk
        self._disk_cache = {}

        # Groupings for audio sources
        self._groups = {
            'all': set()
        }

    def load(self, filepath, streaming=True):
        """Loads and audio file from disk.

        The loaded audio will be added to the 'all' group for this director.

        A cached object will be returned if the file has already been loaded.
        Streaming should be used for large audio sources, such as music.
        Only one instance of a streaming audio source can be played at a time.

        Args:
            filepath (str): Path to audio, relative to the resource directory.

        Kwargs:
            streaming (bool, optional): Streams the audio from disk rather
                than loading the entire file into memory. Defaults to True.

        Returns:
            An :obj:`audio.AudioSource` object for the resource on disk.
        """
        # Load the file from disk and cache it if necessary
        if filepath not in self._disk_cache:
            disk_file = DiskLoader.load_audio(filepath, streaming)
            new_source = AudioSource(disk_file, streaming)

            # Cache the new source
            self._disk_cache[filepath] = new_source

            # Apply the default attenuation distance
            new_source.attenuation_distance = self.attenuation_distance

            # Add this audio source to the default group
            self.add(new_source)

        return self._disk_cache[filepath]

    def add(self, audio_source, group='all'):
        """Adds an audio source to a group.

        Grouping audio allows you to control the playback of the entire group
        rather than an individual source instance. By default, the audio source
        is added to the 'all' group.

        Args:
            audio_source (:obj:`audio.AudioSource`): The audio source to add.

        Kwargs:
            group (str, optional): The group to add the audio to.
                Defaults to 'all'.
        """
        self._groups.setdefault(group, set()).add(audio_source)

    def play(self, group='all'):
        """Plays all audio sources in a group.

        Kwargs:
            group (str, optional): Name of group to play. Defaults to 'all'.
        """
        for audio_source in self._groups.get(group, []):
            audio_source.play()

    def pause(self, group='all'):
        """Pauses all playing audio sources in a group.

        Audio sources which are not currently playing will be left alone.

        Kwargs:
            group (str, optional): Name of group to pause. Defaults to 'all'.
        """
        for audio_source in self._groups.get(group, []):
            if audio_source.state is AudioSource.PLAY:
                audio_source.pause()

    def stop(self, group='all'):
        """Stops all audio sources in a group.

        Kwargs:
            group (str, optional): Name of group to stop. Defaults to 'all'.
        """
        for audio_source in self._groups.get(group, []):
            if audio_source.state is not AudioSource.STOP:
                audio_source.stop()

    def resume(self, group='all'):
        """Resumes playback of all paused audio sources in a group.

        Audio sources which are not currently paused will be left alone.

        Kwargs:
            group (str, optional): Name of group to resume. Defaults to 'all'.
        """
        for audio_source in self._groups.get(group, []):
            if audio_source.state is AudioSource.PAUSE:
                audio_source.play()

    def set_volume(self, level, group='all'):
        """Sets the volume of all audio sources in a group.

        Args:
            volume (float): 0 for silence, 1 for nominal volume.

        Kwargs:
            group (str, optional): Group to set volume of. Defaults to 'all'.
        """
        for audio_source in self._groups.get(group, []):
            audio_source.volume = level

    def set_attenuation_distance(self, distance, group='all'):
        """Sets the distance from the listener before player volumes attenuate.

        Args:
            distance (int): The distance from the listener before the source
                volume attenuates. Within this distance, the volume remains
                nominal. Outside this distance, the volume approaches zero.

        Kwargs:
            group (str, optional): Group to set distance of. Defaults to 'all'.
        """
        for audio_source in self._groups.get(group, []):
            audio_source.attenuation_distance = distance

    @property
    def position(self):
        """The position of the listener in 2d space as a tuple-like type."""
        return self._position

    @position.setter
    def position(self, position):
        """Sets the listener location in 2d space with a tuple-like object."""
        self._position = position

        # Pyglet uses 3d coordinates, convert 2d to a 3d tuple
        listener = pyglet.media.get_audio_driver().get_listener()
        listener.position = (position[0], position[1], 0)

    @property
    def master_volume(self):
        """Returns the master audio volume as a float between 0 and 1."""
        listener = pyglet.media.get_audio_driver().get_listener()
        return listener.volume

    @master_volume.setter
    def master_volume(self, level):
        """Sets the master audio playback volume.

        0 for silence, 1 for nominal volume. Setting this to 1 disables audio
        attenuation, ignoring the position of listeners. Set to 0.99 to
        allow for audio positioning.
        """
        listener = pyglet.media.get_audio_driver().get_listener()
        listener.volume = level
