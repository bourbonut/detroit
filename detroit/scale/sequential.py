from ..interpolate import interpolate, interpolate_round
from .continuous import identity
from .init import init_interpolator
from .linear import linearish
from .log import loggish
from .symlog import symlogish
from .pow import powish

def transformer():
    x0 = 0
    x1 = 1
    t0 = None
    t1 = None
    k10 = None
    transform = None
    interpolator = identity
    clamp = False
    unknown = None

    def scale(x):
        return unknown if x is None or (isinstance(x, float) and math.isnan(x)) else interpolator(k10 == 0 and 0.5 or (x := (transform(x) - t0) * k10, clamp and max(0, min(1, x)) or x))

    def domain_func(_=None):
        nonlocal x0, x1, t0, t1, k10
        if _ is not None:
            x0, x1 = map(float, _)
            t0 = transform(x0)
            t1 = transform(x1)
            k10 = t0 == t1 and 0 or 1 / (t1 - t0)
            return scale
        return [x0, x1]

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
        return lambda _: (r0, r1) if _ is None else (r0 := float(_[0]), r1 := float(_[1]), interpolator := interpolate(r0, r1), scale)

    scale.range = range(interpolate)
    scale.range_round = range(interpolate_round)

    def unknown_func(_=None):
        nonlocal unknown
        if _ is not None:
            unknown = _
            return scale
        return unknown

    return lambda t: (transform := t, t0 := t(x0), t1 := t(x1), k10 := t0 == t1 and 0 or 1 / (t1 - t0), scale)


def copy(source, target):
    return target.domain(source.domain()).interpolator(source.interpolator()).clamp(source.clamp()).unknown(source.unknown())


def sequential():
    scale = linearish(transformer()(identity))
    scale.copy = lambda: copy(scale, sequential())
    return init_interpolator(scale)


def sequential_log():
    scale = loggish(transformer()).domain([1, 10])
    scale.copy = lambda: copy(scale, sequential_log()).base(scale.base())
    return init_interpolator(scale)


def sequential_symlog():
    scale = symlogish(transformer())
    scale.copy = lambda: copy(scale, sequential_symlog()).constant(scale.constant())
    return init_interpolator(scale)


def sequential_pow():
    scale = powish(transformer())
    scale.copy = lambda: copy(scale, sequential_pow()).exponent(scale.exponent())
    return init_interpolator(scale)


def sequential_sqrt():
    return sequential_pow().exponent(0.5)


# -----

