from engine import geometry


def get_nonoverlapping_coordinate_1d(first, first_length, first_velocity,
                                     second, second_length):
    """Returns a new coordinate for the first line to resolve a 1d collision.

    Args:
        first (int): Beginning of the one dimensional line to reposition.
        first_length (int): The length of the line to reposition.
        first_velocity (int): The velocity of the first line.
        second (int): Beginning of the second one dimensional line.
        second_length (int): The length of the second line.

    Returns:
        A new beginning for the first line to remove the overlap.
    """
    has_overlap = geometry.detect_overlap_1d(
        first, first_length, second, second_length)

    if not has_overlap:
        # Lines do not overlap, first line can stay where it is
        return first
    elif first_velocity < 0:
        # Lines overlap and first is moving back, resolve by moving forward
        return second + second_length
    else:
        # Lines overlap and first is moving forward, resolve by moving back
        return second - first_length
