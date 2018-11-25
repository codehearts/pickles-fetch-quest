class GenericFactory(object):
    """Extensible factory for converting strings into arbitrary objects."""

    def __init__(self):
        super(GenericFactory, self).__init__()
        self._recipes = {}

    def add_recipe(self, name, factory_method):
        """Creates a named recipe for creating an object.

        Args:
            name (str): The name of the recipe.
            factory_method (fn): A method returning the object for the recipe.
                This method can take any arguments.
        """
        self._recipes[name] = factory_method

    def create(self, name, *args, **kwargs):
        """Creates an object from the given recipe name.

        Args:
            name (str): The name of the recipe to create an object from.

        Returns:
            An object create from the given recipe name.
        """
        if self.can_create(name):
            return self._recipes[name](*args, **kwargs)

        return None

    def can_create(self, name):
        """Returns true if this factory can an object for the given name."""
        return name in self._recipes
