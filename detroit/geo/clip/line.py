from math import copysign, inf


def clip_line(
    ax: float,
    ay: float,
    bx: float,
    by: float,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
) -> tuple[float, float, float, float] | None:
    t0 = 0
    t1 = 1
    dx = bx - ax
    dy = by - ay

    r = x0 - ax
    if not dx and r > 0:
        return None
    try:
        r = r / dx
    except ZeroDivisionError:
        r = copysign(r, 0) * inf
    if dx < 0:
        if r < t0:
            return None
        if r < t1:
            t1 = r
    elif dx > 0:
        if r > t1:
            return None
        if r > t0:
            t0 = r

    r = x1 - ax
    if not dx and r < 0:
        return None
    try:
        r = r / dx
    except ZeroDivisionError:
        r = copysign(r, 0) * inf
    if dx < 0:
        if r > t1:
            return None
        if r > t0:
            t0 = r
    elif dx > 0:
        if r < t0:
            return None
        if r < t1:
            t1 = r

    r = y0 - ay
    if not dy and r > 0:
        return None
    try:
        r = r / dy
    except ZeroDivisionError:
        r = copysign(r, 0) * inf
    if dy < 0:
        if r < t0:
            return None
        if r < t1:
            t1 = r
    elif dy > 0:
        if r > t1:
            return None
        if r > t0:
            t0 = r

    r = y1 - ay
    if not dy and r < 0:
        return None
    try:
        r = r / dy
    except ZeroDivisionError:
        r = copysign(r, 0) * inf
    if dy < 0:
        if r > t1:
            return None
        if r > t0:
            t0 = r
    elif dy > 0:
        if r < t0:
            return None
        if r < t1:
            t1 = r

    x1 = ax
    y1 = ay
    x2 = bx
    y2 = by
    if t0 > 0:
        x1 = ax + t0 * dx
        y1 = ay + t0 * dy
    if t1 < 1:
        x2 = ax + t1 * dx
        y2 = ay + t1 * dy
    return x1, y1, x2, y2
