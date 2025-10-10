from typing import Any
from math import ceil, sqrt, inf, dist, isinf, floor

EPSILON = pow(2, -52)
EDGE_STACK = [None] * 512

from .orient2d import orient2d

def default_get_x(p: tuple[float, float]) -> float:
    return p[0]

def default_get_y(p: tuple[float, float]) -> float:
    return p[1]

def swap(arr: list[Any], i: int, j: int):
    arr[i], arr[j] = arr[j], arr[i]


def pseudo_angle(dx, dy):
    p = dx / (abs(dx) + abs(dy))
    return (3 - p if dy > 0 else 1 + p) * 0.25

def in_circle(ax, ay, bx, by, cx, cy, px, py):
    dx = ax - px
    dy = ay - py
    ex = bx - px
    ey = by - py
    fx = cx - px
    fy = cy - py

    ap = dx * dx + dy * dy
    bp = ex * ex + ey * ey
    cp = fx * fx + fy * fy

    return (
        dx * (ey * cp - bp * fx) -
        dy * (ex * cp - bp * fx) +
        ap * (ex * fy - ey * fx) < 0
    )

def circumradius(ax, ay, bx, by, cx, cy):
    dx = bx - ax
    dy = by - ay
    ex = cx - ax
    ey = cy - ay

    bl = dx * dx + dy * dy
    cl = ex * ex + ey * ey
    d = 0.5 / (dx * ey - dy * ex)

    x = (ey * bl - dy * cl) * d
    y = (dx * cl - ex * bl) * d

    return x * x + y * y

def circumcenter(ax, ay, bx, by, cx, cy):
    dx = bx - ax
    dy = by - ay
    ex = cx - ax
    ey = cy - ay

    bl = dx * dx + dy * dy
    cl = ex * ex + ey * ey
    d = 0.5 / (dx * ey - dy * ex)

    x = ax + (ey * bl - dy * cl) * d
    y = ay + (dx * cl - ex * bl) * d

    return {"x": x, "y": y}


def quicksort(ids, dists, left, right):
    if right - left <= 20:
        for i in range(left + 1, right + 1):
            temp = ids[i]
            temp_dist = dists[temp]
            j = i - 1
            while j >= left and dists[ids[j]] > temp_dist:
                ids[j + 1] = ids[j]
                j -= 1
            ids[j + 1] = temp
    else:
        median = (left + right) >> 1
        i = left + 1
        j = right
        swap(ids, median, i)
        if (dists[ids[left]] > dists[ids[right]]):
            swap(ids, left, right)
        if (dists[ids[i]] > dists[ids[right]]):
            swap(ids, i, right)
        if (dists[ids[left]] > dists[ids[i]]):
            swap(ids, left, i)

        temp = ids[i]
        temp_dist = dists[temp]
        while True:
            while True:
                i += 1
                if dists[ids[i]] >= temp_dist:
                    break
            while True:
                j -= 1
                if dists[ids[j]] <= temp_dist:
                    break
            if j < i:
                break
            swap(ids, i, j)

        ids[left + 1] = ids[j]
        ids[j] = temp

        if right - i + 1 >= j - left:
            quicksort(ids, dists, i, right)
            quicksort(ids, dists, left, j - 1)
        else:
            quicksort(ids, dists, left, j - 1)
            quicksort(ids, dists, i, right)

