import math
from bisect import bisect_right


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
        self.j = j = min(len(domain), len(range_vals)) - 1
        self.d = [None] * j
        self.r = [None] * j

        if domain[j] < domain[0]:
            self.domain = domain = domain[::-1]
            range_vals = range_vals[::-1]

        for i in range(j):
            self.d[i] = normalize(domain[i], domain[i + 1])
            self.r[i] = interpolate(range_vals[i], range_vals[i + 1])

    def __call__(self, x):
        x = self.d[bisect_right(self.domain, x, 1, self.j) - 1](x)
        return self.r[bisect_right(self.domain, x, 1, self.j) - 1](x)


def copy(source, target):
    return (
        target.domain(source.domain())
        .range(source.range())
        .interpolate(source.interpolate())
        .clamp(source.clamp())
        .unknown(source.unknown())
    )


def normalize(a, b):
    b = b - a
    if b:
        return lambda x: (x - a) / b
    else:
        return math.nan if math.isnan(b) else 0.5


def clamper(a, b):
    if a > b:
        a, b = b, a
    return lambda x: max(a, min(b, x))


def interpolate_number(a, b):
    a, b = float(a), float(b)
    return lambda t: a * (1 - t) + b * t


def interpolate_round(a, b):
    a, b = float(a), float(b)
    return lambda t: round(a * (1 - t) + b * t)


def interpolate_value(a, b):
    if b is None or isinstance(b, bool):
        return constant(b)
    if isinstance(b, (int, float)):
        return number
    if isinstance(b, str):
        c = color(b)
        return rgb if c else string
    if isinstance(b, color):
        return rgb
    if isinstance(b, datetime.date):
        return date
    if isNumberArray(b):
        return numberArray
    if isinstance(b, (list, tuple)):
        return genericArray
    if not hasattr(b, "valueOf") and not hasattr(b, "__str__") or math.isnan(b):
        return object_interpolator
    return number


def identity(x):
    return x


class Transformer:
    def __init__(self, t, u):
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
        if self.clamp != identity:
            self.clamp = clamper(self._domain[0], self._domain[n - 1])
        self.piecewise = PolyMap if n > 2 else BiMap
        self.output = self.input = None
        return self.scale

    def scale(self, x):
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return self._unknown
        else:
            if not self.output:
                domain = [self.transform(x) for x in self._domain]
                self.output = piecewise(domain, self._range, self._interpolate)
            return self.output(self.transform(self.clamp_func(x)))

    def invert(self, y):
        if not self.input:
            range_vals = [self.transform(x) for x in self._domain]
            self.input = piecewise(self._range, range_vals, interpolate_number)
        return self.clamp(self.untransform(self.input(y)))

    def domain(self, *args):
        if args:
            self._domain = list(map(float, args))
            return rescale()
        return copy(self._domain)

    def range(self, *args):
        if args:
            self._range = list(map(float, args))
            return rescale()
        return list(self._range)

    def range_round(self, *args):
        self._range = list(map(float, args))
        self._interpolate = interpolate_round
        return rescale()

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
            return scale
        return self._unknown
