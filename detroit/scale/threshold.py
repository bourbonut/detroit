from bisect import bisect
from .init import init_range

def threshold():
    domain = [0.5]
    range_vals = [0, 1]
    unknown = None
    n = 1

    def scale(x):
        return range_vals[bisect(domain, x, 0, n)] if x is not None and x <= x else unknown

    def domain_func(_=None):
        nonlocal domain, n
        if _ is not None:
            domain = list(_)
            n = min(len(domain), len(range_vals) - 1)
            return scale
        return domain.copy()

    def range_func(_=None):
        nonlocal range_vals, n
        if _ is not None:
            range_vals = list(_)
            n = min(len(domain), len(range_vals) - 1)
            return scale
        return range_vals.copy()

    def invert_extent(y):
        i = range_vals.index(y)
        return [domain[i - 1], domain[i]]

    def unknown_func(_=None):
        nonlocal unknown
        if _ is not None:
            unknown = _
            return scale
        return unknown

    def copy():
        return threshold().domain(domain).range(range_vals).unknown(unknown)

    scale.domain = domain_func
    scale.range = range_func
    scale.invert_extent = invert_extent
    scale.unknown = unknown_func
    scale.copy = copy

    return init_range(scale)
