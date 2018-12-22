from engine import audio, collision, disk, factory, geometry, graphics
from engine import game_object, key_handler, physics, room, tiled_editor
import pyglet.app
import pyglet.gl
import player


disk.DiskLoader.set_resource_paths(['resources/'])

audio_director = audio.AudioDirector(master_volume=0.99)
graphics_director = graphics.GraphicsController(
    160, 140, title="Pickle's Fetch Quest")
key_handler = key_handler.KeyHandler(graphics_director)
collision_resolver = collision.CollisionResolver2d()

audio_director.attenuation_distance = 40

collision_sound = audio_director.load(
    'audio/sfx/bass-drum-hit.wav', streaming=False)

(pickle, pickle_graphics) = player.create_player(key_handler)

graphics_director.add_listeners(on_update=pickle.update)
collision_resolver.register(pickle, collision.RESOLVE_COLLISIONS)


def create_floor_physics(**kwargs):
    x, y, width, height = (kwargs[k] for k in ('x', 'y', 'width', 'height'))

    physics_object = physics.Physics2d(mass=9999, gravity=(0, 0))
    floor_states = {'default': geometry.Rectangle(x, y, width, height)}
    tile = game_object.GameObject(floor_states, x, y, physics_object)

    def play_collision_audio(other):
        collision_sound.play()
        # instance.position = (20, 0)

    tile.add_listeners(on_collision=play_collision_audio)
    graphics_director.add_listeners(on_update=tile.update)
    collision_resolver.register(tile, collision.RESOLVE_COLLISIONS)

    return tile


def position_player(**kwargs):
    x, y, batch = (kwargs[k] for k in ('x', 'y', 'batch'))
    pickle.set_position((x, y))
    pickle_graphics.batch = batch
    return pickle_graphics


# Create factory to convert TMX object names into game objects
tmx_factory = factory.GenericFactory()
tmx_factory.add_recipe('pickle', position_player)
tmx_factory.add_recipe('floor', create_floor_physics)

# Load the entry room from the Tiled editor save file
entry_room_loader = tiled_editor.TmxLoader('rooms/entry-room.tmx', tmx_factory)
entry_room = room.Room(entry_room_loader.layers)


def on_update(dt):
    collision_resolver.resolve()
    key_handler.update(dt)
    entry_room.update(dt)


graphics_director.add_listeners(on_update=on_update)


@graphics_director._window.event
def on_draw():
    graphics_director._window.clear()
    entry_room.draw()


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
