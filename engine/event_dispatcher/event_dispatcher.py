import pyglet.event


class EventDispatcher(pyglet.event.EventDispatcher):
    """Provides an interface for event driven logic.

    Any class which inherits from :cls:`EventDispatcher` provides an interface
    for other objects to be notified of object-specific events.

    If an event listener is attached for an event that has not been registered,
    a :cls:`EventException` will be raised.
    """

    def __init__(self):
        """Creates a new object which can dispatch events to its listeners."""
        super(EventDispatcher, self).__init__()

    def register_event(self, name):
        """Registers an event name with the dispatch system.

        Handlers will not be attached or discovered unless the event name
        is registered.

        Args:
            name (str): The name of the event to register.
        """
        EventDispatcher.register_event_type(name)

    def add_listeners(self, *args, **kwargs):
        """Registers callables to run when events are dispatched.

        Args:
            *args (list of callable): A list of callable objects to attach.
                The `__name__` attribute is used as the event name.
            **kwargs (dict of str: callable): A mapping of event names
                to callable objects to attach.
        """
        try:
            super(EventDispatcher, self).push_handlers(*args, **kwargs)
        except pyglet.event.EventException as e:
            raise EventException(*e.args)

    def dispatch_event(self, name, *args):
        """Runs all callable listeners for the dispatched event.

        This method should only be called by the class implementing
        :cls:`EventDispatcher`, it should not be called by the external
        application.

        Args:
            name (str): The name of the event to dispatch.
                All callables registered for this event with
                :fn:`add_listeners` will be called.
            *args: Arguments to pass to the event listeners.
        """
        super(EventDispatcher, self).dispatch_event(name, *args)


class EventException(Exception):
    """Raised when attaching an event listener to an unregistered event."""
    pass
