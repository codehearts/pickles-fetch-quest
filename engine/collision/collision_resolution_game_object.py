from .collision_resolution_1d import get_nonoverlapping_coordinate_1d
from engine import geometry


def resolve_game_object_collision(first, second):
    """Resolves a collision between two game objects by repositioning one.

    Objects with the lowest velocity on a given axis will be repositioned
    along that axis to resolve the collision.

    Args:
        first (:obj:`engine.game_object.GameObject`):
            The first game object in the collision.
        second (:obj:`engine.game_object.GameObject`):
            The second game object in the collision.

    Returns:
        A tuple of ints for the change in velocity along each axis.
    """
    # Objects are not overlapping
    if not geometry.detect_overlap_2d(first, second):
        return (0, 0)

    # Move the lighter object, leave the heavier object resting
    first_is_heavier = first.physics.mass > second.physics.mass
    moving, resting = (second, first) if first_is_heavier else (first, second)

    x_delta = resolve_game_object_x_collision(moving, resting)
    y_delta = resolve_game_object_y_collision(moving, resting)

    return (x_delta, y_delta)


def resolve_game_object_x_collision(moving, static):
    """Resolves a collision by moving an object along the x axis.

    Args:
        moving (:obj:`engine.game_object.GameObject`):
            The object to move along the x axis.
        static (:obj:`engine.game_object.GameObject`):
            The object to leave as-is.

    Returns:
        The change in the velocity of the object along the x axis.
    """
    # Detect overlap before applying velocity along y axis, but after x axis
    previous_y = moving.y - moving.physics.velocity.y
    has_overlap = geometry.detect_overlap_1d(
        previous_y, moving.height, static.y, static.height)

    if has_overlap:
        # Overlap detected along y-axis, resolve collision on x-axis
        return _resolve_game_object_axis_collision(moving, static, 'x')
    return 0


def resolve_game_object_y_collision(moving, static):
    """Resolves a collision by moving an object along the y axis.

    Args:
        moving (:obj:`engine.game_object.GameObject`):
            The object to move along the y axis.
        static (:obj:`engine.game_object.GameObject`):
            The object to leave as-is.

    Returns:
        The change in the velocity of the object along the y axis.
    """
    has_overlap = geometry.detect_overlap_1d(
        moving.x, moving.width, static.x, static.width)

    if has_overlap:
        # Overlap detected along x-axis, resolve collision on y-axis
        return _resolve_game_object_axis_collision(moving, static, 'y')
    return 0


def _resolve_game_object_axis_collision(moving, static, axis):
    """Resolves a collision by moving an object along the specified axis.

    Args:
        moving (:obj:`engine.game_object.GameObject`):
            The object to move along the axis.
        static (:obj:`engine.game_object.GameObject`):
            The object to leave as-is.
        axis (str): Either 'x' or 'y'.

    Returns:
        The delta between the original velocity and the resolved velocity.
    """
    moving_length = moving.width if axis == 'x' else moving.height
    static_length = static.width if axis == 'x' else static.height

    original_moving_position = getattr(moving, axis)
    original_velocity = getattr(moving.physics.velocity, axis)

    # Get a new coordinate for the moving object to resolve the collision
    resolved_coordinate = get_nonoverlapping_coordinate_1d(
        original_moving_position,
        moving_length,
        original_velocity,
        getattr(static, axis),
        static_length)

    # Cancel velocity/acceleration and update coordinate of moving object
    if abs(resolved_coordinate - original_moving_position) != 0:
        setattr(moving.physics.acceleration, axis, 0)
        setattr(moving.physics.velocity, axis, 0)
        setattr(moving, axis, resolved_coordinate)

    return abs(original_velocity - getattr(moving.physics.velocity, axis))
