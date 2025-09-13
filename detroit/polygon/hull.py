from ..types import Point2D
from .cross import cross
from functools import cmp_to_key

def lexicographic_order(a: Point2D, b: Point2D) -> float:
    return a[0] - b[0] or a[1] - b[1]


def compute_upper_hull_indexes(points: list[Point2D]) -> list[int]:
    indexes = [0, 1] + [None] * (len(points) - 2)
    size = 2

    for i in range(2, len(points)):
        while size > 1 and cross(points[indexes[size - 2]], points[indexes[size - 1]], points[i]) <= 0:
            size -= 1
        indexes[size] = i
        size += 1

    return indexes[:size]

def hull(points: list[Point2D]) -> list[Point2D] | None:
    """
    Returns the convex hull of the specified points using `Andrew's monotone
    chain algorithm
    <https://en.wikibooks.org/wiki/Algorithm_Implementation/Geometry/Convex_hull/Monotone_chain>`_.
    The returned hull is represented as an array containing a subset of the
    input points arranged in counterclockwise order. Returns :code:`None` if
    points has fewer than three elements.

    Parameters
    ----------
    points : list[Point2D]
        List of points

    Returns
    -------
    list[Point2D] | None
        Convex hull or :code:`None` if :code:`points` has fewer than three
        elements.
    
    Examples
    --------
    >>> points = [
    ...     [2, 2],
    ...     [6, 8],
    ...     [10, 10],
    ...     [12, 10],
    ...     [14, 4],
    ...     [20, 4],
    ...     [24, 8],
    ...     [29, 6],
    ...     [32, 4],
    ...     [35, 5],
    ...     [38, 2],
    ... ]
    >>> d3.polygon_hull(points)
    [[38, 2], [2, 2], [6, 8], [10, 10], [12, 10], [24, 8], [35, 5]]
    """
    n = len(points)
    if n < 3:
        return None

    sorted_points = [None] * n
    flipped_points = [None] * n
    
    for i, point in enumerate(points):
        sorted_points[i] = [point[0], point[1], i]

    sorted_points.sort(key=cmp_to_key(lexicographic_order))

    for i, point in enumerate(sorted_points):
        flipped_points[i] = [point[0], -point[1]]

    upper_indexes = compute_upper_hull_indexes(sorted_points)
    lower_indexes = compute_upper_hull_indexes(flipped_points)

    skip_left = lower_indexes[0] == upper_indexes[0]
    skip_right = lower_indexes[-1] == upper_indexes[-1]
    hull = []

    for i in range(len(upper_indexes) - 1, -1, -1):
        hull.append(points[sorted_points[upper_indexes[i]][2]])

    for i in range(skip_left, len(lower_indexes) - skip_right):
        hull.append(points[sorted_points[lower_indexes[i]][2]])

    return hull
