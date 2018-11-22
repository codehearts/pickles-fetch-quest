from engine import AudioDirector, CollisionResolver2d, DiskLoader
from engine import GraphicsController, GraphicsObject, KeyHandler, Physics2d
from engine import Rectangle, RESOLVE_COLLISIONS, Tile
from pyglet.window import key
import pyglet.app
import pyglet.gl

DiskLoader.set_resource_paths(['resources/'])

audio_director = AudioDirector(master_volume=0.99)
pickle_graphics = GraphicsController(160, 140, title="Pickle's Fetch Quest")
key_handler = KeyHandler(pickle_graphics)
collision_resolver = CollisionResolver2d()

audio_director.attenuation_distance = 40

collision_sound = audio_director.load(
    'audio/sfx/bass-drum-hit.wav', streaming=False)

tile_image = DiskLoader.load_image('tiles/test.gif')

graphics = []


def create_tile_graphic(x, y):
    tile_graphic = GraphicsObject({'default': tile_image}, x=x, y=y)
    graphics.append(tile_graphic)

    return tile_graphic


def create_physics_tile(x, y, states, *args, **kwargs):
    physics = Physics2d(*args, **kwargs)
    tile = Tile(states, x=x, y=y, physics=physics)

    def play_collision_audio(other):
        instance = collision_sound.play()
        instance.position = (20, 0)

    tile.add_listeners(on_collision=play_collision_audio)
    pickle_graphics.add_listeners(on_update=tile.update)
    collision_resolver.register(tile, RESOLVE_COLLISIONS)

    return tile


def on_update(dt):
    collision_resolver.resolve()
    key_handler.update(dt)


pickle_graphics.add_listeners(on_update=on_update)

# Floor
create_tile_graphic(-8, 24)
create_tile_graphic(8, 24)
create_tile_graphic(24, 24)
create_tile_graphic(40, 24)
create_tile_graphic(56, 24)
create_tile_graphic(72, 24)
create_tile_graphic(88, 24)
create_tile_graphic(104, 24)
create_tile_graphic(120, 24)
create_tile_graphic(136, 24)
create_tile_graphic(152, 24)
floor_states = {'default': Rectangle(x=0, y=0, width=176, height=16)}
create_physics_tile(-8, 24, floor_states, gravity=(0, 0))

# Left wall
create_tile_graphic(-8, 40)
create_tile_graphic(-8, 56)
create_tile_graphic(-8, 72)
create_tile_graphic(-8, 88)
create_tile_graphic(-8, 104)
left_wall_states = {'default': Rectangle(x=0, y=0, width=16, height=80)}
create_physics_tile(-8, 40, left_wall_states, gravity=(0, 0))

# Right wall
create_tile_graphic(152, 40)
create_tile_graphic(152, 56)
create_tile_graphic(152, 72)
create_tile_graphic(152, 88)
create_tile_graphic(152, 104)
right_wall_states = {'default': Rectangle(x=0, y=0, width=16, height=80)}
create_physics_tile(152, 40, right_wall_states, gravity=(0, 0))

# Player
pickle_frames = DiskLoader.load_image_grid('tiles/pickle.png', 1, 2)

pickle_graphic = GraphicsObject({
    'default': GraphicsObject.create_animation(pickle_frames, 1, loop=True)
    }, x=0, y=0)
graphics.append(pickle_graphic)

player_states = {
    'default': Rectangle(x=72, y=88, width=16, height=16)
}

player = create_physics_tile(72, 88, player_states, friction=75,
                             gravity=(0, -15), terminal_velocity=(2, 100))
player.add_listeners(on_move=pickle_graphic.set_position)


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
    for graphic in graphics:
        graphic._sprite.draw()


if __name__ == "__main__":
    # Enable alpha transparency in OpenGL
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(
        pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    pyglet.app.run()
