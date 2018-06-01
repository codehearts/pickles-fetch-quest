import pyglet.resource


class DiskLoader(object):
    """Singleton for loading resources stored on disk."""

    @classmethod
    def set_resource_paths(cls, resource_paths):
        """Sets the paths to load resources from.

        Args:
            resource_path (list of :obj:`str`): Paths relative to __main__
                to load resources from.
        """
        pyglet.resource.path = resource_paths
        pyglet.resource.reindex()  # Refresh the path index

    @classmethod
    def load_image(cls, filename):
        """Loads an image file from disk.

        Args:
            filename (:obj:`str`): The name of the image file, relative to
                the resource path.

        Returns:
            A :obj:`pyglet.image.Texture` for the loaded image.
        """
        return pyglet.resource.image(filename)

    @classmethod
    def load_audio(cls, filename, streaming=True):
        """Loads an audio file from disk.

        Args:
            filename (:obj:`str`): The name of the audio file, relative to
                the resource path.

        Kwargs:
            streaming (bool, optional): True to stream audio from disk rather
                than loading the entire audio file into memory. Only one
                instance of a streaming audio file can be played at once.
                Use this for longer audio files.

        Returns:
            A :obj:`pyglet.media.Source` for the loaded audio.
        """
        return pyglet.resource.media(filename, streaming=streaming)
