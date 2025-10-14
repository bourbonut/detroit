from collections.abc import Callable
from math import ceil, floor, inf, isinf, nan, sqrt
from typing import Any, TypeVar

from ..types import T
from .orient2d import orient2d

TDelaunator = TypeVar("Delaunator", bound="Delaunator")

EPSILON = pow(2, -52)
EDGE_STACK = [0] * 512


def default_get_x(p: tuple[float, float]) -> float:
    return p[0]


def default_get_y(p: tuple[float, float]) -> float:
    return p[1]


def swap(arr: list[Any], i: int, j: int):
    arr[i], arr[j] = arr[j], arr[i]


def pseudo_angle(dx: float, dy: float) -> float:
    """
    Monotonically increases with real angle, but doesn't need expensive
    trigonometry.

    Parameters
    ----------
    dx : float
        Delta x difference
    dy : float
        Delta y difference

    Returns
    -------
    float
        Pseudo angle
    """
    p = dx / (abs(dx) + abs(dy))
    return (3 - p if dy > 0 else 1 + p) * 0.25


def dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    """
    Returns the squared distance between two points.

    Parameters
    ----------
    a : tuple[float, float]
        Point A
    b : tuple[float, float]
        Point B

    Returns
    -------
    float
        Squared distance between :code:`a` and :code:`b`
    """
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
) -> bool:
    """
    Checks whether point P is inside a circle formed by points A, B, C.

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
    px : float
        X-coordinate of point P
    py : float
        Y-coordinate of point P

    Returns
    -------
    bool
        :code:`True` if P is in the circle formed by points A, B, C.
    """
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
        dx * (ey * cp - bp * fy) - dy * (ex * cp - bp * fx) + ap * (ex * fy - ey * fx)
    ) < 0


