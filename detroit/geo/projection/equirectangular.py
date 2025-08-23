from .projection import geo_projection, ProjectionMutator
from ...types import Point2D

class EquirectangularRaw:
    def __call__(self, lambda_: float, phi: float) -> Point2D:
        return [lambda_, phi]

    def invert(self, lambda_: float, phi: float) -> Point2D:
        return [lambda_, phi]

def geo_equirectangular() -> ProjectionMutator:
    """
    The equirectangular (plate carrée) projection

    Returns
    -------
    ProjectionMutator
        Projection object
    """
    return geo_projection(EquirectangularRaw()).scale(152.63)
