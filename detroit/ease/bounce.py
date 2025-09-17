B1 = 4 / 11
B2 = 6 / 11
B3 = 8 / 11
B4 = 3 / 4
B5 = 9 / 11
B6 = 10 / 11
B7 = 15 / 16
B8 = 21 / 22
B9 = 63 / 64
B0 = 1 / B1 / B1

def ease_bounce_in(t: float) -> float:
    return 1 - ease_bounce_out(1 - t)

def ease_bounce_out(t: float) -> float:
    if t < B1:
        return B0 * t * t
    elif t < B3:
        t -= B2
        return B0 * t * t + B4
    elif t < B6:
        t -= B5
        return B0 * t * t + B7
    else:
        t -= B8
        return B0 * t * t + B9

def ease_bounce_in_out(t: float) -> float:
    t *= 2
    if t <= 1:
        return (1 - ease_bounce_out(1 - t)) * 0.5
    else:
        return (ease_bounce_out(t - 1) + 1) * 0.5
