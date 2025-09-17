def ease_cubic_in(t: float) -> float:
    return t * t * t

def ease_cubic_out(t: float) -> float:
    t -= 1
    return t * t * t + 1

def ease_cubic_in_out(t: float) -> float:
    t *= 2
    if t <= 1:
        return (t * t * t) * 0.5
    else:
        t -= 2
        return (t * t * t + 2) * 0.5
