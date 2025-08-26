from math import asin, cos, sin

from ...types import Point2D
from ..common import Projection
from .azimuthal import azimuthal_invert
from .projection import geo_projection

EPSILON = 1e-6


class OrthographicRaw:
    def __call__(self, x: float, y: float) -> Point2D:
        return [cos(y) * sin(x), sin(y)]

    def invert(self, x: float, y: float) -> Point2D:
        return azimuthal_invert(asin)(x, y)


def geo_orthographic() -> Projection:
    """
    The orthographic projection.

    Returns
    -------
    Projection
        Projection object
    """
    return geo_projection(OrthographicRaw()).scale(249.5).set_clip_angle(90 + EPSILON)
