from graphics_controller import GraphicsController
import pyglet.app

pickle_graphics = GraphicsController(160, 140, title="Pickle's Fetch Quest")

if __name__ == "__main__":
    pyglet.app.run()
