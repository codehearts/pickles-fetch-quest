from ..tile import Tile
from unittest.mock import Mock
import unittest


class TestTile(unittest.TestCase):
    """Test functionality of a Tile object."""

    def setUp(self):
        self.event_handler = Mock()
        self.rect = Tile(1, 2, 3, 4, self.event_handler)

    def test_create_collidable_object(self):
        """Creates a Tile and verifies its attributes."""
        self.assertEqual(1, self.rect.x)
        self.assertEqual(2, self.rect.y)
        self.assertEqual(3, self.rect.width)
        self.assertEqual(4, self.rect.height)
        self.assertEqual((1, 2), self.rect.position)
