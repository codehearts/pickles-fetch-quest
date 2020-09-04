from ..positional_collision_cache import PositionalCollisionCache
from engine.geometry import Rectangle
import unittest


class TestPositionalCollisionCache(unittest.TestCase):
    """Test functionality of the ``PositionalCollisionCache`` class."""

    def setUp(self):
        """Creates a new :cls:`PositionalCollisionCache` as ``self.cache``."""
        self.cache = PositionalCollisionCache()

    def test_new_collisions_are_new_and_not_removed(self):
        """New collisions are considered new and not removed."""
        a = Rectangle(x=1, y=3, width=2, height=2)
        b = Rectangle(x=2, y=2, width=2, height=2)

        self.cache.add_collision(a, b, (1, 1))
        self.cache.update(1)

        self.assertFalse(self.cache.get_removed_collisions())

        new_collisions = self.cache.get_new_collisions()
        self.assertEqual(1, len(new_collisions))
        self.assertCountEqual((a, b), list(new_collisions)[0])

    def test_new_collisions_are_not_registered_twice(self):
        """New collisions are not registered twice between both objects."""
        a = Rectangle(x=1, y=3, width=2, height=2)
        b = Rectangle(x=2, y=2, width=2, height=2)

        self.cache.add_collision(a, b, (1, 1))
        self.cache.add_collision(b, a, (1, 1))
        self.cache.update(1)

        self.assertFalse(self.cache.get_removed_collisions())

        new_collisions = self.cache.get_new_collisions()
        self.assertEqual(1, len(new_collisions))
        self.assertCountEqual((a, b), list(new_collisions)[0])

    def test_repeated_collisions_are_not_new_or_removed(self):
        """Collisions are not new when the same collision occurs again."""
        a = Rectangle(x=1, y=3, width=2, height=2)
        b = Rectangle(x=2, y=2, width=2, height=2)

        self.cache.add_collision(a, b, (1, 1))
        self.cache.update(1)

        self.cache.add_collision(a, b, (1, 1))
        self.cache.update(1)

        self.assertFalse(self.cache.get_removed_collisions())
        self.assertFalse(self.cache.get_new_collisions())

    def test_collision_is_not_removed_without_velocity_x(self):
        """Collisions are not removed if movement occured without velocity."""
        a = Rectangle(x=1, y=3, width=2, height=2)
        b = Rectangle(x=2, y=2, width=2, height=2)

        self.cache.add_collision(a, b, (1, 1))
        self.cache.update(1)

        # Object moved to no longer collide on the x axis
        a.x = 3

        self.cache.add_collision(a, b, (0, 1))  # No x velocity
        self.cache.update(1)

        self.assertFalse(self.cache.get_removed_collisions())
        self.assertFalse(self.cache.get_new_collisions())

    def test_collision_is_not_removed_without_velocity_y(self):
        """Collisions are not removed if movement occured without velocity."""
        a = Rectangle(x=1, y=3, width=2, height=2)
        b = Rectangle(x=2, y=2, width=2, height=2)

        self.cache.add_collision(a, b, (1, 1))
        self.cache.update(1)

        # Object moved to no longer collide on the y axis
        a.y = 2

        self.cache.add_collision(a, b, (1, 0))  # No y velocity
        self.cache.update(1)

        self.assertFalse(self.cache.get_removed_collisions())
        self.assertFalse(self.cache.get_new_collisions())

    def test_collision_is_removed_after_noncolliding_movement(self):
        """Collisions are removed after objects move outside the collision."""
        a = Rectangle(x=1, y=3, width=2, height=2)
        b = Rectangle(x=2, y=2, width=2, height=2)

        self.cache.add_collision(a, b, (1, 1))
        self.cache.update(1)

        # Object is moved to no longer collide
        a.coordinates.set((4, 4))

        self.cache.add_collision(a, b, (0, 0))  # No resolution was necessary
        self.cache.update(1)

        self.assertFalse(self.cache.get_new_collisions())

        removed_collisions = self.cache.get_removed_collisions()
        self.assertEqual(1, len(removed_collisions))
        self.assertCountEqual((a, b), list(removed_collisions)[0])

    def test_removed_collisions_are_not_registered_twice(self):
        """Removed collisions are not registered twice between both objects."""
        a = Rectangle(x=1, y=3, width=2, height=2)
        b = Rectangle(x=2, y=2, width=2, height=2)

        self.cache.add_collision(a, b, (1, 1))
        self.cache.update(1)

        # Object is moved to no longer collide
        a.coordinates.set((4, 4))

        self.cache.add_collision(a, b, (0, 0))  # No resolution was necessary
        self.cache.add_collision(b, a, (0, 0))
        self.cache.update(1)

        self.assertFalse(self.cache.get_new_collisions())

        removed_collisions = self.cache.get_removed_collisions()
        self.assertEqual(1, len(removed_collisions))
        self.assertCountEqual((a, b), list(removed_collisions)[0])

    def test_repeated_collisions_are_new_after_removal(self):
        """A collision is considered new after its removal."""
        a = Rectangle(x=1, y=3, width=2, height=2)
        b = Rectangle(x=2, y=2, width=2, height=2)

        self.cache.add_collision(a, b, (1, 1))
        self.cache.update(1)

        # Object is moved to no longer collide
        a.coordinates.set((4, 4))

        self.cache.add_collision(a, b, (0, 0))  # No resolution was necessary
        self.cache.update(1)

        # Object is moved to collide again
        a.coordinates.set((1, 3))

        self.cache.add_collision(a, b, (1, 1))
        self.cache.update(1)

        self.assertFalse(self.cache.get_removed_collisions())

        new_collisions = self.cache.get_new_collisions()
        self.assertEqual(1, len(new_collisions))
        self.assertCountEqual((a, b), list(new_collisions)[0])
