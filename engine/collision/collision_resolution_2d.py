from .collision_resolution_1d import get_nonoverlapping_coordinate_1d
from engine import geometry


def get_nonoverlapping_coordinates_2d(first, first_velocity, second):
    """Returns new coordinates for the first rectangle to resolve a
    2d collision.

    Args:
        first (:obj:`engine.geometry.Rectangle`):
            Rectangle to calculate coordinates for.
        first_velocity (:obj:`engine.geometry.Point2d`):
            The velocity of the first rectangle.
        second (:obj:`engine.geometry.Rectangle`):
            Second rectangle.

    Returns:
        A tuple of ints with the bottom left coordinate for the first rectangle
        to resolve the collision. The first and second indices are the x and y
        coordinate respectively.
    """
    x = first.x
    y = first.y
    y_pv = first.y - first_velocity.y  # previous y coordinate of first object

    # Detect overlap before applying velocity along y axis, but after x axis
    if geometry.detect_overlap_1d(y_pv, first.height, second.y, second.height):
        # Overlap detected along y-axis, resolve collision on x-axis
        x = get_nonoverlapping_coordinate_1d(first.x, first.width,
                                             first_velocity.x,
                                             second.x, second.width)
    if geometry.detect_overlap_1d(x, first.width, second.x, second.width):
        # Overlap detected along x-axis, resolve collision on y-axis
        y = get_nonoverlapping_coordinate_1d(first.y, first.height,
                                             first_velocity.y,
                                             second.y, second.height)
    return (x, y)
