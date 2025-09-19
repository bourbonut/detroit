from collections.abc import Callable

def jiggle(random: Callable[[None], float]) -> float:
    return (random() - 0.5) * 1e-6
