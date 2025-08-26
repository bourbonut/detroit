from math import cos, pi, sin

from ..types import Point2D


def point_radial(angle: float, radius: float) -> Point2D:
    """
    Returns the point :code:`[x, y]` for the given angle in radians, with 0 at
    -y (12 o'clock) and positive angles proceeding clockwise, and the given
    radius.

    Parameters
    ----------
    angle : float
        Angle value
    radius : float
        Radius value

    Returns
    -------
    Point2D
        2D Point
    """
    angle -= pi * 0.5
    return [radius * cos(angle), radius * sin(angle)]
