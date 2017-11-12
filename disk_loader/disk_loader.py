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
