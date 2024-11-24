from ..interpolate import interpolate, interpolate_round
from .continuous import identity
from .init import init_interpolator
from .linear import LinearBase
from .log import LogBase, transform_log, logp, powp, reflect, transform_logn
from .symlog import transform_symlog
from .pow import transform_pow, transform_sqrt

import math
from datetime import datetime

class Sequential:

    def __init__(self, t):
        self._x0 = 0
        self._x1 = 1
        self._transform = t
        self._t0 = t(self._x0)
        self._t1 = t(self._x1)
        self._k10 = 0 if self._t0 == self._t1 else 1 / (self._t1 - self._t0)
        self._interpolator = identity
        self._clamp = False
        self._unknown = None

    def __call__(self, x):
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return self._unknown 
        if self._k10 == 0:
            x = 0.5 
        else:
            x = (self._transform(x) - self._t0) * self._k10
            if self._clamp:
                x = max(0, min(1, x)) 
        return self._interpolator(x)

    def set_domain(self, domain):
        self._x0, self._x1 = map(float, list(domain)[:2])
        self._t0 = self._transform(self._x0)
        self._t1 = self._transform(self._x1)
        self._k10 = 0 if self._t0 == self._t1 else 1 / (self._t1 - self._t0)
        return self

    @property
    def domain(self):
        return [self._x0, self._x1]

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
        self._r0, self._r1 = list(range_vals)[:2]
        self._interpolator = interpolate(self._r0, self._r1)
        return self

    @property
    def range(self):
        return [self._interpolator(0), self._interpolator(1)]

    def range_round(self, range_vals):
        self._r0, self._r1 = range_vals
        self._interpolator = interpolate_round(self._r0, self._r1)
        return self

    @property
    def set_range_round(self):
        return [self._interpolator(0), self._interpolator(1)]

    def set_unknown(self, *args):
        self._unknown = args[0]
        return self

    @property
    def unknown(self):
        return self._unknown


def copy(source, target):
    return target.set_domain(source.domain).set_interpolator(source.interpolator).set_clamp(source.clamp).set_unknown(source.unknown)


class SequentialLinear(Sequential, LinearBase):
    def __init__(self):
        Sequential.__init__(self, identity)
        LogBase.__init__(self)

    def copy(self):
        return copy(self, SequentialLinear())


class SequentialLog(Sequential, LogBase):
    def __init__(self):
        Sequential.__init__(self)
        LogBase.__init__(self)
        self.transform = transform_log
        self.set_domain([1, 10])

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
        self._x0, self._x1 = map(float, list(domain)[:2])
        self._rescale()
        super().set_domain(domain)
        return self

    def copy(self):
        return copy(self, SequentialLog()).base(self.base)

class SequentialSymlog(Sequential):
    def __init__(self, c = 1):
        self._c = c
        super().__init__(transform_symlog(self._c))

    def set_constant(self, c):
        self._c = float(c)
        self.transform = transform_symlog(self._c)
        self.rescale()
        return self

    def copy(self):
        return copy(self, SequentialSymlog()).set_constant(self.constant)

class SequentialPow(Sequential, LinearBase):
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
        return copy(self, SequentialPow()).set_exponent(self.exponent)

def scale_sequential(*args):
    scale = SequentialLinear()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


def scale_sequential_log(*args):
    scale = SequentialLog()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


def scale_sequential_symlog(*args):
    scale = SequentialSymlog()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


def scale_sequential_pow(*args):
    scale = SequentialPow()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


def scale_sequential_sqrt(*args):
    return scale_sequential_pow(*args).set_exponent(0.5)
