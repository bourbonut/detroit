from collections.abc import Callable

from ..types import U, V
from .object_to_value import interpolate as interpolate_value


def piecewise(
    interpolate: Callable[[U, U], Callable[[float], V]],
    values: list[U] | None = None,
) -> Callable[[float], V]:
    if values is None:
        values = interpolate
        interpolate = interpolate_value

    n = len(values) - 1
    I = [interpolate(values[i], values[i + 1]) for i in range(n)]

    def local_interpolate(t):
        i = max(0, min(n - 1, int(t * n)))
        return I[i](t * n - i)

    return local_interpolate
