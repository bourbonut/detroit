from math import isnan, pi, cos, sin, inf
from ...types import Number
from abc import ABC, abstractclassmethod

def isvaluable(x: Number | None) -> bool:
    return x is not None and not isnan(x) and x

def point_radial(x: Number, y: Number) -> tuple[Number, Number]:
    x -= pi * 0.5
    return y * cos(x), y * sin(x)

def sign(x: Number) -> bool:
    return -1 if x < 0 else 1

def fdiv(y: float, x: float) -> float:
    try:
        return y / x
    except ZeroDivisionError:
        return inf if y > 0 else -inf

class Curve(ABC):
    @abstractclassmethod
    def area_start(self):
        ...

    @abstractclassmethod
    def area_end(self):
        ...

    @abstractclassmethod
    def line_start(self):
        ...

    @abstractclassmethod
    def line_end(self):
        ...

    @abstractclassmethod
    def point(self, x, y):
        ...
