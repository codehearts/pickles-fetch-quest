from engine import DiskLoader, GraphicsController, GraphicsObject, Rectangle
from engine import Tile
import pyglet.app

DiskLoader.set_resource_paths(['resources/'])

pickle_graphics = GraphicsController(160, 140, title="Pickle's Fetch Quest")

tile_geometry_states = {
    'default': Rectangle(x=0, y=0, width=16, height=16)
}
tile = Tile(tile_geometry_states, x=0, y=0)

tile_image = DiskLoader.load_image('tiles/test.gif')
tile_graphic = GraphicsObject({'default': tile_image}, x=tile.x, y=tile.y)

tile.add_listeners(on_move=tile_graphic.set_position)
tile.set_position((72, 64))


@pickle_graphics._window.event
def on_draw():
    tile_graphic._sprite.draw()


if __name__ == "__main__":
    pyglet.app.run()
