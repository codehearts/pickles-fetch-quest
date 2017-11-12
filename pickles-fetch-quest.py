from graphics_controller import GraphicsController
from disk_loader import DiskLoader
import pyglet.app

DiskLoader.set_resource_paths(['resources/'])

pickle_graphics = GraphicsController(160, 140, title="Pickle's Fetch Quest")

tile_image = DiskLoader.load_image('tiles/test.gif')

if __name__ == "__main__":
    pyglet.app.run()
