from engine.graphics import CrossBox, GraphicsBatch
from .world_object import TRIGGER


class World2dDebug(object):
    """Debug properties for a :obj:`world_2d.World2d` instance."""

    def __init__(self, world, collider_color=(0, 255, 128),
                 trigger_color=(0, 255, 255)):
        """Creates a new visual debugger for a :obj:`world_2d.World2d`.

        Args:
            world (list of :obj:`world_2d.World2d`):
                The world to render debug shapes for.

        Kwargs:
            collider_color (tuple of 3 int):
                RGB color tuple to draw colliders with. Default is green.
            trigger_color (tuple of 3 int):
                RGB color tuple to draw triggers with. Default is cyan.
        """
        super(World2dDebug, self).__init__()
        self._collider_batch = GraphicsBatch()
        self._collider_color = collider_color

        self._trigger_batch = GraphicsBatch()
        self._trigger_color = trigger_color

        self._debug_objects = {}

        # Create debug shapes for all objects in the world
        for obj in world._objects:
            if obj.type == TRIGGER:
                self._add_trigger(obj.object)
            else:
                self._add_collider(obj.object)

        # Update our debug shapes when the world is updated
        world.add_listeners(on_update_exit=self._update)

        # Create debug shapes for colliders and triggers as they're added
        world.add_listeners(on_collider_add=self._add_collider)
        world.add_listeners(on_trigger_add=self._add_trigger)

    def draw(self):
        """Draws a solid cross box for colliders and dashed for triggers."""
        self._collider_batch.draw()
        self._trigger_batch.draw_special(GraphicsBatch.DASHED_LINES)

    def _update(self, world):
        """Update debug shapes to match their corresponding world objects."""
        for obj, debug_shape in self._debug_objects.items():
            debug_shape.set_position(obj.coordinates)

    def _add_collider(self, collider):
        """Adds a collider to this debug instance."""
        self._add_object(collider, self._collider_color, self._collider_batch)

    def _add_trigger(self, trigger):
        """Adds a trigger to this debug instance."""
        self._add_object(trigger, self._trigger_color, self._trigger_batch)

    def _add_object(self, obj, color, batch):
        """Adds an object to this debug instance."""
        self._debug_objects[obj] = CrossBox(obj, color, batch)
