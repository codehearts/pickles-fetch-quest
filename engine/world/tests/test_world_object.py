from ..world_object import WorldObject, COLLIDER, TRIGGER
from unittest.mock import Mock
import unittest


class TestWorldObject(unittest.TestCase):
    """Test functionality of the ``WorldObject`` class."""

    def test_register_collider(self):
        """Registering a collider creates a new object."""
        geometry = Mock()
        entry = WorldObject(geometry, COLLIDER)

        self.assertEqual(geometry, entry.object)
        self.assertEqual(COLLIDER, entry.type)

    def test_register_trigger(self):
        """Registering a trigger creates a new object."""
        geometry = Mock()
        entry = WorldObject(geometry, TRIGGER)

        self.assertEqual(geometry, entry.object)
        self.assertEqual(TRIGGER, entry.type)

    def test_register_invalid_method_raises_an_exception(self):
        """Registering for invalid type raises ValueError."""
        with self.assertRaises(ValueError):
            WorldObject(Mock(), 999)
