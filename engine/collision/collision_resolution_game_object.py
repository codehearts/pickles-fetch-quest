from .collision_resolution_1d import get_nonoverlapping_coordinate_1d
from ..geometry import detect_overlap_1d, detect_overlap_2d


def resolve_game_object_collision(first, second):
    """Resolves a collision between two game objects by repositioning one.

    Objects with the lowest velocity on a given axis will be repositioned
    along that axis to resolve the collision.

    Args:
        first (:obj:`GameObject`): The first game object in the collision.
        second (:obj:`GameObject`): The second game object in the collision.

    Returns:
        True if a collision was resolved, False if no collision existed.
    """
    # Objects are not overlapping
    if not detect_overlap_2d(first, second):
        return False

    # Move the lighter object, leave the heavier object resting
    first_is_heavier = first.physics.mass > second.physics.mass
    moving, resting = (second, first) if first_is_heavier else (first, second)

    resolve_game_object_x_collision(moving, resting)
    resolve_game_object_y_collision(moving, resting)

    return True


def resolve_game_object_x_collision(moving, static):
    """Resolves a collision by moving an object along the x axis.

    Args:
        moving (:obj:`GameObject`): The object to move along the x axis.
        static (:obj:`GameObject`): The object to leave as-is.
    """
    # Detect overlap before applying velocity along y axis, but after x axis
    previous_y = moving.y - moving.physics.velocity.y
    if detect_overlap_1d(previous_y, moving.height, static.y, static.height):
        # Overlap detected along y-axis, resolve collision on x-axis
        _resolve_game_object_axis_collision(moving, static, 'x')


def resolve_game_object_y_collision(moving, static):
    """Resolves a collision by moving an object along the y axis.

    Args:
        moving (:obj:`GameObject`): The object to move along the y axis.
        static (:obj:`GameObject`): The object to leave as-is.
    """
    if detect_overlap_1d(moving.x, moving.width, static.x, static.width):
        # Overlap detected along x-axis, resolve collision on y-axis
        _resolve_game_object_axis_collision(moving, static, 'y')


def _resolve_game_object_axis_collision(moving, static, axis):
    """Resolves a collision by moving an object along the specified axis.

    Args:
        moving (:obj:`GameObject`): The object to move along the axis.
        static (:obj:`GameObject`): The object to leave as-is.
        axis (str): Either 'x' or 'y'.
    """
    moving_length = moving.width if axis == 'x' else moving.height
    static_length = static.width if axis == 'x' else static.height

    # Get a new coordinate for the moving object to resolve the collision
    resolved_coordinate = get_nonoverlapping_coordinate_1d(
        getattr(moving, axis),
        moving_length,
        getattr(moving.physics.velocity, axis),
        getattr(static, axis),
        static_length)

    # Cancel velocity/acceleration and update coordinate of moving object
    if resolved_coordinate != getattr(moving, axis):
        setattr(moving.physics.acceleration, axis, 0)
        setattr(moving.physics.velocity, axis, 0)
        setattr(moving, axis, resolved_coordinate)
