from ..types import Point2D
from math import hypot

def length(polygon: list[Point2D]) -> float:
    """
    Returns the length of the perimeter of the specified polygon.

    Parameters
    ----------
    polygon : list[Point2D]
        Polygon

    Returns
    -------
    float
        Length of the perimeter of the specified polygon.

    Examples
    --------
    >>> d3.polygon_length([[1, 1], [1.5, 0], [2, 1]])
    3.23606797749979
    """
    b = polygon[-1]
    xb, yb = b
    perimeter = 0

    for point in polygon:
        xa, ya = xb, yb
        b = point
        xb, yb = point
        xa -= xb
        ya -= yb
        perimeter += hypot(xa, ya)

    return perimeter