def circumradius(
    ax: float,
    ay: float,
    bx: float,
    by: float,
    cx: float,
    cy: float,
) -> float:
    """
    Computes the squared radius of the circle formed by points A, B, C.

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
        Squared radius of the circle formed by points A, B, C.
    """
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
) -> tuple[float, float]:
    """
    Computes the center of the circle formed by points A, B, C.

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
    tuple[float, float]
        Center of the circle formed by points A, B, C.
    """
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
    """
    Sort points by distance via an array of point indices and an array of
    calculated distances.

    Parameters
    ----------
    ids : list[int]
        List of point indices
    dists : list[float]
        List of calculated distances
    left : int
        Left index used recursively by the function itself
    right : int
        Right index used recursively by the function itself
    """
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
    """
    Delaunay triangulation object based an list of point coordinates of the
    form: :math:`[x_0, y_0, x_1, y_1, \\ldots]`.

    Parameters
    ----------
    points : list[float]
        The coordinates of the points as an array :math:`[x_0, y_0, x_1, y_1,
        \\ldots]`.

    Attributes
    ----------
    coords : list[float]
        Point coordinates
    hull : list[int]
        Array of indices that reference points on the convex hull of the input
        data, counter-clockwise.
    triangles : list[int]
        Array of triangle vertex indices (each group of three numbers forms a
        triangle). All triangles are directed counterclockwise.
    halfedges : list[int]
         Array of triangle half-edge indices that allows you to traverse the
         triangulation. :code:`i`-th half-edge in the array corresponds to
         vertex :code:`triangles[i]` the half-edge is coming from.
         :code:`halfedges[i]` is the index of a twin half-edge in an adjacent
         triangle (or :code:`-1` for outer half-edges on the convex hull).
    """

    def __init__(self, coords: list[float]):
        if len(coords) == 0:
            raise ValueError("Invalid array length")
        n = len(coords) >> 1
        if n > 0 and not isinstance(coords[0], (float, int)):
            raise TypeError("Expected coords to contain numbers.")

        max_triangles = max(2 * n - 5, 0)
        self._triangles = [0] * (max_triangles * 3)
        self._halfedges = [0] * (max_triangles * 3)

        self._hash_size = ceil(sqrt(n))
        self._hull_prev = [0] * n
        self._hull_next = [0] * n
        self._hull_tri = [0] * n

        self._hull_hash = [0] * self._hash_size

        self._ids = [0] * n
        self._dists = [0] * n

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
        """
        Creates a :code:`Delaunator` object given a list of points.

        Parameters
        ----------
        points : list[T]
            List of points
        get_x : Callable[[T], float]
            X-coordinate accessor
        get_y : Callable[[T], float]
            Y-coordinate accessor

        Returns
        -------
        Delaunator
            Delaunator object
        """
        n = len(points)
        coords = [0] * (n * 2)

        for i in range(n):
            p = points[i]
            coords[2 * i] = get_x(p)
            coords[2 * i + 1] = get_y(p)

        return cls(coords)

    def __len__(self) -> int:
        return self._triangles_len

    def update(self):
        """
        Updates the triangulation if you modified :code:`delaunay.coords`
        values in place, avoiding expensive memory allocations. Useful for
        iterative relaxation algorithms such as Lloyd's.
        """
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
                self._dists[i] = (coords[2 * i] - coords[0]) or (
                    coords[2 * i + 1] - coords[1]
                )
            quicksort(self._ids, self._dists, 0, n - 1)
            hull = [0] * n
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

        xp = nan
        yp = nan
        for k in range(len(self._ids)):
            i = self._ids[k]
            x = coords[2 * i]
            y = coords[2 * i + 1]

            if k > 0 and abs(x - xp) <= EPSILON and abs(y - yp) <= EPSILON:
                continue

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
            while (
                orient2d(
                    x,
                    y,
                    coords[2 * e],
                    coords[2 * e + 1],
                    coords[2 * q],
                    coords[2 * q + 1],
                )
                >= 0
            ):
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
            while (
                orient2d(
                    x,
                    y,
                    coords[2 * n],
                    coords[2 * n + 1],
                    coords[2 * q],
                    coords[2 * q + 1],
                )
                < 0
            ):
                t = self._add_triangle(n, i, q, hull_tri[i], -1, hull_tri[n])
                hull_tri[i] = self._legalize(t + 2)
                hull_next[n] = n
                hull_size -= 1
                n = q
                q = hull_next[n]

            if e == start:
                q = hull_prev[e]
                while (
                    orient2d(
                        x,
                        y,
                        coords[2 * q],
                        coords[2 * q + 1],
                        coords[2 * e],
                        coords[2 * e + 1],
                    )
                    < 0
                ):
                    t = self._add_triangle(q, i, e, -1, hull_tri[e], hull_tri[q])
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

        self.hull = [0] * hull_size

        e = self._hull_start
        for i in range(hull_size):
            self.hull[i] = e
            e = hull_next[e]

        self.triangles = self._triangles[0 : self._triangles_len]
        self.halfedges = self._halfedges[0 : self._triangles_len]

    def _hash_key(self, x: float, y: float) -> int:
        """
        Calculate an angle-based key for the edge hash used for advancing
        convex hull.

        Parameters
        ----------
        x : float
            X-coordinate point
        y : float
            Y-coordinate point

        Returns
        -------
        int
            angle-based key
        """
        return (
            floor(pseudo_angle(x - self._cx, y - self._cy) * self._hash_size)
            % self._hash_size
        )

    def _legalize(self, a: int) -> int:
        """
        Flip an edge in a pair of triangles if it doesn't satisfy the Delaunay
        condition.

        Parameters
        ----------
        a : int
            Edge index

        Returns
        -------
        int
            New index
        """
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
                coords[2 * p0],
                coords[2 * p0 + 1],
                coords[2 * pr],
                coords[2 * pr + 1],
                coords[2 * pl],
                coords[2 * pl + 1],
                coords[2 * p1],
                coords[2 * p1 + 1],
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
        """
        Link two half-edges to each other.

        Parameters
        ----------
        a : int
            First half-edge id
        b : int
            Second half-edge id
        """
        self._halfedges[a] = b
        if b != -1:
            self._halfedges[b] = a

    def _add_triangle(self, i0: int, i1: int, i2: int, a: int, b: int, c: int) -> int:
        """
        Add a new triangle given vertex indices and adjacent half-edge ids.

        Parameters
        ----------
        i0 : int
            First vertex index
        i1 : int
            Second vertex index
        i2 : int
            Third vertex index
        a : int
            First adjacent half-edge id
        b : int
            Second adjacent half-edge id
        c : int
            Third adjacent half-edge id

        Returns
        -------
        int


        """
        t = self._triangles_len

        self._triangles[t] = i0
        self._triangles[t + 1] = i1
        self._triangles[t + 2] = i2

        self._link(t, a)
        self._link(t + 1, b)
        self._link(t + 2, c)

        self._triangles_len += 3

        return t
