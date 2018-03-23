def detect_overlap_1d(first, first_length, second, second_length):
    """Detects overlap between two lines in one dimensional space.

    Args:
        first (int): Beginning of the first one dimensional line.
        first_length (int): The length of the first line.
        second (int): Beginning of the second one dimensional line.
        second_length (int): The length of the second line.

    Returns:
        True if the lines overlap, False otherwise.
    """
    first_end = first + first_length - 1
    second_end = second + second_length - 1
    return second_end >= first and first_end >= second
