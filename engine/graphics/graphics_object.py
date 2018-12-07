import pyglet.sprite


class GraphicsObject(object):
    """On-screen graphic supporting multiple display states.

    The display states specify which image is displayed when rendering.
    Only the 'default' state is required, additional states can be added
    as needed.

    If a GraphicsObject is set to a state not contained within
    the display states, the rendered graphic will not change.

    GraphicsObjects support batches and groups for efficient rendering.

    Attributes:
        coordinates (:obj:`engine.geometry.Point2d`):
            Coordinates of the bottom left corner.
    """

    def __init__(self, coordinates, display_states, batch=None, group=None):
        """Creates an on-screen graphic supporting multiple display states.

        Args:
            coordinates (:obj:`engine.geometry.Point2d`):
                Coordinates of the bottom left edge.
            display_states (dict of str to :obj:`pyglet.image.Texture`):
                A mapping of state names to image objects. The 'default' state
                is required or a ``KeyError`` is raised.

                A possible valid ``display_states`` value would be::

                    {
                        'default':   idle_image,
                        'activated': activated_image,
                        'flashing': GraphicsObjects.create_animation(
                            flashing_image_grid[0:4], 500, loop=True)
                    }

        Kwargs:
            batch (:obj:`pyglet.graphics.Batch`, optional): The batch to render
                this graphic with. Defaults to None.
            group (:obj:`pyglet.graphics.Group`, optional): The group to render
                this graphic within. Defaults to None.

        Raises:
            KeyError: If ``display_states`` was missing the 'default' state.
        """
        super(GraphicsObject, self).__init__()
        self.coordinates = coordinates

        self._display_states = display_states
        self._sprite = pyglet.sprite.Sprite(
            display_states['default'], x=coordinates.x, y=coordinates.y,
            batch=batch, group=group)
        self._scale = [1, 1]
        self._offset = [0, 0]

    def update(self, dt):
        """Updates the position and scaling of the graphic.

        Args:
            dt (int): The elapsed time in milliseconds
        """
        self._sprite.update(
            x=(self.coordinates.x + self._offset[0]),
            y=(self.coordinates.y + self._offset[1]),
            scale_x=self._scale[0],
            scale_y=self._scale[1])

    def scale_x(self, scale):
        """Sets the horizontal scaling of the graphic.

        Negative scaling can be used to flip the graphic horizontally.

        Args:
            scale (int): The horizontal scaling to apply.
        """
        self._scale[0] = scale
        self._offset[0] = abs(scale) * self._sprite.width if scale < 0 else 0

    def scale_y(self, scale):
        """Sets the vertical scaling of the graphic.

        Negative scaling can be used to flip the graphic vertically.

        Args:
            scale (int): The vertical scaling to apply.
        """
        self._scale[1] = scale
        self._offset[1] = abs(scale) * self._sprite.height if scale < 0 else 0

    def set_position(self, coordinates):
        """Sets the position of the graphic's lower left corner on-screen.

        Args:
            coordinates (tuple of int): The coordinates at which to render
            the graphic's lower left corner.
        """
        self.coordinates.set(coordinates)

    @property
    def batch(self):
        """Returns the graphics batch for this graphics object."""
        return self._sprite.batch

    @batch.setter
    def batch(self, batch):
        """Sets the graphics batch for this object. Can be expensive."""
        self._sprite.batch = batch

    @classmethod
    def create_animation(cls, frames, duration, loop=True):
        """Creates an animation from a list of images.

        Frames can be sliced from an image grid using list slicing.

            GraphicsObject.create_animation(image_grid[0:4], 1.5, loop=True)

        Args:
            indices (list of :obj:`pyglet.image.AbstractImage`):
                List of animation frames, in display order.
            duration (float): Duration of each frame, in seconds.

        Kwargs:
            loop (bool, optional): Whether the animation loops indefinitely.
                Defaults to True.

        Returns:
            A :obj:`pyglet.image.Animation` created from the given frames.
        """
        # Create an animation from the given frames
        animation = pyglet.image.Animation.from_image_sequence(
            frames, duration, loop=loop)

        return animation
