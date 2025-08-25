from .projection import geo_projection
from math import asin, cos, sin, sqrt
from ...types import Point2D

EPSILON2 = 1e-12
A1 = 1.340264
A2 = -0.081106
A3 = 0.000893
A4 = 0.003796
M = sqrt(3) / 2
iterations = 12

class EqualEarthRaw:
    
    def __call__(self, lambda_: float, phi: float) -> Point2D:
        l_ = asin(M * sin(phi))
        l2 = l_ * l_
        l6 = l2 * l2 * l2
        return [
            lambda_ * cos(l_) / (M * (A1 + 3 * A2 * l2 + l6 * (7 * A3 + 9 * A4 * l2))),
            l_ * (A1 + A2 * l2 + l6 * (A3 + A4 * l2))
        ]


    def invert(self, x: float, y: float) -> Point2D:
        l_ = y
        l2 = l_ * l_
        l6 = l2 * l2 * l2
        for i in range(iterations):
            fy = l_ * (A1 + A2 * l2 + l6 * (A3 + A4 * l2)) - y
            fpy = A1 + 3 * A2 * l2 + l6 * (7 * A3 + 9 * A4 * l2)
            delta = fy / fpy
            l_ -= delta
            l2 = l_ * l_
            l6 = l2 * l2 * l2
            if abs(delta) < EPSILON2:
                break
        return [
            M * x * (A1 + 3 * A2 * l2 + l6 * (7 * A3 + 9 * A4 * l2)) / cos(l_),
            asin(sin(l_) / M)
        ]


def geo_equal_earth():
    return geo_projection(EqualEarthRaw()).scale(177.158)
