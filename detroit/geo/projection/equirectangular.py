from .projection import projection, ProjectionMutator

class GeoEquirectangularRaw:
    def __call__(self, lambda_: float, phi: float) -> tuple[float, float]:
        return [lambda_, phi]

    def invert(self, lambda_: float, phi: float) -> tuple[float, float]:
        return [lambda_, phi]

def geo_equirectangular() -> ProjectionMutator:
    return projection(GeoEquirectangularRaw()).scale(152.63)
