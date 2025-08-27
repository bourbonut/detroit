from collections.abc import Callable
from math import isnan, nan

from ..common import PolygonStream

def asint(x: float) -> int | float:
    return int(x) if x.is_integer() else x

def round_zero(x: float) -> int:
    return int(round(x))

def round_digits(digits: int) -> Callable[[float], float]:
    def local_round(x: float) -> float:
        return asint(round(x, digits))
    return local_round

def identity(x: float) -> float:
    return asint(x)

class PathString(PolygonStream):
    def __init__(self, digits: int | None = None):
        digits = 15 if digits is None else digits
        if isnan(digits) or digits < 0:
            raise ValueError(f"Invalid digits: {digits}")

        self._digits = digits
        self._round = identity
        if digits == 0:
            self._round = round_zero
        elif self._digits < 15:
            self._round = round_digits(digits)

        self._cache_append = None
        self._cache_radius = None
        self._cache_circle = None

        self._radius = 4.5
        self._string = []
        self._line = nan
        self._point = nan

    def point_radius(self, radius: float):
        self._radius = radius
        return self

    def polygon_start(self):
        self._line = 0

    def polygon_end(self):
        self._line = nan

    def line_start(self):
        self._point = 0

    def line_end(self):
        if self._line == 0:
            self._string += "Z"
        self._point = nan

    def point(self, x: float, y: float):
        if self._point == 0:
            x = self._round(x)
            y = self._round(y)
            self.append(f"M{x},{y}")
            self._point = 1
        elif self._point == 1:
            x = self._round(x)
            y = self._round(y)
            self.append(f"L{x},{y}")
        else:
            x = self._round(x)
            y = self._round(y)
            self.append(f"M{x},{y}")
            if self._radius != self._cache_radius:
                r = self._round(self._radius)
                r2 = self._round(2 * self._radius)
                s = self._string
                self._string = []
                self.append(f"m0,{r}a{r},{r} 0 1,1 0,{-r2}a{r},{r} 0 1,1 0,{r2}z")
                self._cache_radius = r
                self._cache_circle = self._string
                self._string = s
            self._string += self._cache_circle

    def result(self) -> str | None:
        result = "".join(self._string)
        self._string = []
        return result if len(result) else None

    def append(self, string: str):
        self._string.append(string)

    def __str__(self) -> str:
        return "PathString()"
