from ..types import Point2D

def cross(a: Point2D, b: Point2D, c: Point2D) -> float:
    """
    Returns the 2D cross product of AB and AC vectors, i.e., the z-component of
    the 3D cross product in a quadrant I Cartesian coordinate system (+x is
    right, +y is up). Returns a positive value if ABC is counter-clockwise,
    negative if clockwise, and zero if the points are collinear.

    Parameters
    ----------
    a : Point2D
        Point A
    b : Point2D
        Point B
    c : Point2D
        Point C

    Returns
    -------
    float
        2D cross product
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
