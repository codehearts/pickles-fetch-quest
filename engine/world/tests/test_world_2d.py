from ..world_2d import World2d
from unittest.mock import call, Mock, patch
import unittest


class TestWorld2d(unittest.TestCase):
    """Test functionality of the ``World2d`` class."""

    module = 'engine.world.world_2d'
    resolve_game_object_collision_fn = module+'.resolve_game_object_collision'

    @patch(resolve_game_object_collision_fn)
    @patch('engine.world.world_2d.PositionalCollisionCache')
    def test_3_nonoverlapping_colliders(self, CacheMock, resolve_mock):
        """Resolving 3 non-overlapping colliders performs no resolution."""
        # 3|a..
        # 2|.b.
        # 1|..c
        #   ---
        #   123
        world = World2d()
        a = Mock(name='a', x=1, width=1, y=3, height=1)
        b = Mock(name='b', x=2, width=1, y=2, height=1)
        c = Mock(name='c', x=3, width=1, y=1, height=1)
        world.add_collider(a)
        world.add_collider(b)
        world.add_collider(c)

        world.update(1)

        resolve_mock.assert_not_called()
        CacheMock().add_collision.assert_not_called()

    @patch(resolve_game_object_collision_fn)
    @patch('engine.world.world_2d.PositionalCollisionCache')
    def test_3_stacked_overlapping_colliders(self, CacheMock, resolve_mock):
        """Resolving 3 stacked overlapping colliders resolves each pair."""
        # 1|aa 1|bb 1|cc
        #   --   --   --
        #   12   12   12
        world = World2d()
        a = Mock(name='a', x=1, width=2, y=1, height=1)
        b = Mock(name='b', x=1, width=2, y=1, height=1)
        c = Mock(name='c', x=1, width=2, y=1, height=1)
        world.add_collider(a)
        world.add_collider(b)
        world.add_collider(c)

        resolve_mock.return_value = (1, 2)
        world.update(1)

        self.assertEqual(3, resolve_mock.call_count)
        resolve_mock.assert_has_calls([
            call(a, b),
            call(a, c),
            call(b, c),
        ])

        self.assertEqual(3, CacheMock().add_collision.call_count)
        CacheMock().add_collision.assert_has_calls([
            call(a, b, resolve_mock.return_value),
            call(a, c, resolve_mock.return_value),
            call(b, c, resolve_mock.return_value),
        ])

    @patch(resolve_game_object_collision_fn)
    @patch('engine.world.world_2d.PositionalCollisionCache')
    def test_3_staggered_overlapping_colliders(self, CacheMock, resolve_mock):
        """Resolving staggered overlapping colliders resolves overlaps."""
        # 4|aa..
        # 3|a#b.
        # 2|.b#c
        # 1|..cc
        #   ----
        #   1234
        world = World2d()
        a = Mock(name='a', x=1, width=2, y=3, height=2)
        b = Mock(name='b', x=2, width=2, y=2, height=2)
        c = Mock(name='c', x=3, width=2, y=1, height=2)
        world.add_collider(a)
        world.add_collider(b)
        world.add_collider(c)

        resolve_mock.return_value = (1, 2)
        world.update(1)

        self.assertEqual(2, resolve_mock.call_count)
        resolve_mock.assert_has_calls([
            call(a, b),
            call(b, c),
        ])

        self.assertEqual(2, CacheMock().add_collision.call_count)
        CacheMock().add_collision.assert_has_calls([
            call(a, b, resolve_mock.return_value),
            call(b, c, resolve_mock.return_value),
        ])

    @patch('engine.world.world_2d.detect_overlap_2d')
    @patch('engine.world.world_2d.CollisionCache')
    def test_3_nonoverlapping_triggers(self, CacheMock, detect_mock):
        """Resolving 3 non-overlapping triggers performs no detection."""
        # 3|a..
        # 2|.b.
        # 1|..c
        #   ---
        #   123
        world = World2d()
        a = Mock(name='a', x=1, width=1, y=3, height=1)
        b = Mock(name='b', x=2, width=1, y=2, height=1)
        c = Mock(name='c', x=3, width=1, y=1, height=1)
        world.add_trigger(a)
        world.add_trigger(b)
        world.add_trigger(c)

        world.update(1)

        detect_mock.assert_not_called()
        CacheMock().add_collision.assert_not_called()

    @patch('engine.world.world_2d.detect_overlap_2d')
    @patch('engine.world.world_2d.CollisionCache')
    def test_3_stacked_overlapping_triggers(self, CacheMock, detect_mock):
        """Resolving 3 stacked overlapping triggers detects each pair."""
        # 1|aa 1|bb 1|cc
        #   --   --   --
        #   12   12   12
        world = World2d()
        a = Mock(name='a', x=1, width=2, y=1, height=1)
        b = Mock(name='b', x=1, width=2, y=1, height=1)
        c = Mock(name='c', x=1, width=2, y=1, height=1)
        world.add_trigger(a)
        world.add_trigger(b)
        world.add_trigger(c)

        detect_mock.return_value = True
        world.update(1)

        self.assertEqual(3, detect_mock.call_count)
        detect_mock.assert_has_calls([
            call(a, b),
            call(a, c),
            call(b, c),
        ])

        self.assertEqual(3, CacheMock().add_collision.call_count)
        CacheMock().add_collision.assert_has_calls([
            call(a, b),
            call(a, c),
            call(b, c)
        ])

    @patch('engine.world.world_2d.detect_overlap_2d')
    @patch('engine.world.world_2d.CollisionCache')
    def test_3_staggered_overlapping_triggers(self, CacheMock, detect_mock):
        """Resolving staggered overlapping triggers detects overlaps."""
        # 4|aa..
        # 3|a#b.
        # 2|.b#c
        # 1|..cc
        #   ----
        #   1234
        world = World2d()
        a = Mock(name='a', x=1, width=2, y=3, height=2)
        b = Mock(name='b', x=2, width=2, y=2, height=2)
        c = Mock(name='c', x=3, width=2, y=1, height=2)
        world.add_trigger(a)
        world.add_trigger(b)
        world.add_trigger(c)

        detect_mock.return_value = True
        world.update(1)

        self.assertEqual(2, detect_mock.call_count)
        detect_mock.assert_has_calls([
            call(a, b),
            call(b, c),
        ])

        self.assertEqual(2, CacheMock().add_collision.call_count)
        CacheMock().add_collision.assert_has_calls([call(a, b), call(b, c)])

    @patch(resolve_game_object_collision_fn)
    @patch('engine.world.world_2d.PositionalCollisionCache')
    @patch('engine.world.world_2d.detect_overlap_2d')
    @patch('engine.world.world_2d.CollisionCache')
    def test_collider_against_trigger_resolves_as_trigger(self, CacheMock,
                                                          detect_mock,
                                                          PositionalCacheMock,
                                                          resolve_mock):
        """Colliders are resolved as triggers against a trigger."""
        # 3|aa.
        # 2|a#b
        # 1|.b#
        #   ---
        #   123
        world = World2d()
        a = Mock(name='a', x=1, width=2, y=2, height=2)
        b = Mock(name='b', x=2, width=2, y=1, height=2)
        world.add_collider(a)
        world.add_trigger(b)

        world.update(1)

        resolve_mock.assert_not_called()
        PositionalCacheMock().add_collision.assert_not_called()

        detect_mock.assert_called_once_with(a, b)
        CacheMock().add_collision.assert_called_once_with(a, b)

    @patch(resolve_game_object_collision_fn)
    @patch('engine.world.world_2d.PositionalCollisionCache')
    @patch('engine.world.world_2d.detect_overlap_2d')
    @patch('engine.world.world_2d.CollisionCache')
    def test_trigger_against_collider_resolves_as_trigger(self, CacheMock,
                                                          detect_mock,
                                                          PositionalCacheMock,
                                                          resolve_mock):
        """Triggers are resolved as triggers against a collider."""
        # 3|aa.
        # 2|a#b
        # 1|.b#
        #   ---
        #   123
        world = World2d()
        a = Mock(name='a', x=1, width=2, y=2, height=2)
        b = Mock(name='b', x=2, width=2, y=1, height=2)
        world.add_trigger(a)
        world.add_collider(b)

        resolve_mock.return_value = (1, 2)
        world.update(1)

        resolve_mock.assert_not_called()
        PositionalCacheMock().add_collision.assert_not_called()

        detect_mock.assert_called_once_with(a, b)
        CacheMock().add_collision.assert_called_once_with(a, b)

    @patch(resolve_game_object_collision_fn)
    @patch('engine.world.world_2d.PositionalCollisionCache')
    def test_colliders_dispatch_event_on_enter(self, CacheMock, resolve_mock):
        """New collider collisions dispatch an event."""
        world = World2d()
        a = Mock(name='a', coordinates=(1, 3), x=1, width=2, y=3, height=2)
        b = Mock(name='b', coordinates=(2, 2), x=2, width=2, y=2, height=2)
        world.add_collider(a)
        world.add_collider(b)

        resolve_mock.return_value = (1, 1)
        CacheMock().get_new_collisions.return_value = {(a, b)}

        world.update(1)
        a.dispatch_event.assert_called_once_with('on_collider_enter', b)
        b.dispatch_event.assert_called_once_with('on_collider_enter', a)

    @patch(resolve_game_object_collision_fn)
    @patch('engine.world.world_2d.PositionalCollisionCache')
    def test_colliders_dispatch_event_on_exit(self, CacheMock, resolve_mock):
        """Removed collider collisions dispatch an event."""
        world = World2d()
        a = Mock(name='a', coordinates=(1, 3), x=1, width=2, y=3, height=2)
        b = Mock(name='b', coordinates=(2, 2), x=2, width=2, y=2, height=2)
        world.add_collider(a)
        world.add_collider(b)

        resolve_mock.return_value = (1, 1)
        CacheMock().get_removed_collisions.return_value = {(a, b)}

        world.update(1)
        a.dispatch_event.assert_called_once_with('on_collider_exit', b)
        b.dispatch_event.assert_called_once_with('on_collider_exit', a)

    @patch('engine.world.world_2d.detect_overlap_2d')
    @patch('engine.world.world_2d.CollisionCache')
    def test_triggers_dispatch_event_on_enter(self, CacheMock, detect_mock):
        """New trigger collisions dispatch an event."""
        world = World2d()
        a = Mock(name='a', coordinates=(1, 3), x=1, width=2, y=3, height=2)
        b = Mock(name='b', coordinates=(2, 2), x=2, width=2, y=2, height=2)
        world.add_trigger(a)
        world.add_trigger(b)

        detect_mock.return_value = True
        CacheMock().get_new_collisions.return_value = {(a, b)}

        world.update(1)
        a.dispatch_event.assert_called_once_with('on_trigger_enter', b)
        b.dispatch_event.assert_called_once_with('on_trigger_enter', a)

    @patch('engine.world.world_2d.detect_overlap_2d')
    @patch('engine.world.world_2d.CollisionCache')
    def test_triggers_dispatch_event_on_exit(self, CacheMock, detect_mock):
        """Removed trigger collisions dispatch an event."""
        world = World2d()
        a = Mock(name='a', coordinates=(1, 3), x=1, width=2, y=3, height=2)
        b = Mock(name='b', coordinates=(2, 2), x=2, width=2, y=2, height=2)
        world.add_trigger(a)
        world.add_trigger(b)

        detect_mock.return_value = True
        CacheMock().get_removed_collisions.return_value = {(a, b)}

        world.update(1)
        a.dispatch_event.assert_called_once_with('on_trigger_exit', b)
        b.dispatch_event.assert_called_once_with('on_trigger_exit', a)
