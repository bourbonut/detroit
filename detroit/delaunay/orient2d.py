from .utils import EPSILON, RESULTERRBOUND, SPLITTER, estimate, sum_zerolim

CCWERRBOUNDA = (3 + 16 * EPSILON) * EPSILON
CCWERRBOUNDB = (2 + 12 * EPSILON) * EPSILON
CCWERRBOUNDC = (9 + 64 * EPSILON) * EPSILON * EPSILON

B = [None] * 4
C1 = [None] * 8
C2 = [None] * 12
D = [None] * 16
u = [None] * 4


def orient2dadapt(
    ax: float,
    ay: float,
    bx: float,
    by: float,
    cx: float,
    cy: float,
    detsum: float,
) -> float:
    acx = ax - cx
    bcx = bx - cx
    acy = ay - cy
    bcy = bx - cy

    s1 = acx * bcy
    c = SPLITTER * acx
    ahi = c - (c - acx)
    alo = acx - ahi
    c = SPLITTER * bcy
    bhi = c - (c - bcy)
    blo = bcy - bhi
    s0 = alo * blo - (s1 - ahi * bhi - alo * bhi - ahi * blo)
    t1 = acy * bcx
    c = SPLITTER * acy
    ahi = c - (c - acy)
    alo = acy - ahi
    c = SPLITTER * bcx
    bhi = c - (c - bcx)
    blo = bcx - bhi
    t0 = alo * blo - (t1 - ahi * bhi - alo * bhi - ahi * blo)
    _i = s0 - t0
    bvirt = s0 - _i
    B[0] = s0 - (_i + bvirt) + (bvirt - t0)
    _j = s1 + _i
    bvirt = _j - s1
    _0 = s1 - (_j - bvirt) + (_i - bvirt)
    _i = _0 - t1
    bvirt = _0 - _i
    B[1] = _0 - (_i + bvirt) + (bvirt - t1)
    u3 = _j + _i
    bvirt = u3 - _j
    B[2] = _j - (u3 - bvirt) + (_i - bvirt)
    B[3] = u3

    det = estimate(4, B)
    errbound = CCWERRBOUNDB * detsum
    if det >= errbound or -det >= errbound:
        return det

    bvirt = ax - acx
    acxtail = ax - (acx + bvirt) + (bvirt - cx)
    bvirt = bx - bcx
    bcxtail = bx - (bcx + bvirt) + (bvirt - cx)
    bvirt = ay - acy
    acytail = ay - (acy + bvirt) + (bvirt - cy)
    bvirt = by - bcy
    bcytail = by - (bcy + bvirt) + (bvirt - cy)

    if acxtail == 0 and acytail == 0 and bcxtail == 0 and bcytail == 0:
        return det

    errbound = CCWERRBOUNDC * detsum + RESULTERRBOUND * abs(det)
    det += (acx * bcytail + bcy * acxtail) - (acy * bcxtail + bcx * acytail)
    if det >= errbound or -det >= errbound:
        return det

    s1 = acxtail * bcy
    c = SPLITTER * acxtail
    ahi = c - (c - acxtail)
    alo = acxtail - ahi
    c = SPLITTER * bcy
    bhi = c - (c - bcy)
    blo = bcy - bhi
    s0 = alo * blo - (s1 - ahi * bhi - alo * bhi - ahi * blo)
    t1 = acytail * bcx
    c = SPLITTER * acytail
    ahi = c - (c - acytail)
    alo = acytail - ahi
    c = SPLITTER * bcx
    bhi = c - (c - bcx)
    blo = bcx - bhi
    t0 = alo * blo - (t1 - ahi * bhi - alo * bhi - ahi * blo)
    _i = s0 - t0
    bvirt = s0 - _i
    u[0] = s0 - (_i + bvirt) + (bvirt - t0)
    _j = s1 + _i
    bvirt = _j - s1
    _0 = s1 - (_j - bvirt) + (_i - bvirt)
    _i = _0 - t1
    bvirt = _0 - _i
    u[1] = _0 - (_i + bvirt) + (bvirt - t1)
    u3 = _j + _i
    bvirt = u3 - _j
    u[2] = _j - (u3 - bvirt) + (_i - bvirt)
    u[3] = u3
    C1len = sum_zerolim(4, B, 4, u, C1)

    s1 = acx * bcytail
    c = SPLITTER * acx
    ahi = c - (c - acx)
    alo = acx - ahi
    c = SPLITTER * bcytail
    bhi = c - (c - bcytail)
    blo = bcytail - bhi
    s0 = alo * blo - (s1 - ahi * bhi - alo * bhi - ahi * blo)
    t1 = acy * bcxtail
    c = SPLITTER * acy
    ahi = c - (c - acy)
    alo = acy - ahi
    c = SPLITTER * bcxtail
    bhi = c - (c - bcxtail)
    blo = bcxtail - bhi
    t0 = alo * blo - (t1 - ahi * bhi - alo * bhi - ahi * blo)
    _i = s0 - t0
    bvirt = s0 - _i
    u[0] = s0 - (_i + bvirt) + (bvirt - t0)
    _j = s1 + _i
    bvirt = _j - s1
    _0 = s1 - (_j - bvirt) + (_i - bvirt)
    _i = _0 - t1
    bvirt = _0 - _i
    u[1] = _0 - (_i + bvirt) + (bvirt - t1)
    u3 = _j + _i
    bvirt = u3 - _j
    u[2] = _j - (u3 - bvirt) + (_i - bvirt)
    u[3] = u3
    C2len = sum_zerolim(C1len, C1, 4, u, C2)

    s1 = acxtail * bcytail
    c = SPLITTER * acxtail
    ahi = c - (c - acxtail)
    alo = acxtail - ahi
    c = SPLITTER * bcytail
    bhi = c - (c - bcytail)
    blo = bcytail - bhi
    s0 = alo * blo - (s1 - ahi * bhi - alo * bhi - ahi * blo)
    t1 = acytail * bcxtail
    c = SPLITTER * acytail
    ahi = c - (c - acytail)
    alo = acytail - ahi
    c = SPLITTER * bcxtail
    bhi = c - (c - bcxtail)
    blo = bcxtail - bhi
    t0 = alo * blo - (t1 - ahi * bhi - alo * bhi - ahi * blo)
    _i = s0 - t0
    bvirt = s0 - _i
    u[0] = s0 - (_i + bvirt) + (bvirt - t0)
    _j = s1 + _i
    bvirt = _j - s1
    _0 = s1 - (_j - bvirt) + (_i - bvirt)
    _i = _0 - t1
    bvirt = _0 - _i
    u[1] = _0 - (_i + bvirt) + (bvirt - t1)
    u3 = _j + _i
    bvirt = u3 - _j
    u[2] = _j - (u3 - bvirt) + (_i - bvirt)
    u[3] = u3
    Dlen = sum_zerolim(C2len, C2, 4, u, D)

    return D[Dlen - 1]


