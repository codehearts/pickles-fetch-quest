from ..tile import Tile
from ...geometry import Rectangle
from unittest.mock import Mock
import unittest


class TestTile(unittest.TestCase):
    """Test functionality of a Tile object.

    Each test case is provided the following properties::

        self.on_move: The listener mock for the tile's on_move event.
        self.game_object: A Tile at (1,2) with geometry states:

            {
                'default': Rectangle(x=1, y=2, width=3, height=4)
            }
    """

    def setUp(self):
        geometry_states = {
            'default': Rectangle(x=1, y=2, width=3, height=4)
        }

        self.on_move = Mock()
        self.tile = Tile(geometry_states, x=1, y=2)
        self.tile.add_listeners(on_move=self.on_move)

    def test_create_tile(self):
        """Creates a Tile and verifies its attributes."""
        geometry_states = {
            'default': Rectangle(x=1, y=2, width=3, height=4)
        }

        tile = Tile(geometry_states, x=5, y=6)
        self.assertEqual(5, tile.x)
        self.assertEqual(6, tile.y)
        self.assertEqual(3, tile.width)
        self.assertEqual(4, tile.height)
