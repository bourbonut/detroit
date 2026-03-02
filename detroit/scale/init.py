from collections.abc import Callable

from ..types import U, V
from .abc import ContinuousScaler, SequentialScaler


def init_range(
    obj: ContinuousScaler[U, V],
    domain: list[U] | None = None,
    range_vals: list[V] | None = None,
):
    if domain is None and range_vals is None:
        return obj
    elif domain is None:
        return obj.set_range(range_vals)
    return obj.set_range(range_vals).set_domain(domain)


def init_interpolator(
    obj: SequentialScaler[U, V],
    domain: list[U] | None = None,
    interpolator: Callable[[V], V] | None = None,
):
    if domain is None and interpolator is None:
        return obj
    elif domain is None:
        if callable(interpolator):
            obj.set_interpolator(interpolator)
        else:
            obj.set_range(interpolator)
    else:
        obj.set_domain(domain)
        if callable(interpolator):
            obj.set_interpolator(interpolator)
        else:
            obj.set_range(domain)
    return obj
