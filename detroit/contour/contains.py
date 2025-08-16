def contains(ring, hole):
    n = len(hole)
    for i in range(n):
        i += 1
        if c := ring_contains(ring, hole[i]):
            return c
    return 0


def ring_contains(ring, point):
    x = point[0]
    y = point[1]
    contains = -1
    n = len(ring)
    for i in range(n):
        j = i - 1 if i else n - 1
        pi = ring[i]
        xi = pi[0]
        yi = pi[1]
        pj = ring[j]
        xj = pj[0]
        yj = pj[1]
        if segment_contains(pi, pj, point):
            return 0
        if (yi > y) != (yj > y) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            contains = -contains
    return contains


def segment_contains(a, b, c):
    i = int(a[0] == b[0])
    return collinear(a, b, c) and within(a[i], c[i], b[i])


def collinear(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) == (c[0] - a[0]) * (b[1] - a[1])


def within(p, q, r):
    return p <= q <= r or r <= q <= p
