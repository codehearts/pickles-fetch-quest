def divide_toward_zero(x, y):
    """Divides `x` by `y`, rounding the result towards zero.

    The division is performed without any floating point calculations.

    For exmaple:

        divide_toward_zero(2, 2) == 1
        divide_toward_zero(1, 2) == 0
        divide_toward_zero(0, 2) == 0
        divide_toward_zero(-1, 2) == 0
        divide_toward_zero(-2, 2) == -1

    Args:
        x (int): The numerator of the division.
        y (int): The denominator of the division.

    Returns:
        The int result rounded towards 0.
    """
    return (x // y) if (x * y) > 0 else ((x + (-x % y)) // y)
