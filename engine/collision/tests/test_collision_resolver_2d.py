from ..collision_resolver_entry import DETECT_COLLISIONS, RESOLVE_COLLISIONS
from ..collision_resolver_2d import CollisionResolver2d
from unittest.mock import call, Mock, patch
import unittest


class TestCollisionResolver2d(unittest.TestCase):
    """Test functionality of the ``CollisionResolver2d`` class."""

    module = 'engine.collision.collision_resolver_2d'
    resolve_game_object_collision_fn = module+'.resolve_game_object_collision'

    def setUp(self):
        """Creates a new :cls:`CollisionResolver2d` as ``self.resolver``."""
        self.resolver = CollisionResolver2d(0)

    @patch(resolve_game_object_collision_fn)
    def test_resolve_3_nonoverlapping_shapes(self, resolve_mock):
        """Resolving 3 non-overlapping shapes performs no resolution."""
        # 3|a..
        # 2|.b.
        # 1|..c
        #   ---
        #   123
        a = Mock(name='a', x=1, width=1, y=3, height=1)
        b = Mock(name='b', x=2, width=1, y=2, height=1)
        c = Mock(name='c', x=3, width=1, y=1, height=1)
        self.resolver.register(a, RESOLVE_COLLISIONS)
        self.resolver.register(b, RESOLVE_COLLISIONS)
        self.resolver.register(c, RESOLVE_COLLISIONS)

        resolve_mock.return_value = (0, 0)
        self.resolver.resolve()

        resolve_mock.assert_not_called()
        a.notify_collision_with.assert_not_called()
        b.notify_collision_with.assert_not_called()
        c.notify_collision_with.assert_not_called()

    @patch(resolve_game_object_collision_fn)
    def test_resolve_3_stacked_overlapping_shapes(self, resolve_mock):
        """Resolving 3 stacked overlapping shapes resolves each pair."""
        # 1|aa 1|bb 1|cc
        #   --   --   --
        #   12   12   12
        a = Mock(name='a', x=1, width=2, y=1, height=1)
        b = Mock(name='b', x=1, width=2, y=1, height=1)
        c = Mock(name='c', x=1, width=2, y=1, height=1)
        self.resolver.register(a, RESOLVE_COLLISIONS)
        self.resolver.register(b, RESOLVE_COLLISIONS)
        self.resolver.register(c, RESOLVE_COLLISIONS)

        resolve_mock.return_value = (1, 2)
        self.resolver.resolve()

        self.assertEqual(3, resolve_mock.call_count)
        resolve_mock.assert_has_calls([
            call(a, b),
            call(a, c),
            call(b, c),
        ])
        a.notify_collision_with.assert_has_calls([call(b), call(c)])
        b.notify_collision_with.assert_has_calls([call(a), call(c)])
        c.notify_collision_with.assert_has_calls([call(a), call(b)])

    @patch(resolve_game_object_collision_fn)
    def test_resolve_3_staggered_nonoverlapping_shapes(self, resolve_mock):
        """Resolving staggered non-overlapping shapes resolves overlaps."""
        # 4|aa..
        # 3|a#b.
        # 2|.b#c
        # 1|..cc
        #   ----
        #   1234
        a = Mock(name='a', x=1, width=2, y=3, height=2)
        b = Mock(name='b', x=2, width=2, y=2, height=2)
        c = Mock(name='c', x=3, width=2, y=1, height=2)
        self.resolver.register(a, RESOLVE_COLLISIONS)
        self.resolver.register(b, RESOLVE_COLLISIONS)
        self.resolver.register(c, RESOLVE_COLLISIONS)

        resolve_mock.return_value = (1, 2)
        self.resolver.resolve()

        self.assertEqual(2, resolve_mock.call_count)
        resolve_mock.assert_has_calls([
            call(a, b),
            call(b, c),
        ])
        a.notify_collision_with.assert_has_calls([call(b)])
        b.notify_collision_with.assert_has_calls([call(a), call(c)])
        c.notify_collision_with.assert_has_calls([call(b)])

    @patch(resolve_game_object_collision_fn)
    def test_detect_3_nonoverlapping_shapes(self, resolve_mock):
        """Detecting 3 non-overlapping shapes performs no resolution."""
        # 3|a..
        # 2|.b.
        # 1|..c
        #   ---
        #   123
        a = Mock(name='a', x=1, width=1, y=3, height=1)
        b = Mock(name='b', x=2, width=1, y=2, height=1)
        c = Mock(name='c', x=3, width=1, y=1, height=1)
        self.resolver.register(a, DETECT_COLLISIONS)
        self.resolver.register(b, DETECT_COLLISIONS)
        self.resolver.register(c, DETECT_COLLISIONS)

        resolve_mock.return_value = (1, 2)
        self.resolver.resolve()

        resolve_mock.assert_not_called()
        a.notify_collision_with.assert_not_called()
        b.notify_collision_with.assert_not_called()
        c.notify_collision_with.assert_not_called()

    @patch(resolve_game_object_collision_fn)
    def test_detect_3_stacked_overlapping_shapes(self, resolve_mock):
        """Detecting 3 stacked overlapping shapes notifies each pair."""
        # 1|aa 1|bb 1|cc
        #   --   --   --
        #   12   12   12
        a = Mock(name='a', x=1, width=2, y=1, height=1)
        b = Mock(name='b', x=1, width=2, y=1, height=1)
        c = Mock(name='c', x=1, width=2, y=1, height=1)
        self.resolver.register(a, DETECT_COLLISIONS)
        self.resolver.register(b, DETECT_COLLISIONS)
        self.resolver.register(c, DETECT_COLLISIONS)

        resolve_mock.return_value = (1, 2)
        self.resolver.resolve()

        resolve_mock.assert_not_called()
        a.notify_collision_with.assert_has_calls([call(b), call(c)])
        b.notify_collision_with.assert_has_calls([call(a), call(c)])
        c.notify_collision_with.assert_has_calls([call(a), call(b)])

    @patch(resolve_game_object_collision_fn)
    def test_detect_3_staggered_nonoverlapping_shapes(self, resolve_mock):
        """Detecting staggered non-overlapping shapes notifies of overlaps."""
        # 4|aa..
        # 3|a#b.
        # 2|.b#c
        # 1|..cc
        #   ----
        #   1234
        a = Mock(name='a', x=1, width=2, y=3, height=2)
        b = Mock(name='b', x=2, width=2, y=2, height=2)
        c = Mock(name='c', x=3, width=2, y=1, height=2)
        self.resolver.register(a, DETECT_COLLISIONS)
        self.resolver.register(b, DETECT_COLLISIONS)
        self.resolver.register(c, DETECT_COLLISIONS)

        resolve_mock.return_value = (1, 2)
        self.resolver.resolve()

        resolve_mock.assert_not_called()
        a.notify_collision_with.assert_has_calls([call(b)])
        b.notify_collision_with.assert_has_calls([call(a), call(c)])
        c.notify_collision_with.assert_has_calls([call(b)])

    @patch(resolve_game_object_collision_fn)
    def test_first_uses_resolution_second_uses_detection(self, resolve_mock):
        """No resolution occurs when either object uses detection."""
        # 3|aa.
        # 2|a#b
        # 1|.b#
        #   ---
        #   123
        a = Mock(name='a', x=1, width=2, y=2, height=2)
        b = Mock(name='b', x=2, width=2, y=1, height=2)
        self.resolver.register(a, RESOLVE_COLLISIONS)
        self.resolver.register(b, DETECT_COLLISIONS)

        resolve_mock.return_value = (1, 2)
        self.resolver.resolve()

        resolve_mock.assert_not_called()
        a.notify_collision_with.assert_has_calls([call(b)])
        b.notify_collision_with.assert_has_calls([call(a)])

    @patch(resolve_game_object_collision_fn)
    def test_first_uses_detection_second_uses_resolution(self, resolve_mock):
        """No resolution occurs when either object uses detection."""
        # 3|aa.
        # 2|a#b
        # 1|.b#
        #   ---
        #   123
        a = Mock(name='a', x=1, width=2, y=2, height=2)
        b = Mock(name='b', x=2, width=2, y=1, height=2)
        self.resolver.register(a, DETECT_COLLISIONS)
        self.resolver.register(b, RESOLVE_COLLISIONS)

        resolve_mock.return_value = (1, 2)
        self.resolver.resolve()

        resolve_mock.assert_not_called()
        a.notify_collision_with.assert_has_calls([call(b)])
        b.notify_collision_with.assert_has_calls([call(a)])

    @patch(resolve_game_object_collision_fn)
    def test_does_not_notify_when_threshold_is_not_crossed(self, resolve_mock):
        """No notifications when the movement threshold was not crossed."""
        self.resolver = CollisionResolver2d(2)  # Movement threshold of 2

        a = Mock(name='a', x=1, width=2, y=3, height=2)
        b = Mock(name='b', x=2, width=2, y=2, height=2)
        c = Mock(name='c', x=3, width=2, y=1, height=2)
        self.resolver.register(a, RESOLVE_COLLISIONS)
        self.resolver.register(b, RESOLVE_COLLISIONS)
        self.resolver.register(c, RESOLVE_COLLISIONS)

        # Neither axis has enough movement
        resolve_mock.return_value = (1, 1)

        self.resolver.resolve()
        a.notify_collision_with.assert_not_called()
        b.notify_collision_with.assert_not_called()
        c.notify_collision_with.assert_not_called()

    @patch(resolve_game_object_collision_fn)
    def test_notifies_when_x_threshold_is_crossed(self, resolve_mock):
        """Notifies when the movement threshold was crossed on the x axis."""
        self.resolver = CollisionResolver2d(2)  # Movement threshold of 2

        a = Mock(name='a', x=1, width=2, y=3, height=2)
        b = Mock(name='b', x=2, width=2, y=2, height=2)
        c = Mock(name='c', x=3, width=2, y=1, height=2)
        self.resolver.register(a, RESOLVE_COLLISIONS)
        self.resolver.register(b, RESOLVE_COLLISIONS)
        self.resolver.register(c, RESOLVE_COLLISIONS)

        # X axis has enough movement
        resolve_mock.return_value = (2, 1)

        self.resolver.resolve()
        a.notify_collision_with.assert_has_calls([call(b)])
        b.notify_collision_with.assert_has_calls([call(a), call(c)])
        c.notify_collision_with.assert_has_calls([call(b)])

    @patch(resolve_game_object_collision_fn)
    def test_notifies_when_y_threshold_is_crossed(self, resolve_mock):
        """Notifies when the movement threshold was crossed on the y axis."""
        self.resolver = CollisionResolver2d(2)  # Movement threshold of 2

        a = Mock(name='a', x=1, width=2, y=3, height=2)
        b = Mock(name='b', x=2, width=2, y=2, height=2)
        c = Mock(name='c', x=3, width=2, y=1, height=2)
        self.resolver.register(a, RESOLVE_COLLISIONS)
        self.resolver.register(b, RESOLVE_COLLISIONS)
        self.resolver.register(c, RESOLVE_COLLISIONS)

        # Y axis has enough movement
        resolve_mock.return_value = (1, 2)

        self.resolver.resolve()
        a.notify_collision_with.assert_has_calls([call(b)])
        b.notify_collision_with.assert_has_calls([call(a), call(c)])
        c.notify_collision_with.assert_has_calls([call(b)])
