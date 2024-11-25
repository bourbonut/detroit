import math

from ..path import Path


class WithPath:
    def __init__(self):
        self._digits = 3

    def digits(self, digits=None):
        if digits is None:
            return self._digits
        d = math.floor(digits)
        if d < 0:
            raise ValueError(f"Invalid digits: {d}")
        self._digits = d
        return self

    def _path(self):
        return Path(self._digits)
