from ..types import Point2D

def area(polygon: list[Point2D]) -> float:
    """
    Returns the signed area of the specified polygon. If the vertices of the
    polygon are in counterclockwise order (assuming a coordinate system where
    the origin is in the top-left corner), the returned area is positive;
    otherwise it is negative, or zero.

    Parameters
    ----------
    polygon : list[Point2D]
        Polygon

    Returns
    -------
    float
        Signed area of the specified polygon

    Examples
    --------
    >>> d3.polygon_area([[1, 1], [1.5, 0], [2, 1]])
    -0.5
    """
    b = polygon[-1]
    area = 0
    for point in polygon:
        a = b
        b = point
        area += a[1] * b[0] - a[0] * b[1]

    return area * 0.5
