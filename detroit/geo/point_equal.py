from ..types import Point2D

EPSILON = 1e-6


def point_equal(a: Point2D, b: Point2D) -> bool:
    return abs(a[0] - b[0]) < EPSILON and abs(a[1] - b[1]) < EPSILON