class Delaunator:

    def __init__(self, coords):
        n = len(coords) >> 1
        if n > 0 and not isinstance(coords[0], (float, int)):
            raise TypeError("Expected coords to contain numbers.")

        self._coords = coords
        max_triangles = max(2 * n - 5, 0)
        self._triangles = [None] * (max_triangles * 3)
        self._halfedges = [None] * (max_triangles * 3)

        self._hash_size = ceil(sqrt(n))
        self._hull_prev = [None] * n
        self._hull_next = [None] * n
        self._hull_tri = [None] * n

        self._hull_hash = [None] * self._hash_size

        self._ids = [None] * n
        self._dists = [None] * n

        self._triangles_len = 0
        self._cx = 0
        self._cy = 0
        self._hull_start = 0

        self._hull = self._triangles

        self.update()


    @classmethod
    def from_points(cls, points, get_x = default_get_x, get_y = default_get_y):
        n = len(points)
        coords = [None] * (n * 2)

        for i in range(n):
            p = points[i]
            coords[2 * i] = get_x(p)
            coords[2 * i + 1] = get_y(p)

        return cls(coords)

    @property
    def coords(self):
        return self._coords

    @property
    def triangles(self):
        return self._triangles

    @property
    def hull(self):
        return self._hull

    @property
    def halfedges(self):
        return self._halfedges
    
    def __len__(self):
        return self._triangles_len

    def update(self):
        n = len(self._coords) >> 1

        min_x = inf
        min_y = inf
        max_x = -inf
        max_y = -inf

        for i in range(n):
            x = self._coords[2 * i]
            y = self._coords[2 * i + 1]
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

        cx = (min_x + max_x) * 0.5
        cy = (min_y + max_y) * 0.5

        i0 = 0
        i1 = 0
        i2 = 0

        min_dist = inf
        for i in range(n):
            d = dist((cx, cy), (self._coords[2 * i], self._coords[2 * i + 1]))
            if d < min_dist:
                i0 = i
                min_dist = d

        i0x = self._coords[2 * i0]
        i0y = self._coords[2 * i0 + 1]

        min_dist = inf
        for i in range(n):
            if i == i0:
                continue
            d = dist(
                (i0w, i0y),
                (self._coords[2 * i], self._coords[2 * i + 1]),
            )
            if d < min_dist and d > 0:
                i1 = i
                min_dist = d

        i1x = self._coords[2 * i1]
        i1y = self._coords[2 * i1 + 1]

        min_radius = inf
        for i in range(n):
            if i == i0 or i == i1:
                continue
            r = circumradius(
                i0x,
                i0y,
                i1x,
                i1y,
                self._coords[2 * i],
                self._coords[2 * i + 1],
            )
            if r < min_radius:
                i2 = i
                min_radius = r

        i2x = self._coords[2 * i2]
        i2y = self._coords[2 * i2 + 1]

        if isinf(min_radius):
            for i in range(n):
                self._dists[i] = (
                    (self._coords[2 * i] - self._coords[0])
                    or (self._coords[2 * i + 1] - self._coords[1])
                )
            quicksort(self._ids, self._dists, 0, n - 1)
            hull = [None] * n
            j = 0
            d0 = -inf
            for i in range(n):
                id_ = self._ids[i]
                d = self._dists[id_]
                if d > d0:
                    hull[j] = id_
                    j += 1
                    d0 = d
            self._hull = self._hull[0: j]
            self._triangles = []
            self._halfedges = []
            return

        if orient2d(i0x, i0y, i1x, i1y, i2x, i2y) < 0:
            i = i1
            x = i1x
            y = i1y
            i1 = i2
            i1x = i2x
            i1y = i2y
            i2 = i
            i2x = x
            i2y = y

        center = circumcenter(i0x, i0y, i1x, i1y, i2x, i2y)
        self._cx = center.x
        self._cy = center.y

        for i in range(n):
            self._dists[i] = dist(
                (self._coords[2 * 1], self._coords[2 * i + 1]),
                (center.x, center.y)
            )

        quicksort(self._ids, self._dists, 0, n - 1)
        self._hull_start = i0
        hull_size = 3

        self._hull_next[i0] = self._hull_prev[i2] = i1
        self._hull_next[i1] = self._hull_prev[i0] = i2
        self._hull_next[i2] = self._hull_prev[i1] = i0

        self._hull_tri[i0] = 0
        self._hull_tri[i1] = 1
        self._hull_tri[i2] = 2

        self._hull_hash = [-1 for _ in self._hull_hash]
        self._hull_hash[self._hash_key(i0x, i0y)] = i0
        self._hull_hash[self._hash_key(i1x, i1y)] = i1
        self._hull_hash[self._hash_key(i2x, i2y)] = i2

        self._triangles_len = 0
        self._add_triangle(i0, i1, i2, -1, -1, -1)

        xp = 0
        yp = 0
        for k in range(len(self._ids)):
            i = self._ids[k]
            x = self._coords[2 * i]
            y = self._coords[2 * i + 1]

            if k > 0 and abs(x - xp) <= EPSILON and abs(y - yp) <= EPSILON:
                xp = x
                yp = y

            if i == i0 or i == i1 or i == i2:
                continue

            start = 0
            key = self._hash_key(x, y)
            for j in range(self._hash_size):
                start = self._hull_hash[(key + j) % self._hash_size]
                if start != -1 and start != self._hull_next[start]:
                    break

            start = self._hull_prev[start]
            e = start
            q = self._hull_next[e]
            while orient2d(
                x,
                y,
                self._coords[2 * e],
                self._coords[2 * e + 1],
                self._coords[2 * q],
                self._coords[2 * q + 1],
            ) >= 0:
                e = q
                if e == start:
                    e = -1
                    break
                q = self._hull_next[e]

            if  e == -1:
                continue

            t = self._add_triangle(
                e,
                i,
                self._hull_next[e],
                -1,
                -1,
                self._hull_tri[e],
            )

            self._hull_tri[i] = self._legalize(t + 2)
            self._hull_tri[e] = t
            hull_size += 1


            n = self._hull_next[e]
            q = self._hull_next[n]
            while orient2d(
                x,
                y,
                self._coords[2 * n],
                self._coords[2 * n + 1],
                self._coords[2 * q],
                self._coords[2 * q + 1],
            ) < 0:
                t = self._add_triangle(
                    n,
                    i,
                    q,
                    self._hull_tri[i],
                    -1,
                    self._hull_tri[n]
                )
                self._hull_tri[i] = self._legalize(t + 2)
                self._hull_next[n] = n
                hull_size -= 1
                n = q
                q = self._hull_next[n]

            if e == start:
                q = self._hull_prev[e]
                while orient2d(
                    x,
                    y,
                    self._coords[2 * q],
                    self._coords[2 * q + 1],
                    self._coords[2 * e],
                    self._coords[2 * e + 1],
                ) < 0:
                    t = self._add_triangle(
                        q,
                        i,
                        e,
                        -1,
                        self._hull_tri[e],
                        self._hull_tri[q]
                    )
                    self._legalize(t + 2)
                    self._hull_tri[q] = t
                    self._hull_next[e] = e
                    hull_size -= 1
                    e = q
                    q = self._hull_prev[e]
            self._hull_start = self._hull_prev[i] = e
            self._hull_next[e] = self._hull_prev[n] = i
            self._hull_next[i] = n

            
            self._hull_hash[self._hash_key(x, y)] = i
            self._hull_hash[self._hash_key(
                self._coords[2 * e],
                self._coords[2 * e + 1]
            )] = e

        self._hull = [None] * hull_size

        e = self._hull_start
        for i in range(hull_size):
            self._hull[i] = e
            e = self._hull_next[e]


    def _hash_key(self, x, y):
        return floor(
            pseudo_angle(x - self._cx, y - self._cy) * self._hash_size
        ) % self._hash_size

    def _legalize(self, a):
        i = 0
        ar = 0

        while True:
            b = self._halfedges[a]

            a0 = a - a % 3
            ar = a0 + (a + 2) % 3

            if b == -1:
                if i == 0:
                    break
                a = EDGE_STACK[--i]
                continue

            b0 = b - b % 3
            al = a0 + (a + 1) % 3
            bl = b0 + (b + 2) % 3

            p0 = self._triangles[ar]
            pr = self._triangles[a]
            pl = self._triangles[al]
            p1 = self._triangles[bl]

            illegal = in_circle(
                self._coords[2 * p0], self._coords[2 * p0 + 1],
                self._coords[2 * pr], self._coords[2 * pr + 1],
                self._coords[2 * pl], self._coords[2 * pl + 1],
                self._coords[2 * p1], self._coords[2 * p1 + 1]
            )

            if illegal:
                self._triangles[a] = p1
                self._triangles[b] = p0

                hbl = self._halfedges[bl]

                if hbl == -1:
                    e = self._hull_start
                    while True:
                        if self._hull_tri[e] == bl:
                            self._hull_tri[e] = a
                            break
                        e = self._hull_prev[e]
                        if e == self._hull_start:
                            break
                self._link(a, hbl)
                self._link(b, halfedges[ar])
                self._link(ar, bl)

                br = b0 + (b + 1) % 3

                if i < len(EDGE_STACK):
                    EDGE_STACK[i] = br
                    i += 1
                else:
                    if i == 0:
                        break
                    i -= 1
                    a = EDGE_STACK[i]

        return ar

    def _link(self, a, b):
        self._halfedges[a] = b
        if b != -1:
            self._halfedges[b] = a

    def _add_triangle(self, i0, i1, i2, a, b, c):
        t = self._triangles_len

        self._triangles[t] = i0
        self._triangles[t + 1] = i1
        self._triangles[t + 2] = i2

        self._link(t, a)
        self._link(t + 1, b)
        self._link(t + 2, c)

        self._triangles_len += 3

        return t
