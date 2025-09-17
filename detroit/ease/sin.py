from math import pi, cos, sin

HALF_PI = pi * 0.5

def ease_sin_in(t: float) -> float:
    if t == 1:
        return 1
    else:
        return 1 - cos(t * HALF_PI)

def ease_sin_out(t: float) -> float:
    return sin(t * HALF_PI)

def ease_sin_in_out(t: float) -> float:
    return (1 - cos(pi * t)) * 0.5
