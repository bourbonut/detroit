from collections.abc import Callable
from math import asin, atan2, cos, isinf, sin, sqrt


def azimuthal_raw(
    scale: Callable[[float], float],
) -> Callable[[float, float], tuple[float, float]]:
    def call(x, y):
        cx = cos(x)
        cy = cos(y)
        k = scale(cx * cy)
        if isinf(k):
            return [2, 0]
        return [k * cy * sin(x), k * sin(y)]

    return call


def azimuthal_invert(
    angle: Callable[[float], float],
) -> Callable[[float, float], tuple[float, float]]:
    def invert(x, y):
        z = sqrt(x * x + y * y)
        c = angle(z)
        sc = sin(c)
        cc = cos(c)
        return [atan2(x * sc, z * cc), asin(y * sc / z if z != 0.0 else 0.0)]

    return invert
