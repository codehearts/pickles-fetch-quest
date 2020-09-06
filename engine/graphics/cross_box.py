from pyglet.graphics import vertex_list
from pyglet.gl import GL_LINES


class CrossBox(object):
    """Draws the outline of a rectangle with diagonal lines through its center.

    This is done using OpenGL primitives and is ideal for debug purposes.
    """

    VERTEX_COUNT = 12

    def __init__(self, rectangle, color=(0, 0, 0), batch=None):
        """Creates a new cross box graphic.

        Args:
            rectangle (:obj:`engine.geometry.Rectangle`):
                Rectangular area to render the cross box around.

        Kwargs:
            color (tuple of 3 int, optional):
                An rgb tuple of the color to draw with. Defaults to black.
            batch (:obj:`engine.graphics.GraphicsBatch`, optional):
                The batch to render this graphic with. Defaults to None.
        """
        super(CrossBox, self).__init__()
        self._x, self._y = rectangle.x, rectangle.y

        gl_vertices = ('v2i', self._get_vertices(rectangle))
        gl_colors = ('c3B', color * self.VERTEX_COUNT)

        if batch:
            self._graphic = batch.add(
                self.VERTEX_COUNT, GL_LINES, None, gl_vertices, gl_colors)
        else:
            self._graphic = vertex_list(
                self.VERTEX_COUNT, gl_vertices, gl_colors)

    def set_position(self, coordinates):
        """Sets the position of the cross box's bottom left corner.

        Args:
            coordinates (tuple of int):
                New x and y coordinates for the lower left corner.
        """
        coordinate_delta = (coordinates[0] - self._x, coordinates[1] - self._y)

        # Update each vertex coordinate by the corresponding coordinate delta
        self._graphic.vertices = list(map(
            lambda current, delta: current + delta,
            self._graphic.vertices,
            coordinate_delta * self.VERTEX_COUNT))

        self._x, self._y = coordinates

    def _get_vertices(self, rectangle):
        """Returns the vertices for a cross box around the rectangle."""
        x, x2 = rectangle.x, rectangle.x + rectangle.width
        y, y2 = rectangle.y, rectangle.y + rectangle.height

        return (
            x,  y,  x2, y,
            x,  y,  x,  y2,
            x2, y,  x,  y2,
            x,  y2, x2, y2,
            x2, y2, x,  y,
            x2, y2, x2, y
        )
