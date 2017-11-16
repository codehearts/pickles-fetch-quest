import pyglet.sprite


class GraphicsObject(object):
    """On-screen graphic supporting multiple display states.

    The display states specify which image is displayed when rendering.
    Only the 'default' state is required, additional states can be added
    as needed.

    If a GraphicsObject is set to a state not contained within
    the display states, the rendered graphic will not change.

    GraphicsObjects support batches and groups for efficient rendering.
    """

    def __init__(self, display_states, x=0, y=0, batch=None, group=None):
        """Creates an on-screen graphic supporting multiple display states.

        Args:
            display_states (dict of :obj:`str`: :obj:`pyglet.image.Texture`):
                A mapping of state names to image objects. The 'default' state
                is required or a ``KeyError`` is raised.

                A possible valid ``display_states`` value would be::

                    {
                        'default':   idle_image,
                        'activated': activated_image
                    }
            x (int, optional): The x coordinate for the graphic's left edge.
                Defaults to 0.
            y (int, optional): The y coordinate for the graphic's bottom edge.
                Defaults to 0.
            batch (:obj:`pyglet.graphics.Batch`, optional): The batch to render
                this graphic with. Defaults to None.
            group (:obj:`pyglet.graphics.Group`, optional): The group to render
                this graphic within. Defaults to None.

        Raises:
            KeyError: If ``display_states`` was missing the 'default' state.
        """
        super(GraphicsObject, self).__init__()
        self._display_states = display_states
        self._sprite = pyglet.sprite.Sprite(
            display_states['default'], x=x, y=y, batch=batch, group=group)

    def set_position(self, coordinates):
        """Sets the position of the graphic's lower left corner on-screen.

        Args:
            coordinates (tuple of int): The coordinates at which to render
            the graphic's lower left corner.
        """
        self._sprite.position = coordinates
