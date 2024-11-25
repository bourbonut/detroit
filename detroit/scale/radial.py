import math

from .continuous import Transformer, identity
from .init import init_range
from .linear import LinearBase
from .number import number


def sign(x):
    return -1 if x < 0 else 1


def square(x):
    return sign(x) * x * x


def unsquare(x):
    return sign(x) * math.sqrt(abs(x))


class ScaleRadial(Transformer, LinearBase):
    def __init__(self, t=identity, u=identity):
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

    def set_range(self, range_vals):
        self._range_vals = [number(x) for x in range_vals]
        super().set_range([square(x) for x in self._range_vals])
        return self

    @property
    def range(self):
        return self._range_vals.copy()

    def set_range_round(self, range_vals):
        return super().set_range(range_vals).set_round(True)

    def set_round(self, round_val):
        self._round = bool(round_val)
        return self

    @property
    def round(self):
        return self._round

    def copy(self):
        return (
            ScaleRadial()
            .set_domain(self.domain)
            .set_range(self.range)
            .set_round(self.round)
            .set_clamp(self.clamp)
            .set_unknown(self._unknown)
        )


def scale_radial(*args):
    scale = ScaleRadial()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
