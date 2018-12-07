import pyglet.graphics


class GraphicsBatch(pyglet.graphics.Batch):
    """Manages a set of objects to draw together for efficiency.

    A :obj:`engine.graphics.GraphicsBatch` object can be passed as a
    constructor argument to a :obj:`engine.graphics.GraphicsObject` to add that
    object to the batch.
    """
