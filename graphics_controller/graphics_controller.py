import pyglet.window


class GraphicsController(object):
    def __init__(self, width, height, title=None, resizable=False):
        """Opens a desktop window and provides an interface to render graphics.

        Args:
            width (int): The width of the window.
            height (int): The height of the window.
            title (:obj:`str`, optional): Text to display in title bar.
                Defaults to None.
            resizeable (bool, optional): Allows the user to resize the window.
                Defaults to False.
        """
        super(GraphicsController, self).__init__()
        self._window = pyglet.window.Window(
                width=width,
                height=height,
                caption=title,
                resizable=resizable)
