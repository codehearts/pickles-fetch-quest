def flip_1d_index_vertically(index, rows, columns):
    """Finds the index to the corresponding vertically flipped 1d matrix value.

    Consider a 1d matrix [1, 2, 3, 4, 5, 6] with 3 rows and 2 columns. The
    original and vertically flipped representations are shown below.

        1 2    5 6
        3 4 -> 3 4
        5 6    1 2

    This function allows the translated matrix to be accessed using indices
    into the original matrix, such that index 0 (value 1) becomes index 4
    (value 5, corresponding to index 0 of the flipped matrix).

    Args:
        index (int): Index into the original 1d matrix.
        rows (int): Number of rows in the matrix.
        columns (int): Number of columns in the matrix.

    Returns:
        The index for the corresponding value of the vertically flipped matrix,
        as an int.
    """
    # Get current row in 1d matrix, from 0 to rows-1
    current_row = index // columns

    # Flip row (0 -> rows-1, ..., rows-1 -> 0, etc.)
    flipped_row = rows - current_row - 1

    # Calculate total number of entries on preceding rows
    offset_row = flipped_row * columns

    # Calculate current column position in row
    offset_column = index % columns

    return offset_row + offset_column
