from math import acos, sin
from ...types import Point2D
from .azimuthal import azimuthal_raw, azimuthal_invert
from .projection import geo_projection
from ..common import Projection

class AzimuthalEquidistantRaw:

    def __call__(self, lambda_: float, phi: float) -> Point2D:
        def scale(c: float) -> float:
            c = acos(c)
            return c / sin(c) if c != 0. else 0.
        return azimuthal_raw(scale)(lambda_, phi)

    def invert(self, x: float, y: float) -> Point2D:
        def angle(z: float) -> float:
            return z
        return azimuthal_invert(angle)(x, y)

def geo_azimuthal_equidistant() -> Projection:
    """
    The azimuthal equidistant projection.

    Returns
    -------
    Projection
        Projection object
    """
    return geo_projection(AzimuthalEquidistantRaw()).scale(79.4188).set_clip_angle(180 - 1e-3)
