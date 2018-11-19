from pyglet import window


class KeyHandler(object):
    """Maps keypresses to an arbitrary number of callbacks."""

    def __init__(self, graphics_controller):
        """Creates a new key handler attached to a graphics controller.

        Args:
            graphics_controller (:obj:`GraphicsController`): The graphics
                controller owning the window to handle key events for.
        """
        super(KeyHandler, self).__init__()
        self._key_handler = window.key.KeyStateHandler()
        self._key_release_mappings = {}
        self._key_press_mappings = {}
        self._key_down_mappings = {}

        graphics_controller.add_key_handler(
            self._key_handler,
            on_press=lambda *args:
                self._handle_key_event(*args, self._key_press_mappings),
            on_release=lambda *args:
                self._handle_key_event(*args, self._key_release_mappings))

    def on_key_down(self, key, callback):
        """Registers a callback to call when the given key is held down.

        The callback will be called on each update as long as the key is
        held. The time delta in milliseconds will be the only argument.

        Args:
            key (int): The key which will trigger the callback.
            callback (fn): The callback for when the key is down.
        """
        self._key_down_mappings.setdefault(key, []).append(callback)

    def on_key_press(self, key, callback):
        """Registers a callback for when the given key is initially pressed.

        The callback is only called once when the key is initially pressed.
        No arguments are passed to the callback.

        Args:
            key (int): The key which will trigger the callback.
            callback (fn): The callback for when the key is pressed.
        """
        self._key_press_mappings.setdefault(key, []).append(callback)

    def on_key_release(self, key, callback):
        """Registers a callback for when the given key is initially released.

        The callback is only called once when the key is initially released.
        No arguments are passed to the callback.

        Args:
            key (int): The key which will trigger the callback.
            callback (fn): The callback for when the key is released.
        """
        self._key_release_mappings.setdefault(key, []).append(callback)

    def update(self, dt):
        """Updates the key handler, calling any callbacks as necessary.

        Args:
            dt (int): The elapsed time in milliseconds
        """
        for key, callbacks in self._key_down_mappings.items():
            if self._key_handler[key]:
                for callback in callbacks:
                    callback(dt)

    def _handle_key_event(self, key, modifiers, mapping):
        """Dispatches a key event to any registered listeners in the mapping.

        Args:
            key (int): The key for the event.
            modifiers (int): Any modifier keys for the event.
            mapping (dict of int to fn): A mapping of keys to their handlers.
        """
        if key in mapping:
            for callback in mapping[key]:
                callback()
