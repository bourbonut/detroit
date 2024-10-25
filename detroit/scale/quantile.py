from bisect import bisect
from ..array import ascending, quantileSorted as threshold # TODO
from .init import init_range

def quantile():
    domain = []
    range_vals = []
    thresholds = []
    unknown = None

    def rescale():
        nonlocal thresholds
        n = max(1, len(range_vals))
        thresholds = [None] * (n - 1)
        for i in range(1, n):
            thresholds[i - 1] = threshold(domain, i / n)
        return scale

    def scale(x):
        return unknown if x is None or (isinstance(x, float) and math.isnan(x)) else range_vals[bisect(thresholds, x)]

    def invert_extent(y):
        i = range_vals.index(y)
        return [None, None] if i < 0 else [
            thresholds[i - 1] if i > 0 else domain[0],
            thresholds[i] if i < len(thresholds) else domain[-1]
        ]

    def domain_func(_=None):
        if _ is None:
            return domain.copy()
        domain.clear()
        for d in _:
            if d is not None and not (isinstance(d, float) and math.isnan(d)):
                domain.append(d)
        domain.sort(ascending)
        return rescale()

    def range_func(_=None):
        if _ is not None:
            range_vals[:] = list(_)
            return rescale()
        return range_vals.copy()

    def unknown_func(_=None):
        nonlocal unknown
        if _ is not None:
            unknown = _
            return scale
        return unknown

    def quantiles_func():
        return thresholds.copy()

    def copy():
        return quantile().domain(domain).range(range_vals).unknown(unknown)

    scale.invert_extent = invert_extent
    scale.domain = domain_func
    scale.range = range_func
    scale.unknown = unknown_func
    scale.quantiles = quantiles_func
    scale.copy = copy

    return init_range(scale)


# -----

