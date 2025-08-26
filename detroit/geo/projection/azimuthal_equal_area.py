from math import asin, inf, sqrt

from ...types import Point2D
from ..common import Projection
from .azimuthal import azimuthal_invert, azimuthal_raw
from .projection import geo_projection


class AzimuthalEqualAreaRaw:
    def __call__(self, lambda_: float, phi: float) -> Point2D:
        def scale(cxcy: float) -> float:
            return sqrt(2 / (1 + cxcy)) if cxcy != -1 else inf

        return azimuthal_raw(scale)(lambda_, phi)

    def invert(self, x: float, y: float) -> Point2D:
        def angle(z: float) -> float:
            return 2 * asin(z / 2)

        return azimuthal_invert(angle)(x, y)


def geo_azimuthal_equal_area() -> Projection:
    """
    The azimuthal equal-area projection.

    Returns
    -------
    Projection
        Projection object
    """
    return (
        geo_projection(AzimuthalEqualAreaRaw()).scale(124.75).set_clip_angle(180 - 1e-3)
    )
