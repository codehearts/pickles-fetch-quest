from ..collision_cache import CollisionCache
from engine.geometry import Rectangle
import unittest


class TestCollisionCache(unittest.TestCase):
    """Test functionality of the ``CollisionCache`` class."""

    def setUp(self):
        """Creates a new :cls:`CollisionCache` as ``self.cache``."""
        self.cache = CollisionCache()

    def test_new_collisions_are_new_and_not_removed(self):
        """New collisions are considered new and not removed."""
        a = Rectangle(x=1, y=3, width=2, height=2)
        b = Rectangle(x=2, y=2, width=2, height=2)

        self.cache.add_collision(a, b)
        self.cache.update(1)

        self.assertFalse(self.cache.get_removed_collisions())

        new_collisions = self.cache.get_new_collisions()
        self.assertEqual(1, len(new_collisions))
        self.assertCountEqual((a, b), list(new_collisions)[0])

    def test_new_collisions_are_not_registered_twice(self):
        """New collisions are not registered twice between both objects."""
        a = Rectangle(x=1, y=3, width=2, height=2)
        b = Rectangle(x=2, y=2, width=2, height=2)

        self.cache.add_collision(a, b)
        self.cache.add_collision(b, a)
        self.cache.update(1)

        self.assertFalse(self.cache.get_removed_collisions())

        new_collisions = self.cache.get_new_collisions()
        self.assertEqual(1, len(new_collisions))
        self.assertCountEqual((a, b), list(new_collisions)[0])

    def test_repeated_collisions_are_not_new_or_removed(self):
        """Collisions are not new when the same collision occurs again."""
        a = Rectangle(x=1, y=3, width=2, height=2)
        b = Rectangle(x=2, y=2, width=2, height=2)

        self.cache.add_collision(a, b)
        self.cache.update(1)

        self.cache.add_collision(a, b)
        self.cache.update(1)

        self.assertFalse(self.cache.get_removed_collisions())
        self.assertFalse(self.cache.get_new_collisions())

    def test_collision_is_removed_when_no_longer_colliding(self):
        """Collisions are removed if the collision wasn't added again."""
        a = Rectangle(x=1, y=3, width=2, height=2)
        b = Rectangle(x=2, y=2, width=2, height=2)

        self.cache.add_collision(a, b)
        self.cache.update(1)

        # The collision is not added because the objects no longer collide
        self.cache.update(1)

        self.assertFalse(self.cache.get_new_collisions())

        removed_collisions = self.cache.get_removed_collisions()
        self.assertEqual(1, len(removed_collisions))
        self.assertCountEqual((a, b), list(removed_collisions)[0])

    def test_repeated_collisions_are_new_after_removal(self):
        """A collision is considered new after its removal."""
        a = Rectangle(x=1, y=3, width=2, height=2)
        b = Rectangle(x=2, y=2, width=2, height=2)

        self.cache.add_collision(a, b)
        self.cache.update(1)

        # No collision added because they no longer collide
        self.cache.update(1)

        self.cache.add_collision(a, b)
        self.cache.update(1)

        self.assertFalse(self.cache.get_removed_collisions())

        new_collisions = self.cache.get_new_collisions()
        self.assertEqual(1, len(new_collisions))
        self.assertCountEqual((a, b), list(new_collisions)[0])

    def test_new_collisions_involving_same_object_are_handled(self):
        """New collisions involving the same object are handled."""
        a = Rectangle(x=1, y=3, width=2, height=2)
        b = Rectangle(x=2, y=2, width=2, height=2)
        c = Rectangle(x=3, y=1, width=2, height=2)

        self.cache.add_collision(a, b)
        self.cache.update(1)

        # New collision between a and b occurred
        self.assertFalse(self.cache.get_removed_collisions())

        new_collisions = self.cache.get_new_collisions()
        self.assertEqual(1, len(new_collisions))
        self.assertCountEqual((a, b), list(new_collisions)[0])

        self.cache.add_collision(a, b)
        self.cache.add_collision(b, c)
        self.cache.update(1)

        # New collision between b and c occurred
        self.assertFalse(self.cache.get_removed_collisions())

        new_collisions = self.cache.get_new_collisions()
        self.assertEqual(1, len(new_collisions))
        self.assertCountEqual((b, c), list(new_collisions)[0])

    def test_removed_collisions_involving_same_object_are_handled(self):
        """Removed collisions involving the same object are handled."""
        a = Rectangle(x=1, y=3, width=2, height=2)
        b = Rectangle(x=2, y=2, width=2, height=2)
        c = Rectangle(x=3, y=1, width=2, height=2)

        self.cache.add_collision(a, b)
        self.cache.update(1)

        self.cache.add_collision(a, b)
        self.cache.add_collision(b, c)
        self.cache.update(1)

        # Collision between a and b did not reoccur
        self.cache.add_collision(b, c)
        self.cache.update(1)

        # Collision between a and b was removed
        removed_collisions = self.cache.get_removed_collisions()
        self.assertEqual(1, len(removed_collisions))
        self.assertCountEqual((a, b), list(removed_collisions)[0])

        # No new collision between a and b was erroneously added
        new_collisions = self.cache.get_new_collisions()
        self.assertNotIn((a, b), new_collisions)
        self.assertNotIn((b, a), new_collisions)

        # Collision between b and c did not reoccur
        self.cache.update(1)

        # Collision between b and c was removed
        self.assertFalse(self.cache.get_new_collisions())

        removed_collisions = self.cache.get_removed_collisions()
        self.assertEqual(1, len(removed_collisions))
        self.assertCountEqual((b, c), list(removed_collisions)[0])
