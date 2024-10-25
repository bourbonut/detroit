from ..array import InternMap # TODO
from .init import init_range

implicit = object()

def ordinal():
    index = InternMap()
    domain = []
    range_vals = []
    unknown = implicit

    def scale(d):
        i = index.get(d)
        if i is None:
            if unknown != implicit:
                return unknown
            index.set(d, i := len(domain))
            domain.append(d)
        return range_vals[i % len(range_vals)]

    def domain_func(_=None):
        if _ is None:
            return domain.copy()
        domain.clear()
        index.clear()
        for value in _:
            if index.has(value):
                continue
            index.set(value, len(domain))
            domain.append(value)
        return scale

    def range_func(_=None):
        if _ is not None:
            range_vals[:] = list(_)
            return scale
        return range_vals.copy()

    def unknown_func(_=None):
        nonlocal unknown
        if _ is not None:
            unknown = _
            return scale
        return unknown

    def copy():
        return ordinal().domain(domain).range(range_vals).unknown(unknown)

    scale.domain = domain_func
    scale.range = range_func
    scale.unknown = unknown_func
    scale.copy = copy

    init_range(scale)

    return scale
