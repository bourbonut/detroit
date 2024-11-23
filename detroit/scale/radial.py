from .continuous import Transformer, identity
from .init import init_range
from .linear import LinearBase
from .number import number
import math

def sign(x):
    return -1 if x < 0 else 1

def square(x):
    return sign(x) * x * x

def unsquare(x):
    return sign(x) * math.sqrt(abs(x))

class ScaleRadial(Transformer, LinearBase):
    def __init__(self, t = identity, u = identity):
        super().__init__(t, u)
        self._range_vals = [0, 1]
        self._round = False
        self._unknown = None

    def __call__(self, x):
        y = unsquare(super().__call__(x))
        if isinstance(y, float) and math.isnan(y):
            return self._unknown
        elif self._round:
            return round(y)
        else:
            return y

    def invert(self, y):
        return super().invert(square(y))

    def range(self, *args):
        if args:
            self._range_vals = [number(x) for x in args[0]]
            super().range([square(x) for x in self._range_vals])
            return self
        return self._range_vals.copy()

    def range_round(self, *args):
        return super().range(*args).round(True)

    def round(self, *args):
        if args:
            self._round = bool(args[0])
            return self
        return self._round

    def clamp(self, *args):
        if args:
            super().clamp(*args)
            return self
        return super().clamp()

    def unknown(self, *args):
        if args:
            self._unknown = args[0]
            return self
        return self._unknown

    def copy(self):
        return ScaleRadial().domain(self._domain).range(self._range_vals).round(self._round).clamp(self.clamp()).unknown(self._unknown)


def scale_radial(*args):
    scale = ScaleRadial()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
