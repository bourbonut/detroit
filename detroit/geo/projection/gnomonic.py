from math import atan, cos, sin

from ...types import Point2D
from ..common import Projection
from .azimuthal import azimuthal_invert
from .projection import geo_projection


class GnomonicRaw:
    def __call__(self, x: float, y: float) -> Point2D:
        cy = cos(y)
        k = cos(x) * cy
        return [cy * sin(x) / k, sin(y) / k]

    def invert(self, x: float, y: float) -> Point2D:
        return azimuthal_invert(atan)(x, y)


def geo_gnomonic() -> Projection:
    """
    The gnomonic projection.

    Returns
    -------
    Projection
        Projection object
    """
    return geo_projection(GnomonicRaw()).scale(144.049).set_clip_angle(60)
