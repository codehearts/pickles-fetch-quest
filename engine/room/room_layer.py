class RoomLayer(object):
    """Object layer within a room.

    Attributes:
        batch (:obj:`GraphicsBatch`): Rendering batch for objects on the layer.
    """

    def __init__(self, batch=None):
        """Creates a new layer for a room.

        Kwargs:
            batch (:obj:`GraphicsBatch`, optional): Batch for the layer.
        """
        super(RoomLayer, self).__init__()
        self.batch = batch
        self._objects = []

    def add_object(self, new_object):
        """Adds an object to the layer.

        Args:
            new_object (obj): An object to add to this layer.
        """
        self._objects.append(new_object)

    def update(self, dt):
        """Updates all objects on the layer.

        Each object on the layer will have its `update` method called with the
        delta time passed as the only argument.

        Args:
            dt (int): Elapsed time since last update, in milliseconds
        """
        for layer_object in self._objects:
            layer_object.update(dt)

    def draw(self):
        """Draws the layer.

        If the layer has a graphics batch, the batch will be drawn.
        Otherwise, all objects are drawn in their insertion order.
        """
        if self.batch:
            self.batch.draw()
        else:
            for layer_object in self._objects:
                layer_object.draw()

    def is_empty(self):
        """Returns true if the layer has no objects."""
        return not self._objects
