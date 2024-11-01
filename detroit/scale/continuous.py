from bisect import bisect
from ..interpolate import interpolate as interpolate_value, interpolate_number, interpolate_round
from .constant import constant
from .number import number
import math
from datetime import datetime

def identity(x):
    return x

def normalize(a, b):
    if isinstance(a, datetime):
        a = a.timestamp()
    elif isinstance(a, str):
        a = float(a)
    if isinstance(b, datetime):
        b = b.timestamp()
    elif isinstance(b, str):
        b = float(b)
    b = b - a
    if not math.isnan(b) and b:
        def f(x):
            if isinstance(x, datetime):
                x = x.timestamp()
            elif isinstance(x, str):
                x = float(x)
            return (x - a) / b
        return f
    else:
        return constant(math.nan if math.isnan(b) else 0.5)

def clamper(a, b):
    if a > b:
        a, b = b, a
    def f(x):
        return max(a, min(b, x))
    return f

class BiMap:
    def __init__(self, domain, range_vals, interpolate):
        d0, d1 = domain[0], domain[1]
        r0, r1 = range_vals[0], range_vals[1]
        if d1 < d0:
            self.d0 = normalize(d1, d0)
            self.r0 = interpolate(r1, r0)
        else:
            self.d0 = normalize(d0, d1)
            self.r0 = interpolate(r0, r1)

    def __call__(self, x):
        return self.r0(self.d0(x))


class PolyMap:
    def __init__(self, domain, range_vals, interpolate):
        self.domain = domain
        self.j = j = min(len(self.domain), len(range_vals)) - 1
        self.d = [None] * j
        self.r = [None] * j

        if self.domain[j] < self.domain[0]:
            self.domain = self.domain[::-1]
            range_vals = range_vals[::-1]

        for i in range(j):
            self.d[i] = normalize(self.domain[i], self.domain[i + 1])
            self.r[i] = interpolate(range_vals[i], range_vals[i + 1])

    def __call__(self, x):
        i = bisect(self.domain, x, 1, self.j) - 1
        return self.r[i](self.d[i](x))


def copy(source, target):
    return (
        target.domain(source.domain())
        .range(source.range())
        .interpolate(source.interpolate())
        .clamp(source.clamp())
        .unknown(source.unknown())
    )

class Transformer:
    def __init__(self, t = identity, u = identity):
        self.transform = t
        self.untransform = u
        self._domain = [0, 1]
        self._range = [0, 1]
        self._clamp = identity
        self._interpolate = interpolate_value
        self._unknown = None
        self.input = None
        self.output = None

    def rescale(self):
        n = min(len(self._domain), len(self._range))
        if self._clamp != identity:
            self._clamp = clamper(self._domain[0], self._domain[n - 1])
        self.piecewise = PolyMap if n > 2 else BiMap
        self.output = self.input = None
        return self

    def __call__(self, x):
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return self._unknown
        else:
            if not self.output:
                domain = [self.transform(x) for x in self._domain]
                self.output = self.piecewise(domain, self._range, self._interpolate)
            return self.output(self.transform(self._clamp(x)))

    def invert(self, y):
        if not self.input:
            domain = [self.transform(x) for x in self._domain]
            self.input = self.piecewise(self._range, domain, interpolate_number)
        return self._clamp(self.untransform(self.input(y)))

    def domain(self, *args):
        if args:
            self._domain = list(map(number, args[0]))
            return self.rescale()
        return list(self._domain)

    def range(self, *args):
        if args:
            self._range = list(args[0])
            return self.rescale()
        return list(self._range)

    def range_round(self, *args):
        self._range = list(map(float, args[0]))
        self._interpolate = interpolate_round
        return self.rescale()

    def clamp(self, *args):
        if args:
            self._clamp = True if args[0] else identity
            return self.rescale()
        return self._clamp != identity

    def interpolate(self, *args):
        if args:
            self._interpolate = args[0]
            return self.rescale()
        return self._interpolate

    def unknown(self, *args):
        if args:
            self._unknown = args[0]
            return self.rescale()
        return self._unknown


def continuous():
    return Transformer(identity, identity)
