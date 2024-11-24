from ..interpolate import interpolate, interpolate_round, piecewise
from .continuous import identity
from .init import init_interpolator
from .linear import LinearBase
from .log import LogBase, transform_log, logp, powp, reflect, transform_logn
from .sequential import copy
from .symlog import transform_symlog
from .pow import transform_sqrt, transform_pow

import math
from datetime import datetime

class Diverging:

    def __init__(self, t):
        self.transform = t
        self._x0 = 0
        self._x1 = 0.5
        self._x2 = 1
        self._t0 = t(self._x0)
        self._t1 = t(self._x1)
        self._t2 = t(self._x2)
        self._k10 = 0 if self._t0 == self._t1 else 0.5 / (self._t1 - self._t0)
        self._k21 = 0 if self._t1 == self._t2 else 0.5 / (self._t2 - self._t1)
        self._s = -1 if self._t1 < self._t0 else 1
        self._interpolator = identity
        self._clamp = False
        self._unknown = None

    def __call__(self, x):
        if isinstance(x, float) and math.isnan(x):
            return self._unknown
        else:
            x = self.transform(x)
            k = self._k10 if self._s * x < self._s * self._t1 else self._k21
            x = 0.5 + (x - self._t1) * k
            return self._interpolator(max(0, min(1, x)) if self._clamp else x)

    def set_domain(self, domain):
        self._x0, self._x1, self._x2 = map(float, list(domain)[:3])
        self._t0 = self.transform(self._x0)
        self._t1 = self.transform(self._x1)
        self._t2 = self.transform(self._x2)
        self._k10 = 0 if self._t0 == self._t1 else 0.5 / (self._t1 - self._t0)
        self._k21 = 0 if self._t1 == self._t2 else 0.5 / (self._t2 - self._t1)
        self._s = -1 if self._t1 < self._t0 else 1
        return self

    @property
    def domain(self):
        return [self._x0, self._x1, self._x2]

    def set_clamp(self, clamp):
        self._clamp = bool(clamp)
        return self

    @property
    def clamp(self):
        return self._clamp

    def set_interpolator(self, interpolator):
        self._interpolator = interpolator
        return self

    @property
    def interpolator(self):
        return self._interpolator

    def set_range(self, range_vals):
        self._r0 = float(range_vals[0])
        self._r1 = float(range_vals[1])
        self._r2 = float(range_vals[2])
        self._interpolator = piecewise(interpolate, [self._r0, self._r1, self._r2])
        return self

    def set_range_round(self, range_vals):
        self._r0 = float(range_vals[0])
        self._r1 = float(range_vals[1])
        self._r2 = float(range_vals[2])
        self._interpolator = piecewise(interpolate_round, [self._r0, self._r1, self._r2])
        return self

    @property
    def range(self):
        return [self._interpolator(0), self._interpolator(0.5), self._interpolator(1)]

    def set_unknown(self, unknown):
        self._unknown = unknown
        return self

    @property
    def unknown(self):
        return self._unknown

class DivergingLinear(Diverging, LinearBase):
    def __init__(self):
        Diverging.__init__(self, identity)
        LogBase.__init__(self)

    def copy(self):
        return copy(self, DivergingLinear())


class DivergingLog(Diverging, LogBase):
    def __init__(self):
        Diverging.__init__(self, identity)
        LogBase.__init__(self)
        self.transform = transform_log
        self.set_domain([0.1, 1, 10])

    def _rescale(self):
        self._logs = logp(self._base)
        self._pows = powp(self._base)
        d = self.domain[0]
        if isinstance(d, datetime):
            d = d.timestamp()
        if d < 0:
            self._logs = reflect(self._logs)
            self._pows = reflect(self._pows)
            self.transform = transform_logn
        else:
            self.transform = transform_log
        return self

    def set_domain(self, domain):
        self._x0, self._x1, self._x2 = map(float, list(domain)[:3])
        self._rescale()
        super().set_domain(domain)
        return self

    def copy(self):
        return copy(self, DivergingLog()).base(self.base)

class DivergingSymlog(Diverging):
    def __init__(self, c = 1):
        self._c = c
        super().__init__(transform_symlog(self._c))

    def set_constant(self, c):
        self._c = float(c)
        self.transform = transform_symlog(self._c)
        self.rescale()
        return self

    def copy(self):
        return copy(self, DivergingSymlog()).set_constant(self.constant)

class DivergingPow(Diverging, LinearBase):
    def __init__(self, t = identity):
        super().__init__(t)
        self._exponent = 1

    def _rescale(self):
        if self._exponent == 1:
            self.transform = identity
            self.rescale()
            return self
        elif self._exponent == 0.5:
            self.transform = transform_sqrt
            self.rescale()
            return self
        else:
            self.transform = transform_pow(self._exponent)
            self.rescale()
            return self

    def set_exponent(self, exponent):
        self._exponent = float(exponent)
        return self._rescale()

    @property
    def exponent(self):
        return self._exponent

    def copy(self):
        return copy(self, DivergingPow()).set_exponent(self.exponent)


def scale_diverging(*args):
    scale = DivergingLinear()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


def scale_diverging_log(*args):
    scale = DivergingLog()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


def scale_diverging_symlog(*args):
    scale = DivergingSymlog()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


def scale_diverging_pow(*args):
    scale = DivergingPow()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


def scale_diverging_sqrt(*args):
    return scale_diverging_pow(*args).exponent(0.5)
