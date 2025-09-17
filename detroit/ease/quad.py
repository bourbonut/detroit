def ease_quad_in(t: float) -> float:
    return t * t

def ease_quad_out(t: float) -> float:
    return t * (2 - t)

def ease_quad_in_out(t: float) -> float:
    t *= 2
    if t <= 1:
        return t * t * 0.5
    else:
        t -= 1
        return (t * (2 - t) + 1) * 0.5
