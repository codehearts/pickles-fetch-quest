from ..generic_factory import GenericFactory
import unittest


class TestGenericFactory(unittest.TestCase):
    """Test generic factory recipes."""

    def test_can_not_create_objects_without_recipe(self):
        """Objects can't be created if a recipe is not specified."""
        factory = GenericFactory()

        self.assertFalse(factory.can_create('nonexistent'))

    def test_can_create_objects_with_recipe(self):
        """Objects can be created if a recipe is exists for them."""
        factory = GenericFactory()
        factory.add_recipe('my_recipe', lambda x: x*x)

        self.assertTrue(factory.can_create('my_recipe'))

    def test_returns_none_when_creating_unknown_recipe(self):
        """Creating from an unknown recipe returns None."""
        factory = GenericFactory()

        self.assertIsNone(factory.create('nonexistent'))

    def test_creates_objects_from_appropriate_recipes(self):
        """The correct recipe is used to create an object."""
        factory = GenericFactory()
        factory.add_recipe('square', lambda x: x*x)
        factory.add_recipe('double', lambda x: x*2)

        self.assertEqual(16, factory.create('square', 4))
        self.assertEqual(8, factory.create('double', 4))
