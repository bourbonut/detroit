from math import isnan, pi, cos, sin
from ...types import Number

def isvaluable(x: Number | None) -> bool:
    return x is not None and not isnan(x) and x

def point_radial(x: Number, y: Number) -> tuple[Number, Number]:
    x -= pi * 0.5
    return y * cos(x), y * sin(x)
