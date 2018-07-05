from .collision_resolution_2d import get_nonoverlapping_coordinates_2d
from .collision_resolution_1d import get_nonoverlapping_coordinate_1d
from ..geometry import detect_overlap_1d, detect_overlap_2d


def resolve_game_object_collision(first, second):
    """Resolves a collision between two game objects by repositioning one.

    Objects with the lowest velocity on a given axis will be repositioned
    along that axis to resolve the collision. If an object has no physics,
    the other object will always be moved.

    Args:
        first (:obj:`GameObject`): The first game object in the collision.
        second (:obj:`GameObject`): The second game object in the collision.

    Returns:
        True if a collision was resolved, False if no collision existed.
    """
    # No resolution can be performed if both objects lack physics
    if first.physics is None or second.physics is None:
        return _resolve_game_object_collision_without_physics(first, second)

    # Objects are not overlapping
    if not detect_overlap_2d(first, second):
        return False

    if abs(first.physics.velocity.x) > abs(second.physics.velocity.x):
        resolve_game_object_x_collision(first, second)
    else:
        resolve_game_object_x_collision(second, first)

    if abs(first.physics.velocity.y) > abs(second.physics.velocity.y):
        resolve_game_object_y_collision(first, second)
    else:
        resolve_game_object_y_collision(second, first)

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


def _resolve_game_object_collision_without_physics(first, second):
    """Resolves a collision between game objects which lack physics.

    If one of the two objects has physics, the collision will be resolved by
    repositioning the object with physics.

    Args:
        first (:obj:`GameObject`): The first game object in the collision.
        second (:obj:`GameObject`): The second game object in the collision.

    Returns:
        True if a collision was resolved, False if no collision existed.
    """
    # No resolution can be performed if both objects lack physics
    if first.physics is None and second.physics is None:
        return False

    # Consider the object with physics to be moving
    if first.physics is None:
        moving, static = second, first
    else:
        moving, static = first, second

    return _resolve_game_object_collision_against_static(moving, static)


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


def _resolve_game_object_collision_against_static(moving, static):
    """Resolves a collision by moving the moving object against the static.

    Args:
        moving (:obj:`GameObject`): The moving game object in the collision.
        static (:obj:`GameObject`): The static game object in the collision.

    Returns:
        True if the moving object was moved, False otherwise.
    """
    new_coordinates = get_nonoverlapping_coordinates_2d(
        moving, moving.physics.velocity, static)

    changed_coordinates = []

    # Detect coordinate change on x axis
    if new_coordinates[0] != moving.x:
        changed_coordinates.append('x')

    # Detect coordinate change on y axis
    if new_coordinates[1] != moving.y:
        changed_coordinates.append('y')

    # Cancel velocity along axis the object was moved along
    for axis in changed_coordinates:
        setattr(moving.physics.acceleration, axis, 0)
        setattr(moving.physics.velocity, axis, 0)

    was_collision_resolved = (moving.coordinates != new_coordinates)
    moving.set_position(new_coordinates)

    return was_collision_resolved
