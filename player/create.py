from .platformer_controller import PlatformerController
from engine import disk, game_object, geometry, graphics, physics
from pyglet.window import key


def create_player(key_handler):
    """Creates a new player object.

    Args:
        key_handler (:obj:`engine.key_handler.KeyHandler`):
            The key handler for controlling the player.

    Returns:
        A tuple of :obj:`engine.game_object.GameObject` for the player object
        and :obj:`engine.graphics.GraphicsObject` for the player graphics.
    """
    # Animation frames from disk
    pickle_frames = disk.DiskLoader.load_image_grid('tiles/pickle.png', 1, 2)

    # Geometric states for the player
    pickle_states = {
        'default': geometry.Rectangle(x=0, y=0, width=16, height=16)}

    # Player physics
    pickle_physics = physics.Physics2d(
        friction=75, gravity=(0, -15), terminal_velocity=(2, 100))

    # Player graphics
    pickle_graphics = graphics.GraphicsObject(
        geometry.Point2d(0, 0),
        {
            'default': graphics.GraphicsObject.create_animation(
                pickle_frames, 1, loop=True)})

    # Player object
    pickle = game_object.GameObject(pickle_states, 0, 0, pickle_physics)

    # Player controls
    pickle_controls = PlatformerController(
        pickle, walk_acceleration=30, jump_height=48, jump_time=250)

    # Listeners
    pickle.add_listeners(on_move=pickle_graphics.set_position)
    pickle.add_listeners(on_collision=pickle_controls.process_collision)

    # Player key press handlers
    key_handler.on_key_press(key.LEFT, lambda: pickle_graphics.scale_x(-1))
    key_handler.on_key_press(key.RIGHT, lambda: pickle_graphics.scale_x(1))

    # Player key down handlers
    key_handler.on_key_down(key.LEFT, pickle_controls.walk_left)
    key_handler.on_key_down(key.RIGHT, pickle_controls.walk_right)
    key_handler.on_key_down(key.UP, pickle_controls.jump)

    # Player key release handlers
    key_handler.on_key_release(key.LEFT, pickle_controls.stop_walking)
    key_handler.on_key_release(key.RIGHT, pickle_controls.stop_walking)
    key_handler.on_key_release(key.UP, pickle_controls.cancel_jump)

    return (pickle, pickle_graphics)
