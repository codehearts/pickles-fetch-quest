import pyglet.resource
import pyglet.image
import csv


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
    def load_image_grid(cls, filename, rows, columns, **kwargs):
        """Loads an image grid file from disk, such as a sprite sheet.

        Args:
            filename (:obj:`str`): The name of the image file, relative to
                the resource path.
            rows (int): Number of rows in the image grid.
            columns (int): Number of columns in the image grid.

        Kwargs:
            item_width (int, optional): Width of each column. Default is
                calculated as the image width divided by the number of columns.
            item_height (int, optional): Height of each row. Default is
                calculated as the image height divided by the number of rows.
            row_padding (int, optional): Number of pixels between each row,
                excluding the edges of the image. Defaults to 0.
            column_padding (int, optional): Number of pixels between each
                column, excluding the edges of the image. Defaults to 0.

        Returns:
            A :obj:`pyglet.image.ImageGrid` for the loaded image grid.
        """
        image = cls.load_image(filename)
        return pyglet.image.ImageGrid(image, rows, columns, **kwargs)

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

    @classmethod
    def load_csv(cls, path):
        """Loads a CSV from disk into a two dimensional list of entries.

        Args:
            path (str): Path to the CSV file, relative to the resource path.

        Returns:
            A list of entry lists, one list per each line.
        """
        with pyglet.resource.file(path, mode='r') as csv_file:
            csv_data = list(csv.reader(csv_file))

        return csv_data
