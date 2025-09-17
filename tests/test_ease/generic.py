from collections.abc import Callable

def out(ease_in: Callable[[float], float]) -> Callable[[float], float]:
    return lambda t: 1 - ease_in(1 - t)

def in_out(ease_in: Callable[[float], float]) -> Callable[[float], float]:
    return lambda t: (
        ease_in(t * 2) if t < 0.5  else (2 - ease_in((1 - t) * 2))
    ) * 0.5
