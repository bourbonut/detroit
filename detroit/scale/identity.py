from .linear import linearish
from .number import number

def identity(domain=None):
    unknown = None

    def scale(x):
        return unknown if x is None or (isinstance(x, float) and math.isnan(x)) else x

    scale.invert = scale

    def domain_func(_=None):
        return domain if _ is None else (domain := list(map(float, _)), scale)

    scale.domain = scale.range = domain_func

    def unknown_func(_=None):
        nonlocal unknown
        return unknown if _ is None else (unknown := _, scale)

    scale.unknown = unknown_func

    def copy_func():
        return identity(domain).unknown(unknown)

    scale.copy = copy_func

    domain = list(map(float, domain)) if domain is not None else [0, 1]

    return linearish(scale)
