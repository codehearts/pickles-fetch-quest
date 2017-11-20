import operator


class Point2d(object):
    """A two dimensional point in space.

    Attributes:
        x (int): The x coordinate of the point.
        y (int): The y coordinate of the point.
    """

    def __init__(self, x, y):
        """Creates a new two dimensional point.

        Args:
            x (int): The x coordinate of the point.
            y (int): The y coordinate of the point.
        """
        super(Point2d, self).__init__()
        self.x = x
        self.y = y

    def _call_with_other(self, fn, other):
        """Calls a function for both coordinates with another object.

        Used to prevent code duplication for operator overloading.

        Args:
            fn (callable): Function to call with an individual coordinate
                and `other`. Will be called with `self.x` and `other` before
                `self.y` and `other`.
            other (:obj:`Object`): The other object to pass to the function.

        Returns:
            A tuple of the return values of the function when called with
            `self.x`, `self.y`, and `other`.
        """
        try:
            x_result, y_result = fn(self.x, other.x), fn(self.y, other.y)
        except AttributeError:
            try:
                x_result, y_result = fn(self.x, other[0]), fn(self.y, other[1])
            except TypeError:
                x_result, y_result = fn(self.x, other), fn(self.y, other)
        finally:
            return (x_result, y_result)

    def __eq__(self, other):
        """Determines if this point is equal to another object.

        Args:
            other (:obj:`Object`): The value to compare against the point.
        """
        equalities = self._call_with_other(operator.eq, other)
        return equalities[0] and equalities[1]

    def __ne__(self, other):
        """Determines if this point is not equal to another object.

        Args:
            other (:obj:`Object`): The value to compare against the point.
        """
        equalities = self._call_with_other(operator.ne, other)
        return equalities[0] or equalities[1]

    def __add__(self, other):
        """Adds to the x and y coordinates.

        If `other` is another :cls:`Point`, the x and y coordinates will be
        summed with the x and y coordinates of the other point respectively.

        If `other` is an iterable, the first index is added to the x
        coordinate and the second index is added to the y coordinate.

        If `other` is a number, it will be added to both coordinates.

        Args:
            other (:obj:`Object`): The value to add to the point.
        """
        return Point2d(*self._call_with_other(operator.add, other))

    def __mul__(self, other):
        """Multiplies the x and y coordinates by the value.

        If `other` is another :cls:`Point`, the x and y coordinates will be
        multiplied by the x and y coordinates of the other point respectively.

        If `other` is an iterable, the x coordinate is multiplied by the first
        index and the y coordinate is multiplied by the second index.

        If `other` is a number, both coordinates will be multiplied by it.

        Args:
            other (:obj:`Object`): The value to multiply the point by.
        """
        return Point2d(*self._call_with_other(operator.mul, other))

    def __floordiv__(self, other):
        """Divides the x and y coordinates by the value, flooring the result.

        If `other` is another :cls:`Point`, the x and y coordinates will be
        divided by the x and y coordinates of the other point respectively.

        If `other` is an iterable, the x coordinate is divided by the first
        index and the y coordinate is divided by the second index.

        If `other` is a number, both coordinates will be divided by it.

        Args:
            other (:obj:`Object`): The value to divide the point by.
        """
        return Point2d(*self._call_with_other(operator.floordiv, other))

    def __iadd__(self, other):
        """Adds to the x and y coordinates.

        See :fn:`__add__` for documentation on how `other` will be processed.

        Args:
            other (:obj:`Object`): The value to add to the point.
        """
        self.x, self.y = self._call_with_other(operator.add, other)
        return self

    def __imul__(self, other):
        """Multiplies the x and y coordinates by the value.

        See :fn:`__mul__` for documentation on how `other` will be processed.

        Args:
            other (:obj:`Object`): The value to multiply the point by.
        """
        self.x, self.y = self._call_with_other(operator.mul, other)
        return self

    def __ifloordiv__(self, other):
        """Divides the x and y coordinates by the value, flooring the result.


        See :fn:`__floordiv__` for documentation on how `other` will be
        processed.

        Args:
            other (:obj:`Object`): The value to divide the point by.
        """
        self.x, self.y = self._call_with_other(operator.floordiv, other)
        return self