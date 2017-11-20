from engine import DiskLoader, GraphicsController, GraphicsObject, Physics2d
from engine import Rectangle, Tile
import pyglet.app

DiskLoader.set_resource_paths(['resources/'])

pickle_graphics = GraphicsController(160, 140, title="Pickle's Fetch Quest")

tile_image = DiskLoader.load_image('tiles/test.gif')

tile_geometry_states = {
    'default': Rectangle(x=0, y=0, width=16, height=16)
}

tile = Tile(tile_geometry_states, x=0, y=0)
tile_graphic = GraphicsObject({'default': tile_image}, x=tile.x, y=tile.y)
tile.add_listeners(on_move=tile_graphic.set_position)
tile.set_position((72, 0))

physics = Physics2d()
physics_tile = Tile(tile_geometry_states, x=72, y=128, physics=physics)
physics_graphic = GraphicsObject({'default': tile_image},
                                 x=physics_tile.x, y=physics_tile.y)
physics_tile.add_listeners(on_move=physics_graphic.set_position)
pickle_graphics.add_listeners(on_update=physics_tile.update)


@pickle_graphics._window.event
def on_draw():
    pickle_graphics._window.clear()
    tile_graphic._sprite.draw()
    physics_graphic._sprite.draw()

if __name__ == "__main__":
    pyglet.app.run()
