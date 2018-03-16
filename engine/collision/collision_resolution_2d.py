from .collision_resolution_1d import get_nonoverlapping_coordinate_1d
from ..geometry import detect_overlap_1d


def get_nonoverlapping_coordinates_2d(first, first_velocity, second):
    """Returns new coordinates for the first rectangle to resolve a
    2d collision.

    Args:
        first (:obj:`Rectangle`): Rectangle to calculate coordinates for.
        first_velocity (:obj:`Point2d`): The velocity of the first rectangle.
        second (:obj:`Rectangle`): Second rectangle.

    Returns:
        A tuple of ints with the bottom left coordinate for the first rectangle
        to resolve the collision. The first and second indices are the x and y
        coordinate respectively.
    """
    x = first.x
    y = first.y
    previous_y = first.y - first_velocity.y

    # Detect overlap before applying velocity along y axis, but after x axis
    if detect_overlap_1d(previous_y, first.height, second.y, second.height):
        # Overlap detected along y-axis, resolve collision on x-axis
        x = get_nonoverlapping_coordinate_1d(first.x, first.width,
                                             first_velocity.x,
                                             second.x, second.width)
    if detect_overlap_1d(x, first.width, second.x, second.width):
        # Overlap detected along x-axis, resolve collision on y-axis
        y = get_nonoverlapping_coordinate_1d(first.y, first.height,
                                             first_velocity.y,
                                             second.y, second.height)
    return (x, y)
