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
    if first.physics is None and second.physics is None:
        return False

    # First object has no physics, move second object
    if first.physics is None:
        return _resolve_game_object_collision_against_static(second, first)

    # Second object has no physics, move first object
    if second.physics is None:
        return _resolve_game_object_collision_against_static(first, second)

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
    if detect_overlap_1d(moving.y - moving.physics.velocity.y, moving.height,
                         static.y, static.height):
        # Overlap detected along y-axis, resolve collision on x-axis
        x = get_nonoverlapping_coordinate_1d(moving.x, moving.width,
                                             moving.physics.velocity.x,
                                             static.x, static.width)
        if x != moving.x:
            moving.physics.acceleration.x = 0
            moving.physics.velocity.x = 0
            moving.x = x


def resolve_game_object_y_collision(moving, static):
    """Resolves a collision by moving an object along the y axis.

    Args:
        moving (:obj:`GameObject`): The object to move along the y axis.
        static (:obj:`GameObject`): The object to leave as-is.
    """
    if detect_overlap_1d(moving.x, moving.width, static.x, static.width):
        # Overlap detected along x-axis, resolve collision on y-axis
        y = get_nonoverlapping_coordinate_1d(moving.y, moving.height,
                                             moving.physics.velocity.y,
                                             static.y, static.height)

        if y != moving.y:
            moving.physics.acceleration.y = 0
            moving.physics.velocity.y = 0
            moving.y = y


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

    # Cancel velocity along axis the object was moved along
    if new_coordinates[0] != moving.x:
        moving.physics.acceleration.x = 0
        moving.physics.velocity.x = 0
    if new_coordinates[1] != moving.y:
        moving.physics.acceleration.y = 0
        moving.physics.velocity.y = 0

    was_collision_resolved = (moving.coordinates != new_coordinates)
    moving.set_position(new_coordinates)

    return was_collision_resolved