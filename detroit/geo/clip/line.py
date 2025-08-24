from ...types import Point2D
from math import inf

def sign(x: float) -> float:
    return -1 if x < 0 else 1

def clip_line(a: Point2D, b: Point2D, x0: float, y0: float, x1: float, y1: float) -> bool:
    ax = a[0]
    ay = a[1]
    bx = b[0]
    by = b[1]
    t0 = 0
    t1 = 1
    dx = bx - ax
    dy = by - ay

    r = x0 - ax
    if not dx and r > 0:
        return False
    r = r / dx if dx != 0. else sign(r) * inf
    if dx < 0:
        if r < t0:
            return False
        if r < t1:
            t1 = r
    elif dx > 0:
        if r > t1:
            return False
        if r > t0:
            t0 = r

    r = x1 - ax
    if not dx and r < 0:
        return False
    r = r / dx if dx != 0. else sign(r) * inf
    if dx < 0:
        if r > t1:
            return False
        if r > t0:
            t0 = r
    elif dx > 0:
        if r < t0:
            return False
        if r < t1:
            t1 = r

    r = y0 - ay
    if not dy and r > 0:
        return False
    r = r / dy if dy != 0. else sign(r) * inf
    if dy < 0:
        if r < t0:
            return False
        if r < t1:
            t1 = r
    elif dy > 0:
        if r > t1:
            return False
        if r > t0:
            t0 = r

    r = y1 - ay
    if not dy and r < 0:
        return False
    r = r / dy if dy != 0. else sign(r) * inf
    if dy < 0:
        if r > t1:
            return False
        if r > t0:
            t0 = r
    elif dy > 0:
        if r < t0:
            return False
        if r < t1:
            t1 = r

    if t0 > 0:
        a[0] = ax + t0 * dx
        a[1] = ay + t0 * dy
    if t1 < 1:
        b[0] = ax + t1 * dx
        b[1] = ay + t1 * dy
    return True
