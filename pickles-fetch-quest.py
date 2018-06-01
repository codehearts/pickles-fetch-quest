from engine import CollisionResolver2d, DiskLoader, GraphicsController
from engine import GraphicsObject, Physics2d, Rectangle, RESOLVE_COLLISIONS
from engine import Tile
import pyglet.app

DiskLoader.set_resource_paths(['resources/'])

pickle_graphics = GraphicsController(160, 140, title="Pickle's Fetch Quest")
collision_resolver = CollisionResolver2d()

collision_sound = DiskLoader.load_audio(
    'audio/sfx/bass-drum-hit.wav', streaming=False)

tile_image = DiskLoader.load_image('tiles/test.gif')

tile_geometry_states = {
    'default': Rectangle(x=0, y=0, width=16, height=16)
}
graphics = []


def create_tile(x, y):
    tile = Tile(tile_geometry_states, x=x, y=y)
    tile_graphic = GraphicsObject({'default': tile_image}, x=tile.x, y=tile.y)

    tile.add_listeners(on_move=tile_graphic.set_position)
    collision_resolver.register(tile, RESOLVE_COLLISIONS)

    graphics.append(tile_graphic)
    return tile, tile_graphic


def create_physics_tile(x, y, *args, **kwargs):
    physics = Physics2d(*args, **kwargs)
    tile = Tile(tile_geometry_states, x=x, y=y, physics=physics)
    tile_graphic = GraphicsObject({'default': tile_image}, x=tile.x, y=tile.y)

    tile.add_listeners(on_move=tile_graphic.set_position)
    pickle_graphics.add_listeners(on_update=tile.update)
    collision_resolver.register(tile, RESOLVE_COLLISIONS)

    graphics.append(tile_graphic)
    return tile, tile_graphic


pickle_graphics.add_listeners(on_update=lambda x: collision_resolver.resolve())

bottom_1, bottom_1_graphic = create_physics_tile(72-160, 46, gravity=(10, 0))
bottom_2, bottom_2_graphic = create_physics_tile(72, 62-80, gravity=(0, 10))
bottom_3, bottom_3_graphic = create_physics_tile(88, 62-144, gravity=(0, 10))

middle_1, middle_1_graphic = create_physics_tile(72-96, 62, gravity=(10, 0))
middle_2, middle_2_graphic = create_tile(72, 62)
middle_3, middle_3_graphic = create_physics_tile(72+64, 62, gravity=(-10, 0))

top_1, top_1_graphic = create_physics_tile(72-176, 78, gravity=(10, 0))
top_2, top_2_graphic = create_physics_tile(72, 62+112, gravity=(0, -10))
top_3, top_3_graphic = create_physics_tile(72+128, 78, gravity=(-10, 0))


@pickle_graphics._window.event
def on_draw():
    pickle_graphics._window.clear()
    for graphic in graphics:
        graphic._sprite.draw()


if __name__ == "__main__":
    pyglet.app.run()
