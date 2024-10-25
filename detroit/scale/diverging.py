from ..interpolate import interpolate, interpolate_round, piecewise
from .continuous import identity
from .init import init_interpolator
from .linear import linearish
from .log import loggish
from .sequential import copy
from .symlog import symlogish
from .pow import powish

def transformer():
    x0 = 0
    x1 = 0.5
    x2 = 1
    s = 1
    t0 = None
    t1 = None
    t2 = None
    k10 = None
    k21 = None
    interpolator = identity
    transform = None
    clamp = False
    unknown = None

    def scale(x):
        return unknown if (isinstance(x, float) and math.isnan(x)) else (x := 0.5 + ((x := float(transform(x))) - t1) * (s * x < s * t1 and k10 or k21), interpolator(clamp and max(0, min(1, x)) or x))

    def domain_func(_=None):
        nonlocal x0, x1, x2, t0, t1, t2, k10, k21, s
        if _ is not None:
            x0, x1, x2 = map(float, _)
            t0 = transform(x0)
            t1 = transform(x1)
            t2 = transform(x2)
            k10 = t0 == t1 and 0 or 0.5 / (t1 - t0)
            k21 = t1 == t2 and 0 or 0.5 / (t2 - t1)
            s = t1 < t0 and -1 or 1
            return scale
        return [x0, x1, x2]

    def clamp_func(_=None):
        nonlocal clamp
        if _ is not None:
            clamp = bool(_)
            return scale
        return clamp

    def interpolator_func(_=None):
        nonlocal interpolator
        if _ is not None:
            interpolator = _
            return scale
        return interpolator

    def range(interpolate):
        return lambda _: (r0, r1, r2) if _ is None else (r0 := float(_[0]), r1 := float(_[1]), r2 := float(_[2]), interpolator := piecewise(interpolate, [r0, r1, r2]), scale)

    scale.range = range(interpolate)
    scale.range_round = range(interpolate_round)

    def unknown_func(_=None):
        nonlocal unknown
        if _ is not None:
            unknown = _
            return scale
        return unknown

    return lambda t: (transform := t, t0 := t(x0), t1 := t(x1), t2 := t(x2), k10 := t0 == t1 and 0 or 0.5 / (t1 - t0), k21 := t1 == t2 and 0 or 0.5 / (t2 - t1), s := t1 < t0 and -1 or 1, scale)


def diverging():
    scale = linearish(transformer()(identity))
    scale.copy = lambda: copy(scale, diverging())
    return init_interpolator(scale)


def diverging_log():
    scale = loggish(transformer()).domain([0.1, 1, 10])
    scale.copy = lambda: copy(scale, diverging_log()).base(scale.base())
    return init_interpolator(scale)


def diverging_symlog():
    scale = symlogish(transformer())
    scale.copy = lambda: copy(scale, diverging_symlog()).constant(scale.constant())
    return init_interpolator(scale)


def diverging_pow():
    scale = powish(transformer())
    scale.copy = lambda: copy(scale, diverging_pow()).exponent(scale.exponent())
    return init_interpolator(scale)


def diverging_sqrt():
    return diverging_pow().exponent(0.5)


# -----