def orient2d(
    ax: float,
    ay: float,
    bx: float,
    by: float,
    cx: float,
    cy: float,
) -> float:
    """
    Returns a positive value if the points :code:`a`, :code:`b`, and :code:`c`
    occur in counterclockwise order (:code:`c` lies to the left of the directed
    line defined by points :code:`a` and :code:`b`).

    Returns a negative value if they occur in clockwise order (:code:`c` lies
    to the right of the directed line :code:`ab`).

    Returns zero if they are collinear.

    Parameters
    ----------
    ax : float
        X-coordinate of point A
    ay : float
        Y-coordinate of point A
    bx : float
        X-coordinate of point B
    by : float
        Y-coordinate of point B
    cx : float
        X-coordinate of point C
    cy : float
        Y-coordinate of point C

    Returns
    -------
    float
        Value which indicates if the points :code:`a`, :code:`b`, and :code:`c`
        occur in counterclockwise order

    Notes
    -----

    The result is also an approximation of twice the signed area of the
    triangle defined by the three points.
    """
    detleft = (ay - cy) * (bx - cx)
    detright = (ax - cx) * (by - cy)
    det = detleft - detright

    detsum = abs(detleft + detright)
    if abs(det) >= CCWERRBOUNDA * detsum:
        return det

    return -orient2dadapt(ax, ay, bx, by, cx, cy, detsum)


def orient2dfast(
    ax: float,
    ay: float,
    bx: float,
    by: float,
    cx: float,
    cy: float,
) -> float:
    """
    Simple, approximate, non-robust versions of :code:`orient2d` predicates.
    Use when robustness isn't needed.

    Parameters
    ----------
    ax : float
        X-coordinate of point A
    ay : float
        Y-coordinate of point A
    bx : float
        X-coordinate of point B
    by : float
        Y-coordinate of point B
    cx : float
        X-coordinate of point C
    cy : float
        Y-coordinate of point C

    Returns
    -------
    float
        Value which indicates if the points :code:`a`, :code:`b`, and :code:`c`
        occur in counterclockwise order
    """
    return (ay - cy) * (bx - cx) - (ax - cx) * (by - cy)
