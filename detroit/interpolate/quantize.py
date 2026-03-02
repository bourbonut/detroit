from collections.abc import Callable


def quantize(interpolator: Callable[[float], float], n: int) -> list[float]:
    return [interpolator(i / (n - 1)) for i in range(n)]
