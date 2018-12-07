class Room(object):
    """Collection of rendering layers and objects.

    Attributes:
        layers (:obj:`engine.room.RoomLayerCollection`):
            Collection of layers for the room.
    """

    def __init__(self, layers):
        """Creates a new room.

        Args:
            layers (:obj:`engine.room.RoomLayerCollection`):
                Layers for the room.
        """
        super(Room, self).__init__()
        self.layers = layers

    def update(self, dt):
        """Updates all layers in the room.

        Args:
            dt (int): Elapsed time since last update, in milliseconds
        """
        self.layers.update(dt)

    def draw(self):
        """Draws all layers in the room."""
        self.layers.draw()
