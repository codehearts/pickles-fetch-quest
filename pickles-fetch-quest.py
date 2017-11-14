from engine import DiskLoader, GraphicsController, GraphicsObject, Tile
import pyglet.app

DiskLoader.set_resource_paths(['resources/'])

pickle_graphics = GraphicsController(160, 140, title="Pickle's Fetch Quest")

tile_image = DiskLoader.load_image('tiles/test.gif')
tile_graphic = GraphicsObject({'default': tile_image})


def update_tile_graphic(event, sender):
    if event == 'position_changed':
        tile_graphic.set_position(sender.position)


tile = Tile(72, 64, 16, 16, update_tile_graphic)


@pickle_graphics._window.event
def on_draw():
    tile_graphic._sprite.draw()


if __name__ == "__main__":
    pyglet.app.run()
