from ..types import Point2D

def centroid(polygon: list[Point2D]) -> Point2D:
    """
    Returns the centroid of the specified polygon.

    Parameters
    ----------
    polygon : list[Point2D]
        Polygon

    Returns
    -------
    Point2D
        Centroid point

    Examples
    --------
    >>> d3.polygon_centroid([[1, 1], [1.5, 0], [2, 1]])
    [1.5, 0.6666666666666666]
    """
    x = 0
    y = 0
    b = polygon[-1]
    k = 0

    for point in polygon:
        a = b
        b = point
        c = a[0] * b[1] - b[0] * a[1]
        k += c
        x += (a[0] + b[0]) * c
        y += (a[1] + b[1]) * c

    k *= 3
    return [x / k, y / k]
