from ..collision_resolver_entry import CollisionResolverEntry
from ..collision_resolver_entry import DETECT_COLLISIONS, RESOLVE_COLLISIONS
from unittest.mock import Mock
import unittest


class TestCollisionResolverEntry(unittest.TestCase):
    """Test functionality of the ``CollisionResolverEntry`` class."""

    def test_register_for_detection(self):
        """Registering for detection creates a new object."""
        geometry = Mock()
        entry = CollisionResolverEntry(geometry, DETECT_COLLISIONS)

        self.assertEqual(geometry, entry.geometry)
        self.assertEqual(DETECT_COLLISIONS, entry.method)

    def test_register_for_resolution(self):
        """Registering for resolution creates a new object."""
        geometry = Mock()
        entry = CollisionResolverEntry(geometry, RESOLVE_COLLISIONS)

        self.assertEqual(geometry, entry.geometry)
        self.assertEqual(RESOLVE_COLLISIONS, entry.method)

    def test_register_for_invalid_method(self):
        """Registering for invalid method raises ValueError."""
        with self.assertRaises(ValueError):
            CollisionResolverEntry(Mock(), 999)
