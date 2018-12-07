from engine import audio, collision, disk, factory, geometry, graphics
from engine import game_object, key_handler, physics, room, tiled_editor
from pyglet.window import key
import pyglet.app
import pyglet.gl

disk.DiskLoader.set_resource_paths(['resources/'])

audio_director = audio.AudioDirector(master_volume=0.99)
pickle_graphics = graphics.GraphicsController(
    160, 140, title="Pickle's Fetch Quest")
key_handler = key_handler.KeyHandler(pickle_graphics)
collision_resolver = collision.CollisionResolver2d(2)

audio_director.attenuation_distance = 40

collision_sound = audio_director.load(
    'audio/sfx/bass-drum-hit.wav', streaming=False)


def create_physics_tile(x, y, states, *args, **kwargs):
    physics_object = physics.Physics2d(*args, **kwargs)
    tile = game_object.GameObject(states, x, y, physics_object)

    def play_collision_audio(other):
        instance = collision_sound.play()
        instance.position = (20, 0)

    tile.add_listeners(on_collision=play_collision_audio)
    pickle_graphics.add_listeners(on_update=tile.update)
    collision_resolver.register(tile, collision.RESOLVE_COLLISIONS)

    return tile


def create_floor_physics(**kwargs):
    x, y, width, height = (kwargs[k] for k in ('x', 'y', 'width', 'height'))

    physics_object = physics.Physics2d(mass=9999, gravity=(0, 0))
    floor_states = {'default': geometry.Rectangle(x, y, width, height)}
    tile = game_object.GameObject(floor_states, x, y, physics_object)

    def play_collision_audio(other):
        collision_sound.play()
        # instance.position = (20, 0)

    tile.add_listeners(on_collision=play_collision_audio)
    pickle_graphics.add_listeners(on_update=tile.update)
    collision_resolver.register(tile, collision.RESOLVE_COLLISIONS)

    return tile


pickle_frames = disk.DiskLoader.load_image_grid('tiles/pickle.png', 1, 2)
pickle_graphic = graphics.GraphicsObject(geometry.Point2d(0, 0), {
    'default':
        graphics.GraphicsObject.create_animation(pickle_frames, 1, loop=True)})

player_states = {'default': geometry.Rectangle(x=0, y=0, width=16, height=16)}
player = create_physics_tile(0, 0, player_states, friction=75,
                             gravity=(0, -15), terminal_velocity=(2, 100))

player.add_listeners(on_move=pickle_graphic.set_position)


def position_pickle(**kwargs):
    x, y, batch = (kwargs[k] for k in ('x', 'y', 'batch'))
    player.set_position((x, y))
    pickle_graphic.batch = batch
    return pickle_graphic


# Create factory to convert TMX object names into game objects
tmx_factory = factory.GenericFactory()
tmx_factory.add_recipe('pickle', position_pickle)
tmx_factory.add_recipe('floor', create_floor_physics)

# Load the entry room from the Tiled editor save file
entry_room_loader = tiled_editor.TmxLoader('rooms/entry-room.tmx', tmx_factory)
entry_room = room.Room(entry_room_loader.layers)


def on_update(dt):
    collision_resolver.resolve()
    key_handler.update(dt)
    entry_room.update(dt)


pickle_graphics.add_listeners(on_update=on_update)


class PlayerControls(object):
    def __init__(self, player_object, walk_acceleration, jump_height):
        self._player = player_object
        self._walk_acceleration = walk_acceleration
        self._jump_height = jump_height
        self._last_ground_position = player_object.y
        self._is_jumping = False

    @property
    def _is_aerial(self):
        return self._player.physics.velocity.y != 0 or self._is_jumping

    def jump(self, *args):
        if not self._is_aerial:
            self._last_ground_position = self._player.y
            self._player.physics.acceleration.y = 80
            self._is_jumping = True
        if self._player.y >= self._last_ground_position + self._jump_height:
            self._player.physics.acceleration.y = 0
        else:
            height_difference = self._player.y - self._last_ground_position
            jump_percent = 1 - (height_difference / self._jump_height)

            # Acceleration eases in until the object is past the jump height
            self._player.physics.acceleration.y *= pow(max(jump_percent, 0), 3)

    def cancel_jump(self, *args):
        self._player.physics.acceleration.y = 0
        self._is_jumping = False

    def walk_left(self, *args):
        self._player.physics.acceleration.x = -self._walk_acceleration

    def walk_right(self, *args):
        self._player.physics.acceleration.x = self._walk_acceleration

    def stop_walking(self, *args):
        self._player.physics.acceleration.x = 0


# Fine-grained player controls
player_controls = PlayerControls(player, walk_acceleration=30, jump_height=48)

key_handler.on_key_press(key.LEFT, lambda: pickle_graphic.scale_x(-1))
key_handler.on_key_press(key.RIGHT, lambda: pickle_graphic.scale_x(1))

# Player key down handlers
key_handler.on_key_down(key.LEFT, player_controls.walk_left)
key_handler.on_key_down(key.RIGHT, player_controls.walk_right)
key_handler.on_key_down(key.UP, player_controls.jump)

# Player key release handlers
key_handler.on_key_release(key.LEFT, player_controls.stop_walking)
key_handler.on_key_release(key.RIGHT, player_controls.stop_walking)
key_handler.on_key_release(key.UP, player_controls.cancel_jump)


@pickle_graphics._window.event
def on_draw():
    pickle_graphics._window.clear()
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
