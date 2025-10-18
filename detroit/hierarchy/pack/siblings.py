from math import sqrt

from .enclose import Circle, pack_enclose_random


def place(b: Circle, a: Circle, c: Circle):
    dx = b.x - a.x
    dy = b.y - a.y
    d2 = dx * dx + dy * dy
    if d2:
        a2 = a.r + c.r
        a2 *= a2
        b2 = b.r + c.r
        b2 *= b2
        if a2 > b2:
            x = (d2 + b2 - a2) / (2 * d2)
            y = sqrt(max(0, b2 / d2 - x * x))
            c.x = b.x - x * dx - y * dy
            c.y = b.y - x * dy + y * dx
        else:
            x = (d2 + a2 - b2) / (2 * d2)
            y = sqrt(max(0, a2 / d2 - x * x))
            c.x = a.x + x * dx - y * dy
            c.y = a.y + x * dy + y * dx
    else:
        c.x = a.x + c.r
        c.y = a.y


def intersects(a: Circle, b: Circle) -> bool:
    dr = a.r + b.r - 1e-6
    dx = b.x - a.x
    dy = b.y - a.y
    return dr > 0 and dr * dr > dx * dx + dy * dy


class Node:
    def __init__(self, circle: Circle):
        self.circle = circle
        self.next = None
        self.previous = None


def score(node: Node) -> float:
    a = node.circle
    b = node.next.circle
    ab = a.r + b.r
    dx = (a.x * b.r + b.x * a.r) / ab
    dy = (a.y * b.r + b.y * a.r) / ab
    return dx * dx + dy * dy


def pack_siblings_random(circles: list[Circle]) -> float:
    circles = list(circles)
    n = len(circles)
    if n == 0:
        return 0

    a = circles[0]
    a.x = 0
    a.y = 0
    if n <= 1:
        return a.r

    b = circles[1]
    a.x = -b.r
    b.x = a.r
    b.y = 0

    if n <= 2:
        return a.r + b.r

    c = circles[2]
    place(b, a, c)
    a = Node(a)
    b = Node(b)
    c = Node(c)
    a.next = c.previous = b
    b.next = a.previous = c
    c.next = b.previous = a

    i = 3
    while i < n:
        continue_main = False
        c = circles[i]
        place(a.circle, b.circle, c)
        c = Node(c)

        j = b.next
        k = a.previous
        sj = b.circle.r
        sk = a.circle.r
        while True:
            if sj <= sk:
                if intersects(j.circle, c.circle):
                    b = j
                    a.next = b
                    b.previous = a
                    continue_main = True
                    break
                sj += j.circle.r
                j = j.next
            else:
                if intersects(k.circle, c.circle):
                    a = k
                    a.next = b
                    b.previous = a
                    continue_main = True
                    break
                sk += k.circle.r
                k = k.previous
            if j == k.next:
                break

        if continue_main:
            continue

        c.previous = a
        c.next = b
        a.next = b.previous = b = c

        aa = score(a)
        c = c.next
        while c != b:
            ca = score(c)
            if ca < aa:
                a = c
                aa = ca
            c = c.next
        b = a.next
        i += 1

    a = [b.circle]
    c = b

    c = c.next
    while c != b:
        a.append(c.circle)
        c = c.next
    c = pack_enclose_random(a)

    for circle in circles:
        a = circle
        a.x -= c.x
        a.y -= c.y

    return c.r


def pack_siblings(circles: list[Circle]) -> list[Circle]:
    """
    Packs the specified array of circles, each of which must have a
    :code:`circle.r` property specifying the circle's radius. Assigns the
    following properties to each circle:

    * :code:`circle.x` - the x-coordinate of the circle's center
    * :code:`circle.y` - the y coordinate of the circle's center

    The circles are positioned according to the front-chain packing algorithm
    by `Wang et al <https://dl.acm.org/doi/10.1145/1124772.1124851>`_.

    Parameters
    ----------
    circles : list[Circle]
        List of circles

    Returns
    -------
    list[Circle]
        Packed list of circles
    """
    pack_siblings_random(circles)
    return circles
