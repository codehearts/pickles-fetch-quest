from engine.geometry import Rectangle
import pyglet.sprite


class GraphicsObject(Rectangle):
    """On-screen graphics with dimensions and positioning.

    GraphicsObjects support batches and groups for efficient rendering.

    Attributes:
        coordinates (:obj:`engine.geometry.Point2d`):
            Coordinates of the bottom left corner.
    """

    def __init__(self, graphic, coordinates=(0, 0), batch=None, group=None):
        """Creates an on-screen graphic supporting multiple display states.

        Args:
            graphic (:obj:`pyglet.image.Texture`):
                The image to render for this graphic.

        Kwargs:
            coordinates (:obj:`engine.geometry.Point2d`, optional):
                Coordinates of the bottom left edge. Defaults to (0, 0).
            batch (:obj:`engine.graphics.GraphicsBatch`, optional):
                The batch to render this graphic with. Defaults to None.
            group (:obj:`pyglet.graphics.Group`, optional):
                The group to render this graphic within. Defaults to None.
        """
        self._sprite = pyglet.sprite.Sprite(
            graphic, coordinates[0], coordinates[1], batch=batch, group=group)
        self._offset = [0, 0]
        self._scale = [1, 1]

        super(GraphicsObject, self).__init__(
            *coordinates, self._sprite.width, self._sprite.height)

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
        self._set_scale_offset(scale, 0)

    def scale_y(self, scale):
        """Sets the vertical scaling of the graphic.

        Negative scaling can be used to flip the graphic vertically.

        Args:
            scale (int): The vertical scaling to apply.
        """
        self._scale[1] = scale
        self._set_scale_offset(scale, 1)

    def _set_scale_offset(self, scale, index):
        """Maintains a bottom-left anchor by offsetting the sprite."""
        dimension = 'width' if index == 0 else 'height'
        sprite_dimension = getattr(self._sprite, dimension)

        self._offset[index] = abs(scale) * sprite_dimension if scale < 0 else 0

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
