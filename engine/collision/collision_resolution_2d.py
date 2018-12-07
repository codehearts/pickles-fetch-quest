from .collision_resolution_1d import get_nonoverlapping_coordinate_1d
from engine import geometry


def get_nonoverlapping_coordinates_2d(first, first_velocity, second):
    """Returns coordinates for the first rectangle to resolve a 2d collision.

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

    # Detect overlap before applying velocity along y axis, but after x axis
    if _detect_overlap(first.y - first_velocity.y, first, second, 'y'):
        # Overlap detected along y-axis, resolve collision on x-axis
        x = _get_coordinate(first, second, first_velocity, 'x')

    if _detect_overlap(x, first, second, 'x'):
        # Overlap detected along x-axis, resolve collision on y-axis
        y = _get_coordinate(first, second, first_velocity, 'y')

    return (x, y)


def _detect_overlap(first_axis, first, second, axis):
    """Returns whether the first overlaps the second on the axis."""
    dimension = 'width' if axis == 'x' else 'height'

    axis2 = getattr(second, axis)
    size1, size2 = getattr(first, dimension), getattr(second, dimension)

    return geometry.detect_overlap_1d(first_axis, size1, axis2, size2)


def _get_coordinate(first, second, first_velocity, axis):
    """Returns a new coordinate for the first object on the axis."""
    dimension = 'width' if axis == 'x' else 'height'

    axis1, axis2 = getattr(first, axis), getattr(second, axis)
    size1, size2 = getattr(first, dimension), getattr(second, dimension)
    speed = getattr(first_velocity, axis)

    return get_nonoverlapping_coordinate_1d(axis1, size1, speed, axis2, size2)
