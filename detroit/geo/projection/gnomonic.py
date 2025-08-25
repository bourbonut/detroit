from math import atan, cos, sin
from .azimuthal import azimuthal_invert
from .projection import geo_projection
from ...types import Point2D

class GnomonicRaw:

    def __call__(self, x: float, y: float) -> Point2D:
        cy = cos(y)
        k = cos(x) * cy
        return [cy * sin(x) / k, sin(y) / k]

    def invert(self, x: float, y: float) -> Point2D:
        return azimuthal_invert(atan)

def geo_gnomonic():
    return geo_projection(GnomonicRaw()).scale(144.049).set_clip_angle(60)
