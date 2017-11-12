from graphics_controller import GraphicsController, GraphicsObject
from disk_loader import DiskLoader
import pyglet.app

DiskLoader.set_resource_paths(['resources/'])

pickle_graphics = GraphicsController(160, 140, title="Pickle's Fetch Quest")

tile_image = DiskLoader.load_image('tiles/test.gif')
tile_graphic = GraphicsObject({'default': tile_image}, x=72, y=64)


@pickle_graphics._window.event
def on_draw():
    tile_graphic._sprite.draw()


if __name__ == "__main__":
    pyglet.app.run()
