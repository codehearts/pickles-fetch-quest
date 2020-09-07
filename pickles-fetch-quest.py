from engine import audio, camera, disk, easing, factory, geometry, game_object
from engine import graphics, key_handler, room, tiled_editor, world
import pyglet.app
import pyglet.gl
import player


disk.DiskLoader.set_resource_paths(['resources/'])

game_width = 160
game_height = 140
game_scale = 4

audio_director = audio.AudioDirector(master_volume=0.99)
graphics_director = graphics.GraphicsController(
    game_width * game_scale, game_height * game_scale,
    title="Pickle's Fetch Quest")
key_handler = key_handler.KeyHandler(graphics_director)
game_world = world.World2d()
game_world_debugger = world.World2dDebug(game_world)

audio_director.attenuation_distance = 40

collision_sound = audio_director.load(
    'audio/sfx/bass-drum-hit.wav', streaming=False)

(pickle, pickle_graphics_idle) = player.create_player(key_handler)

graphics_director.add_listeners(on_update=pickle.update)
game_world.add_collider(pickle)


def create_floor_physics(**kwargs):
    x, y, width, height = (kwargs[k] for k in ('x', 'y', 'width', 'height'))

    tile = game_object.ImmovableGameObject(x, y, width, height)

    def play_collision_audio(other):
        collision_sound.play()
        # instance.position = (20, 0)

    tile.add_listeners(on_collider_enter=play_collision_audio)
    graphics_director.add_listeners(on_update=tile.update)
    game_world.add_collider(tile)

    return tile


def position_player(**kwargs):
    x, y, batch = (kwargs[k] for k in ('x', 'y', 'batch'))
    pickle.set_position((x, y))
    pickle_graphics_idle.batch = batch
    return pickle_graphics_idle


# Create factory to convert TMX object names into game objects
tmx_factory = factory.GenericFactory()
tmx_factory.add_recipe('pickle', position_player)
tmx_factory.add_recipe('floor', create_floor_physics)

# Load the entry room from the Tiled editor save file
entry_room_loader = tiled_editor.TmxLoader('rooms/entry-room.tmx', tmx_factory)
entry_room = room.Room(entry_room_loader.layers)

camera = camera.Camera(game_width, game_height)
camera.set_boundary(entry_room.width, entry_room.height)
camera.scale = game_scale
camera.follow = pickle
camera.follow_lead = geometry.Point2d(48, 0)
camera.follow_deadzone = geometry.Rectangle(
    x=game_width // 2 - 16, y=game_height // 2, width=32, height=48)
camera.follow_easing = easing.LinearInterpolation(0.08)


def on_update(dt):
    game_world.update(dt)
    key_handler.update(dt)
    entry_room.update(dt)
    camera.update(dt)


graphics_director.add_listeners(on_update=on_update)


@graphics_director._window.event
def on_draw():
    graphics_director._window.clear()
    camera.attach()
    entry_room.draw()
    game_world_debugger.draw()
    camera.detach()


if __name__ == "__main__":
    # Enable alpha transparency in OpenGL
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(
        pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    # Use nearest neighbor for scaling (for crisp pixel art)
    pyglet.gl.glTexParameteri(
        pyglet.gl.GL_TEXTURE_2D,
        pyglet.gl.GL_TEXTURE_MAG_FILTER,
        pyglet.gl.GL_NEAREST)

    pyglet.app.run()
