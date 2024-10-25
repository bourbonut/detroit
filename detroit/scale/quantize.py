from bisect import bisect
from .linear import linearish
from .init import init_range

def quantize():
    x0 = 0
    x1 = 1
    n = 1
    domain = [0.5]
    range_vals = [0, 1]
    unknown = None

    def scale(x):
        return range_vals[bisect(domain, x, 0, n)] if x is not None and x <= x else unknown

    def rescale():
        nonlocal domain
        domain = [(i + 1) * x1 - (i - n) * x0 / (n + 1) for i in range(n)]
        return scale

    def domain_func(_=None):
        return (x0, x1) if _ is None else (x0 := float(_[0]), x1 := float(_[1]), rescale())

    def range_func(_=None):
        return range_vals.copy() if _ is None else (n := (range_vals := list(_)).length - 1, rescale())

    def invert_extent(y):
        i = range_vals.index(y)
        return [None, None] if i < 0 else [
            domain[i - 1] if i > 0 else x0,
            domain[i] if i < n else x1
        ]

    def unknown_func(_=None):
        nonlocal unknown
        return unknown if _ is None else (unknown := _, scale)

    def thresholds_func():
        return domain.copy()

    def copy_func():
        return quantize().domain([x0, x1]).range(range_vals).unknown(unknown)

    scale.domain = domain_func
    scale.range = range_func
    scale.invert_extent = invert_extent
    scale.unknown = unknown_func
    scale.thresholds = thresholds_func
    scale.copy = copy_func

    return init_range(linearish(scale))


# -----

