from ..types import Point2D

def contains(polygon: list[Point2D], point: Point2D) -> bool:
    """
    Returns :code:`True` if and only if the specified point is inside the
    specified polygon.


    Parameters
    ----------
    polygon : list[Point2D]
        Polygon
    point : Point2D
        2D Point

    Returns
    -------
    bool
        :code:`True` if and only if the specified point is inside the specified
        polygon.

    Examples
    --------
    >>> d3.polygon_contains([[1, 1], [1.5, 0], [2, 1]], [1.5, 0.667])
    True
    """
    p = polygon[-1]
    x, y = point
    x0, y0 = p
    inside = False

    for point in polygon:
        x1, y1 = point
        if (y1 > y) != (y0 > y) and x < (x0 - x1) * (y - y1) / (y0 - y1) + x1:
            inside = not inside
        x0, y0 = x1, y1

    return inside
