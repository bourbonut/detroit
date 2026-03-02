from collections.abc import Callable


def constant(x: float) -> Callable[[float], float]:
    def f(*args):
        return x

    return f
