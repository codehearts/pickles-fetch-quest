from ..event_dispatcher import EventDispatcher
import pyglet.clock
import pyglet.window


class GraphicsController(EventDispatcher):
    """Controller for graphical output to a desktop window.

    Events:
        on_update: Fires periodically with the number of milliseconds since the
            last update.
    """

    def __init__(self, width, height, title=None, resizable=False,
                 update_rate=120):
        """Creates a blank desktop window.

        Args:
            width (int): The width of the window.
            height (int): The height of the window.
            title (:obj:`str`, optional): Text to display in title bar.
                Defaults to None.
            resizeable (bool, optional): Allows the user to resize the window.
                Defaults to False.
            update_rate (int, optional): Number of times to fire the
                `on_update` event per second. Note that this is independent
                from the frame rate. Defaults to 120.
        """
        super(GraphicsController, self).__init__()
        self.register_event_type('on_update')

        self._window = pyglet.window.Window(
                width=width,
                height=height,
                caption=title,
                resizable=resizable)

        pyglet.clock.schedule_interval(self._dispatch_update, 1.0/update_rate)

    def _dispatch_update(self, seconds):
        """Dispatches the `on_update` event with the time delta in ms.

        Args:
            seconds (float): The number of seconds elapsed since last update.
        """
        self.dispatch_event('on_update', int(seconds * 1000))
