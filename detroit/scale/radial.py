from .continuous import continuous
from .init import init_range
from .linear import linearish
from .number import number

def square(x):
    return math.sign(x) * x * x

def unsquare(x):
    return math.sign(x) * math.sqrt(abs(x))

def radial():
    squared = continuous()
    range_vals = [0, 1]
    round = False
    unknown = None

    def scale(x):
        y = unsquare(squared(x))
        return unknown if (isinstance(y, float) and math.isnan(y)) else (round and round(y) or y)

    def invert(y):
        return squared.invert(square(y))

    def domain_func(_=None):
        if _ is not None:
            squared.domain(_)
            return scale
        return squared.domain()

    def range_func(_=None):
        if _ is not None:
            squared.range([float(x) for x in _])
            return scale
        return range_vals.copy()

    def range_round_func(_=None):
        return scale.range(_).round(True)

    def round_func(_=None):
        nonlocal round
        if _ is not None:
            round = bool(_)
            return scale
        return round

    def clamp_func(_=None):
        if _ is not None:
            squared.clamp(_)
            return scale
        return squared.clamp()

    def unknown_func(_=None):
        nonlocal unknown
        if _ is not None:
            unknown = _
            return scale
        return unknown

    def copy():
        return radial().domain(squared.domain()).range(range_vals).round(round).clamp(squared.clamp()).unknown(unknown)

    scale.domain = domain_func
    scale.range = range_func
    scale.range_round = range_round_func
    scale.round = round_func
    scale.clamp = clamp_func
    scale.unknown = unknown_func
    scale.copy = copy

    init_range(scale)

    return linearish(scale)


# -----

