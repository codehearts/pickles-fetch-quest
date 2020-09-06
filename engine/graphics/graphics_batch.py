from pyglet.gl import glPushAttrib, glPopAttrib, glEnable, GL_ENABLE_BIT
from pyglet.gl import glLineStipple, GL_LINE_STIPPLE
from pyglet.graphics import Batch


class GraphicsBatch(Batch):
    """Manages a set of objects to draw together for efficiency.

    A :obj:`engine.graphics.GraphicsBatch` object can be passed as a
    constructor argument to a :obj:`engine.graphics.GraphicsObject` to add that
    object to the batch.

    Batches can be rendered with additional special properties:

    * ``DASHED_LINES``: OpenGL lines will be drawn dashed rather than solid.
    """

    DASHED_LINES = 1

    def draw_special(self, style):
        """Draws the batch with special OpenGL attributes.

        Args:
            style (int): The style with which to draw the batch.
        """
        glPushAttrib(GL_ENABLE_BIT)

        if style == self.DASHED_LINES:
            self._set_dashed_lines()

        self.draw()

        glPopAttrib()

    def _set_dashed_lines(self):
        """Sets OpenGL to draw dashed lines."""
        glLineStipple(1, 0x00FF)
        glEnable(GL_LINE_STIPPLE)
