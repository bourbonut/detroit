from ...types import Point2D
from ..common import Projection
from .projection import geo_projection


class EquirectangularRaw:
    def __call__(self, lambda_: float, phi: float) -> Point2D:
        return [lambda_, phi]

    def invert(self, lambda_: float, phi: float) -> Point2D:
        return [lambda_, phi]


def geo_equirectangular() -> Projection:
    """
    The equirectangular (plate carrée) projection

    Returns
    -------
    Projection
        Projection object
    """
    return geo_projection(EquirectangularRaw()).scale(152.63)
