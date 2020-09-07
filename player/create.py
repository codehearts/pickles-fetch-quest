from .platformer_controller import PlatformerController
from engine import disk, game_object, graphics
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

    # Player collider
    pickle_collider = game_object.PhysicalGameObject(
        x=0, y=0, width=16, height=16,
        friction=75, gravity=(0, -15), terminal_velocity=(2, 100))

    # Player graphics
    pickle_graphic_idle = graphics.GraphicsObject(
        graphics.GraphicsObject.create_animation(pickle_frames, 1, loop=True))

    # Player controls
    pickle_controls = PlatformerController(
        pickle_collider, walk_acceleration=30, jump_height=48, jump_time=250)

    # Attachments
    pickle_collider.attach(pickle_graphic_idle, (0, -1))

    # Listeners
    pickle_collider.add_listeners(
        on_collider_enter=pickle_controls.process_collision)

    # Player key press handlers
    key_handler.on_key_press(key.LEFT, lambda: pickle_graphic_idle.scale_x(-1))
    key_handler.on_key_press(key.RIGHT, lambda: pickle_graphic_idle.scale_x(1))

    # Player key down handlers
    key_handler.on_key_down(key.LEFT, pickle_controls.walk_left)
    key_handler.on_key_down(key.RIGHT, pickle_controls.walk_right)
    key_handler.on_key_down(key.UP, pickle_controls.jump)

    # Player key release handlers
    key_handler.on_key_release(key.LEFT, pickle_controls.stop_walking)
    key_handler.on_key_release(key.RIGHT, pickle_controls.stop_walking)
    key_handler.on_key_release(key.UP, pickle_controls.cancel_jump)

    return (pickle_collider, pickle_graphic_idle)
