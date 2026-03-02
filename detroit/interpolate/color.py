import math
from collections.abc import Callable

from .constant import constant


def linear(a: float, d: float) -> Callable[[float], float]:
    def f(t: float) -> float:
        return a + t * d

    return f


def exponential(a: float, b: float, y: float) -> Callable[[float], float]:
    a = a**y
    b = b**y - a
    y = 1 / y

    def f(t: float) -> float:
        return (a + t * b) ** y

    return f


def hue(a: float, b: float) -> Callable[[float], float]:
    d = b - a
    if not math.isnan(d) and d:
        if d < -180 or 180 < d:
            return linear(a, d - 360 * round(d / 360))
        else:
            return linear(a, d)
    else:
        return constant(b if math.isnan(a) else a)


def gamma(y: float) -> Callable[[float, float], Callable[[float], float]]:
    if round(y) == 1.0:
        return color

    def f(a: float, b: float) -> Callable[[float], float]:
        d = b - a
        return (
            exponential(a, b, y)
            if not math.isnan(d) and d
            else constant(math.isnan(a) and b or a)
        )

    return f


def color(a: float, b: float) -> Callable[[float], float]:
    d = b - a
    return (
        linear(a, d) if not math.isnan(d) and d else constant(b if math.isnan(a) else a)
    )
