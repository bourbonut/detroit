from collections.abc import Callable
from typing import Any, TypeVar
from math import ceil, sqrt, inf, isinf, floor
from .orient2d import orient2d
from ..types import T

TDelaunator = TypeVar("Delaunator", bound="Delaunator")

EPSILON = pow(2, -52)
EDGE_STACK = [None] * 512

def default_get_x(p: tuple[float, float]) -> float:
    return p[0]

def default_get_y(p: tuple[float, float]) -> float:
    return p[1]

def swap(arr: list[Any], i: int, j: int):
    arr[i], arr[j] = arr[j], arr[i]

def pseudo_angle(dx: float, dy: float) -> float:
    p = dx / (abs(dx) + abs(dy))
    return (3 - p if dy > 0 else 1 + p) * 0.25

def dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    ax, ay = a
    bx, by = b
    dx = ax - bx
    dy = ay - by
    return dx * dx + dy * dy

def in_circle(
    ax: float,
    ay: float,
    bx: float,
    by: float,
    cx: float,
    cy: float,
    px: float,
    py: float,
) -> float:
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
        dx * (ey * cp - bp * fy) -
        dy * (ex * cp - bp * fx) +
        ap * (ex * fy - ey * fx)
    ) < 0

def circumradius(
    ax: float,
    ay: float,
    bx: float,
    by: float,
    cx: float,
    cy: float,
) -> float:
    dx = bx - ax
    dy = by - ay
    ex = cx - ax
    ey = cy - ay

    bl = dx * dx + dy * dy
    cl = ex * ex + ey * ey
    denom = dx * ey - dy * ex
    d = 0.5 / denom if denom != 0 else inf

    x = (ey * bl - dy * cl) * d
    y = (dx * cl - ex * bl) * d

    return x * x + y * y

def circumcenter(
    ax: float,
    ay: float,
    bx: float,
    by: float,
    cx: float,
    cy: float,
) -> float:
    dx = bx - ax
    dy = by - ay
    ex = cx - ax
    ey = cy - ay

    bl = dx * dx + dy * dy
    cl = ex * ex + ey * ey
    denom = dx * ey - dy * ex
    d = 0.5 / denom if denom != 0 else inf

    x = ax + (ey * bl - dy * cl) * d
    y = ay + (dx * cl - ex * bl) * d

    return x, y


