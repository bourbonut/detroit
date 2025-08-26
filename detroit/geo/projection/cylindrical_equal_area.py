from math import asin, cos, sin

from ...types import Point2D


class CylindricalEqualArea:
    def __init__(self, phi0):
        self._cos_phi0 = cos(phi0)

    def __call__(self, lambda_: float, phi: float) -> Point2D:
        return [lambda_ * self._cos_phi0, sin(phi) / self._cos_phi0]

    def invert(self, x: float, y: float) -> Point2D:
        return [x / self._cos_phi0, asin(y * self._cos_phi0)]
