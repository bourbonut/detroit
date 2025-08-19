from math import floor, nan, isnan
import re

from ...path.string_round import string_round

class PathString:
    def __init__(self, digits = None):
        self._append = self._append_default if digits is None else self._append_round
        self._radius = 4.5
        self._string = ""
        self._line = nan
        self._point = nan

        self._cache_digits = None
        self._cache_append = None
        self._cache_radius = None
        self._cache_circle = None

    def point_radius(self, radius):
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

    def point(self, x, y):
        if self._point == 0:
            self._append(f"M{x},{y}")
            self._point = 1
        elif self._point == 1:
            self._append(f"L{x},{y}")
        else:
            self._append(f"M{x},{y}")
            if self._radius != self._cache_radius or self._append != self._cache_append:
                r = self._radius
                s = self._string
                self._string = ""
                self._append(f"m0,{r}a{r},{r} 0 1,1 0,{-2 * r}a{r},{r} 0 1,1 0,{2 * r}z")
                self._cache_radius = r
                self._cache_append = self._append
                self._cache_circle = self._string
                self._string = s
            self._string += self._cache_circle

    def result(self):
        result = self._string
        self._string = ""
        return result if len(result) else None

    def _append_default(self, string):
        self._string += string

    def _append_round(self, digits):
        d = floor(digits)
        if isnan(d) or d < 0:
            raise ValueError(f"Invalid digits: {digits}")
        if d > 15:
            return self._append_default
        if d != self._cache_digits:
            self._cache_digits = d
            def append_round(self, string):
                floats = re.findall(r"\d+\.\d+", string)
                rounds = [string_round(f, d) for f in floats]
                for (old, new) in zip(floats, rounds):
                    string = string.replace(old, new)
                self._string += string
            self._cache_append = append_round
        return self._cache_append