def quicksort(ids: list[int], dists: list[float], left: int, right: int):
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
        if dists[ids[left]] > dists[ids[right]]:
            swap(ids, left, right)
        if dists[ids[i]] > dists[ids[right]]:
            swap(ids, i, right)
        if dists[ids[left]] > dists[ids[i]]:
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
    def __init__(self, coords: list[float]):
        if len(coords) == 0:
            raise ValueError("Invalid array length")
        n = len(coords) >> 1
        if n > 0 and not isinstance(coords[0], (float, int)):
            raise TypeError("Expected coords to contain numbers.")

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

        self.coords = coords
        self.hull = self._triangles
        self.triangles = self._triangles
        self.halfedges = self._halfedges

        self.update()


    @classmethod
    def from_points(
        cls,
        points: list[T],
        get_x: Callable[[T], float] = default_get_x,
        get_y: Callable[[T], float] = default_get_y,
    ) -> TDelaunator:
        n = len(points)
        coords = [None] * (n * 2)

        for i in range(n):
            p = points[i]
            coords[2 * i] = get_x(p)
            coords[2 * i + 1] = get_y(p)

        return cls(coords)

    def __len__(self) -> int:
        return self._triangles_len

    def update(self):
        coords = self.coords
        hull_prev = self._hull_prev
        hull_next = self._hull_next
        hull_tri = self._hull_tri
        hull_hash = self._hull_hash
        n = len(coords) >> 1

        min_x = inf
        min_y = inf
        max_x = -inf
        max_y = -inf

        for i in range(n):
            x = coords[2 * i]
            y = coords[2 * i + 1]
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            self._ids[i] = i

        cx = (min_x + max_x) * 0.5
        cy = (min_y + max_y) * 0.5

        i0 = 0
        i1 = 0
        i2 = 0

        min_dist = inf
        for i in range(n):
            d = dist((cx, cy), (coords[2 * i], coords[2 * i + 1]))
            if d < min_dist:
                i0 = i
                min_dist = d

        i0x = coords[2 * i0]
        i0y = coords[2 * i0 + 1]

        min_dist = inf
        for i in range(n):
            if i == i0:
                continue
            d = dist((i0x, i0y), (coords[2 * i], coords[2 * i + 1]))
            if d < min_dist and d > 0:
                i1 = i
                min_dist = d

        i1x = coords[2 * i1]
        i1y = coords[2 * i1 + 1]

        min_radius = inf
        for i in range(n):
            if i == i0 or i == i1:
                continue
            r = circumradius(
                i0x,
                i0y,
                i1x,
                i1y,
                coords[2 * i],
                coords[2 * i + 1],
            )
            if r < min_radius:
                i2 = i
                min_radius = r

        i2x = coords[2 * i2]
        i2y = coords[2 * i2 + 1]

        if isinf(min_radius):
            for i in range(n):
                self._dists[i] = (
                    (coords[2 * i] - coords[0])
                    or (coords[2 * i + 1] - coords[1])
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
            self.hull = hull[0:j]
            self.triangles = []
            self.halfedges = []
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
        self._cx = center[0]
        self._cy = center[1]

        for i in range(n):
            self._dists[i] = dist((coords[2 * 1], coords[2 * i + 1]), center)

        quicksort(self._ids, self._dists, 0, n - 1)
        self._hull_start = i0
        hull_size = 3

        hull_next[i0] = hull_prev[i2] = i1
        hull_next[i1] = hull_prev[i0] = i2
        hull_next[i2] = hull_prev[i1] = i0

        hull_tri[i0] = 0
        hull_tri[i1] = 1
        hull_tri[i2] = 2

        hull_hash = self._hull_hash = [-1 for _ in self._hull_hash]
        hull_hash[self._hash_key(i0x, i0y)] = i0
        hull_hash[self._hash_key(i1x, i1y)] = i1
        hull_hash[self._hash_key(i2x, i2y)] = i2

        self._triangles_len = 0
        self._add_triangle(i0, i1, i2, -1, -1, -1)

        xp = 0
        yp = 0
        for k in range(len(self._ids)):
            i = self._ids[k]
            x = coords[2 * i]
            y = coords[2 * i + 1]

            if k > 0 and abs(x - xp) <= EPSILON and abs(y - yp) <= EPSILON:
                xp = x
                yp = y

            if i == i0 or i == i1 or i == i2:
                continue

            start = 0
            key = self._hash_key(x, y)
            for j in range(self._hash_size):
                start = hull_hash[(key + j) % self._hash_size]
                if start != -1 and start != hull_next[start]:
                    break

            start = hull_prev[start]
            e = start
            q = hull_next[e]
            while orient2d(
                x,
                y,
                coords[2 * e],
                coords[2 * e + 1],
                coords[2 * q],
                coords[2 * q + 1],
            ) >= 0:
                e = q
                if e == start:
                    e = -1
                    break
                q = hull_next[e]

            if e == -1:
                continue

            t = self._add_triangle(
                e,
                i,
                hull_next[e],
                -1,
                -1,
                hull_tri[e],
            )

            hull_tri[i] = self._legalize(t + 2)
            hull_tri[e] = t
            hull_size += 1


            n = hull_next[e]
            q = hull_next[n]
            while orient2d(
                x,
                y,
                coords[2 * n],
                coords[2 * n + 1],
                coords[2 * q],
                coords[2 * q + 1],
            ) < 0:
                t = self._add_triangle(
                    n,
                    i,
                    q,
                    hull_tri[i],
                    -1,
                    hull_tri[n]
                )
                hull_tri[i] = self._legalize(t + 2)
                hull_next[n] = n
                hull_size -= 1
                n = q
                q = hull_next[n]

            if e == start:
                q = hull_prev[e]
                while orient2d(
                    x,
                    y,
                    coords[2 * q],
                    coords[2 * q + 1],
                    coords[2 * e],
                    coords[2 * e + 1],
                ) < 0:
                    t = self._add_triangle(
                        q,
                        i,
                        e,
                        -1,
                        hull_tri[e],
                        hull_tri[q]
                    )
                    self._legalize(t + 2)
                    hull_tri[q] = t
                    hull_next[e] = e
                    hull_size -= 1
                    e = q
                    q = hull_prev[e]

            self._hull_start = hull_prev[i] = e
            hull_next[e] = hull_prev[n] = i
            hull_next[i] = n

            
            hull_hash[self._hash_key(x, y)] = i
            hull_hash[self._hash_key(coords[2 * e], coords[2 * e + 1])] = e

        self.hull = [None] * hull_size

        e = self._hull_start
        for i in range(hull_size):
            self.hull[i] = e
            e = hull_next[e]

        self.triangles = self._triangles[0:self._triangles_len]
        self.halfedges = self._halfedges[0:self._triangles_len]


    def _hash_key(self, x: float, y: float) -> int:
        return floor(
            pseudo_angle(x - self._cx, y - self._cy) * self._hash_size
        ) % self._hash_size

    def _legalize(self, a: int) -> int:
        triangles = self._triangles
        halfedges = self._halfedges
        coords = self.coords
        i = 0
        ar = 0

        while True:
            b = halfedges[a]

            a0 = a - a % 3
            ar = a0 + (a + 2) % 3

            if b == -1:
                if i == 0:
                    break
                i -= 1
                a = EDGE_STACK[i]
                continue

            b0 = b - b % 3
            al = a0 + (a + 1) % 3
            bl = b0 + (b + 2) % 3

            p0 = triangles[ar]
            pr = triangles[a]
            pl = triangles[al]
            p1 = triangles[bl]

            illegal = in_circle(
                coords[2 * p0], coords[2 * p0 + 1],
                coords[2 * pr], coords[2 * pr + 1],
                coords[2 * pl], coords[2 * pl + 1],
                coords[2 * p1], coords[2 * p1 + 1]
            )

            if illegal:
                triangles[a] = p1
                triangles[b] = p0

                hbl = halfedges[bl]

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

    def _link(self, a: int, b: int):
        self._halfedges[a] = b
        if b != -1:
            self._halfedges[b] = a

    def _add_triangle(
        self,
        i0: int,
        i1: int,
        i2: int,
        a: int,
        b: int,
        c: int
    ) -> int:
        t = self._triangles_len

        self._triangles[t] = i0
        self._triangles[t + 1] = i1
        self._triangles[t + 2] = i2

        self._link(t, a)
        self._link(t + 1, b)
        self._link(t + 2, c)

        self._triangles_len += 3

        return t
