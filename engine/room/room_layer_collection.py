from collections import OrderedDict


class RoomLayerCollection(object):
    """Collection of multiple layers for a room."""

    def __init__(self, width, height):
        """Creates a new collection of ordered room layers.

        Args:
            width (int): The width of the collection in pixels.
            height (int): The height of the collection in pixels.
        """
        super(RoomLayerCollection, self).__init__()

        self._layers = OrderedDict()
        self._width = width
        self._height = height

    def add_layer(self, name, layer):
        """Adds a layer to the end of the collection, rendering it on top.

        Args:
            name (str): Name of the layer, for easy access.
            layer (:obj:`engine.room.RoomLayer`):
                Layer to add to the collection.
        """
        self._layers[name] = layer

    def get_layer(self, name):
        """Returns the layer with the given name.

        Args:
            name (str): Name of the layer.

        Returns:
            The :obj:`engine.room.RoomLayer` with the given name.
        """
        return self._layers[name]

    def update(self, dt):
        """Updates each layer in the collection.

        The first layer inserted is the first updated.

        Args:
            dt (int): Elapsed time since last update, in milliseconds
        """
        for name, layer in self._layers.items():
            layer.update(dt)

    def draw(self):
        """Draws each layer in the collection.

        The first layer inserted is the first drawn.
        """
        for name, layer in self._layers.items():
            layer.draw()

    @property
    def width(self):
        """Returns the pixel width of the collection."""
        return self._width

    @property
    def height(self):
        """Returns the pixel height of the collection."""
        return self._height
