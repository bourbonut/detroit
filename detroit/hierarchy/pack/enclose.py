from math import sqrt
from random import shuffle
from typing import Any


class Circle:
    def __init__(self, x: float, y: float, r: float):
        self.x = x
        self.y = y
        self.r = r

    @classmethod
    def from_other(cls, circle: Any):
        return cls(
            x=circle.get("x") if isinstance(circle, dict) else circle.x,
            y=circle.get("y") if isinstance(circle, dict) else circle.y,
            r=circle.get("r") if isinstance(circle, dict) else circle.r,
        )


def pack_enclose_random(circles: list[dict[str, float]]) -> Circle:
    """
    Computes the smallest circle that encloses the specified array of circles,
    each of which must have a :code:`circle.r` property specifying the circle's
    radius, and :code:`circle.x` and :code:`circle.y` properties specifying the
    circle's center. The enclosing circle is computed using the
    `Matoušek-Sharir-Welzl algorithm \
    <https://people.inf.ethz.ch/emo/PublFiles/SubexLinProg_ALG16_96.pdf>`_.
    (See also `Apollonius' \
    Problem <https://observablehq.com/@d3/apollonius-problem>`_.)

    Parameters
    ----------
    circles : list[dict[str, float]]
        List of circles defined as dictionaries such as :code:`circle = {"x":
        ..., "y": ..., "r": ...}`

    Returns
    -------
    Circle
        Smallest circle that enclosed the specified array of circles
    """
    i = 0
    circles = [Circle.from_other(circle) for circle in circles]
    shuffle(circles)
    n = len(circles)
    basis = []
    e = None
    while i < n:
        p = circles[i]
        if e and encloses_weak(e, p):
            i += 1
        else:
            basis = extend_basis(basis, p)
            e = enclose_basis(basis)
            i = 0
    return e


def extend_basis(basis: list[Circle], p: Circle):
    if encloses_weak_all(p, basis):
        return [p]

    for i in range(len(basis)):
        if encloses_not(p, basis[i]) and encloses_weak_all(
            enclose_basis_2(basis[i], p), basis
        ):
            return [basis[i], p]

    for i in range(len(basis) - 1):
        for j in range(i + 1, len(basis)):
            if (
                encloses_not(enclose_basis_2(basis[i], basis[j]), p)
                and encloses_not(enclose_basis_2(basis[i], p), basis[j])
                and encloses_not(enclose_basis_2(basis[j], p), basis[i])
                and encloses_weak_all(enclose_basis_3(basis[i], basis[j], p), basis)
            ):
                return [basis[i], basis[j], p]

    raise RuntimeError("This error should not be raised.")


def encloses_not(a: Circle, b: Circle) -> bool:
    dr = a.r - b.r
    dx = b.x - a.x
    dy = b.y - a.y
    return dr < 0 or dr * dr < dx * dx + dy * dy


def encloses_weak(a: Circle, b: Circle) -> bool:
    dr = a.r - b.r + max(a.r, b.r, 1) * 1e-9
    dx = b.x - a.x
    dy = b.y - a.y
    return dr > 0 and dr * dr > dx * dx + dy * dy


def encloses_weak_all(a: Circle, basis: list[Circle]) -> bool:
    for i in range(len(basis)):
        if not encloses_weak(a, basis[i]):
            return False
    return True


def enclose_basis(basis: list[Circle]) -> Circle:
    match len(basis):
        case 1:
            return enclose_basis_1(basis[0])
        case 2:
            return enclose_basis_2(basis[0], basis[1])
        case 3:
            return enclose_basis_3(basis[0], basis[1], basis[2])


def enclose_basis_1(a: Circle) -> Circle:
    return Circle(a.x, a.y, a.r)


def enclose_basis_2(a: Circle, b: Circle) -> Circle:
    x1 = a.x
    y1 = a.y
    r1 = a.r
    x2 = b.x
    y2 = b.y
    r2 = b.r
    x21 = x2 - x1
    y21 = y2 - y1
    r21 = r2 - r1
    length = sqrt(x21 * x21 + y21 * y21)
    return Circle(
        (x1 + x2 + x21 / length * r21) * 0.5,
        (y1 + y2 + y21 / length * r21) * 0.5,
        (length + r1 + r2) * 0.5,
    )


def enclose_basis_3(a: Circle, b: Circle, c: Circle) -> Circle:
    x1 = a.x
    y1 = a.y
    r1 = a.r
    x2 = b.x
    y2 = b.y
    r2 = b.r
    x3 = c.x
    y3 = c.y
    r3 = c.r
    a2 = x1 - x2
    a3 = x1 - x3
    b2 = y1 - y2
    b3 = y1 - y3
    c2 = r2 - r1
    c3 = r3 - r1
    d1 = x1 * x1 + y1 * y1 - r1 * r1
    d2 = d1 - x2 * x2 - y2 * y2 + r2 * r2
    d3 = d1 - x3 * x3 - y3 * y3 + r3 * r3
    ab = a3 * b2 - a2 * b3
    xa = (b2 * d3 - b3 * d2) / (ab * 2) - x1
    xb = (b3 * c2 - b2 * c3) / ab
    ya = (a3 * d2 - a2 * d3) / (ab * 2) - y1
    yb = (a2 * c3 - a3 * c2) / ab
    A = xb * xb + yb * yb - 1
    B = 2 * (r1 + xa * xb + ya * yb)
    C = xa * xa + ya * ya - r1 * r1
    r = -((B + sqrt(B * B - 4 * A * C)) / (2 * A) if abs(A) > 1e-6 else C / B)
    return Circle(x1 + xa + xb * r, y1 + ya + yb * r, r)
