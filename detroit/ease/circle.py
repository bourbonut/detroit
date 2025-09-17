from math import sqrt

def ease_circle_in(t: float) -> float:
    return 1 - sqrt(1 - t * t)

def ease_circle_out(t: float) -> float:
    t -= 1
    return sqrt(1 - t * t)

def ease_circle_in_out(t: float) -> float:
    t *= 2
    if t <= 1:
        return (1 - sqrt(1 - t * t)) * 0.5
    else:
        t -= 2
        return (sqrt(1 - t * t) + 1) * 0.5
