from engine import event_dispatcher
import pyglet.clock
import pyglet.window


class GraphicsController(event_dispatcher.EventDispatcher):
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
            title (str, optional): Text to display in title bar.
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

    def add_key_handler(self, key_handler, on_press, on_release):
        """Adds a key handler to the window owned by the controller.

        Args:
            key_handler (:obj:`pyglet.window.key.KeyStateHandler`): The key
                handler to receive key events from this controller's window.
            on_press (fn): Callback for when a key is initially pressed.
                Receives the pressed key and any modifies as ints.
            on_release (fn): Callback for when a key is initially released.
                Receives the pressed key and any modifies as ints.
        """
        self._window.push_handlers(key_handler)
        self._window.push_handlers(
            on_key_press=on_press, on_key_release=on_release)
