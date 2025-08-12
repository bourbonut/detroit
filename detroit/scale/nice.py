from ..types import Interval, T


def nice(domain: list[T], interval: Interval) -> list[T]:
    domain = domain.copy()

    i0 = 0
    i1 = len(domain) - 1
    x0 = domain[i0]
    x1 = domain[i1]
    t = None

    if x1 < x0:
        t = i0
        i0 = i1
        i1 = t
        t = x0
        x0 = x1
        x1 = t

    domain[i0] = interval.floor(x0)
    domain[i1] = interval.ceil(x1)
    return domain
