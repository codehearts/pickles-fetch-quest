from .overlap_detection_1d import detect_overlap_1d


def detect_overlap_2d(first, second):
    """Detects overlap between two rectangles in two dimensional space.

    Args:
        first (:obj:`engine.geometry.Rectangle`): The first rectangle.
        second (:obj:`engine.geometry.Rectangle`): The second rectangle.

    Returns:
        True if the rectangles overlap, False otherwise.
    """
    x_axis = detect_overlap_1d(first.x, first.width, second.x, second.width)
    y_axis = detect_overlap_1d(first.y, first.height, second.y, second.height)
    return x_axis and y_axis
