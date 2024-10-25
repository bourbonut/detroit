from ..array import ascending, bisect, quantile
from .continuous import identity
from .init import init_interpolator

def sequential_quantile():
    domain = []
    interpolator = identity

    def scale(x):
        return interpolator((bisect(domain, x, 1) - 1) / (len(domain) - 1)) if x is not None and not (isinstance(x, float) and math.isnan(x)) else None

    def domain_func(_=None):
        if _ is None:
            return domain.copy()
        domain.clear()
        for d in _:
            if d is not None and not (isinstance(d, float) and math.isnan(d)):
                domain.append(d)
        domain.sort(ascending)
        return scale

    def interpolator_func(_=None):
        if _ is not None:
            interpolator = _
            return scale
        return interpolator

    def range_func():
        return [interpolator(i / (len(domain) - 1)) for i in range(len(domain))]

    def quantiles_func(n):
        return [quantile(domain, i / n) for i in range(n + 1)]

    def copy():
        return sequential_quantile().domain(domain)

    scale.domain = domain_func
    scale.interpolator = interpolator_func
    scale.range = range_func
    scale.quantiles = quantiles_func
    scale.copy = copy

    return init_interpolator(scale)


# -----

