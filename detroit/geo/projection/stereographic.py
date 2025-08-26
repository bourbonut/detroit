from math import atan, cos, sin

from ...types import Point2D
from ..common import Projection
from .azimuthal import azimuthal_invert
from .projection import geo_projection


class StereographicRaw:
    def __call__(self, x: float, y: float) -> Point2D:
        cy = cos(y)
        k = 1 + cos(x) * cy
        return [cy * sin(x) / k, sin(y) / k]

    def invert(self, x: float, y: float) -> Point2D:
        def angle(z: float) -> float:
            return 2 * atan(z)

        return azimuthal_invert(angle)(x, y)


def geo_stereographic() -> Projection:
    """
    The stereographic projection.

    Returns
    -------
    Projection
        Projection object
    """
    return geo_projection(StereographicRaw()).scale(250).set_clip_angle(142)
