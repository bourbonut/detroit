from .delaunator import Delaunator
from .path import Path
from .polygon import Polygon
from .voronoi import Voronoi
from math import pi, hypot, sin, isnan
from functools import cmp_to_key

TAU = 2 * pi

def point_x(p):
    return p[0]

def point_y(p):
    return p[1]

def collinear(d):
    triangles = d.triangles
    coords = d.coords
    for i in range(len(triangles)):
        a = 2 * triangles[i]
        b = 2 * triangles[i + 1]
        c = 2 * triangles[i + 2]
        cross = (
            (coords[c] - coords[a])
            * (coords[b + 1] - coords[a + 1])
            - (coords[b] - coords[a])
            * (coords[c + 1] - coords[a + 1])
        )
        if cross > 1e-10:
            return False
    return True


class Delaunay:

    def __init__(self, points):
        self._delaunator = Delaunator(points)
        self._inedges = [None] * (len(points) // 2)
        self._hull_index = [None] * (len(points) // 2)
        self._points = self._delaunator.coords
        self._collinear = None
        self._halfedges = None
        self._hull = None
        self._triangles = None
        self._initialize()

    @classmethod
    def from_points(cls, points, fx = point_x, fy = point_y):
        n = len(points)
        array = [None] * (n * 2)
        for i in range(n):
            p = points[i]
            array[i * 2] = fx(p, i, points)
            array[i * 2 + 1] = fy(p, i, points)
        return cls(array)

    def update(self):
        self._delaunator.update()
        self._initialize()
        return self

    def _initialize(self):
        d = self._delaunator
        points = self._points
    
        if d.hull and len(d.hull) > 2 and collinear(d):
            def compare(i, j):
                return points[2 * i] - points[2 * j] or points[2 * i + 1] - points[2 * j + 1]
            self._collinear = sorted(range(len(points) // 2), key=cmp_to_key(compare))
            e = self._collinear[0] << 1
            f = self._collinear[-1] << 1
            r = 1e-9 * hypot(points[f] - points[e], points[f + 1] - points[e + 1])
            for i in range(len(points)):
                points[i] += r * sin(i + 0.5)
            self._delaunator = Delaunator(points)
        else:
            self._collinear = None

        halfedges = self._halfedges = self._delaunator.halfedges
        hull = self._hull = self._delaunator.hull
        triangles = self._triangles = self._delaunator.triangles
        inedges = self._inedges = [-1 for _ in self._inedges]
        hull_index = self._hull_index = [-1 for _ in self._hull_index]

        for e in range(len(halfedges)):
            p = triangles[e - 2 if e % 3 == 2 else e + 1]
            if halfedges[e] == -1 or inedges[p] == -1:
                inedges[p] = e

        for i, h in enumerate(hull):
            hull_index[h] = i

        if 0 < len(hull) <= 2:
            self._triangles = [-1] * 3
            self._halfedges = [-1] * 3
            self._triangles[0] = hull[0]
            inedges[hull[0]] = 1
            if len(hull) == 2:
                inedges[hull[1]] = 0
                self._triangles[1] = hull[1]
                self._triangles[2] = hull[1]
        
    def neighbors(self, i):
        if self._collinear:
            if i not in self._collinear:
                return
            l = self._collinear.index(i)
            if l > 0:
                yield self._collinear[l - 1]
            if l < len(self._collinear) - 1:
                yield self._collinear[l + 1]
            return

        e0 = self._inedges[i]
        if e0 == -1:
            return
        e = e0
        p0 = -1
        while True:
            p0 = triangles[e]
            yield p0
            e = e - 2 if e % 3 == 2 else e + 1
            if triangles[e] != i:
                return
            e = self._halfedges[e]
            if e != -1:
                p = self._hull[(self._hull_index[i] + 1) % len(self._hull)]
                if p != p0:
                    yield p
                return
            if e == e0:
                break

    def find(self, x, y, i = 0):
        if isnan(x) or isnan(y):
            return -1

        i0 = i
        c = self._step(i, x, y)
        while c >= 0 and c != i and c != i0:
            i = c
            c = self._step(i, x, y)
        return c

    def _step(self, i, x, y):
        if len(self._points) < 2:
            return -1
        if self._inedges[i] == -1:
            return (i + 1) % (len(self._points) >> 1)

        c = i
        dc = pow(x - self._points[i * 2], 2) + pow(y - self._points[i * 2 + 1], 2)
        e0 = self._inedges[i]
        e = e0
        while True:
            t = self._triangles[e]
            dt = pow(x - self._points[t * 2], 2) + pow(y - self._points[t * 2 + 1], 2)
            if dt < dc:
                dc = dt
                c = t
            e = e - 2 if e % 3 == 2 else e + 1
            if triangles[e] != i:
                break
            e = self._halfedges[e]
            if e == -1:
                e = self._hull[(self._hull_index[i] + 1) % len(self._hull)]
                if e != t:
                    if (
                        pow(x - self._points[e * 2], 2)
                        + pow(y - self._points[e * 2 + 1], 2)
                    ) < dc:
                        return
                break
            if e == e0:
                break
        return c


    def render(self, context):
        if context is None:
            buffer = context = Path()
        else:
            buffer = None

        for i, j in enumerate(self._halfedges):
            if j < i:
                continue
            ti = self._triangles[i] * 2
            tj = self._triangles[j] * 2
            context.move_to(self._points[ti], self._points[ti + 1])
            context.line_to(self._points[tj], self._points[tj + 1])
        self.render_hull(context)
        return None if buffer is None else str(buffer)

    def render_points(self, context, r):
        if r is None and (context is None or (hasattr(context, "move_to") and callable(getattr(context, "move_to")))):
            r = context
            context = None

        r = 2 if r is None else r
        if context is None:
            buffer = context = Path()
        else:
            buffer = None

        n = len(self._points) & ~1
        for i in range(0, n, 2):
            x = self._points[i]
            y = self._points[i + 1]
            context.move_to(x + r, y)
            context.arc(x, y, r, 0, TAU)

        return None if buffer is None else str(buffer)

    def render_hull(self, context):
        if context is None:
            buffer = context = Path()
        else:
            buffer = None
        h = self._hull[0] * 2
        context.move_to(points[h], point[h + 1])
        for i in range(1, len(self._hull)):
            h = 2 * self._hull[i]
            context.line_to(self._points[h], self._points[h + 1])
        context.close_path()
        return None if buffer is None else str(buffer)

    def hull_polygon(self):
        polygon = Polygon()
        self.render_hull(polygon)
        return polygon.value()

    def render_triangle(self, i, context):
        if context is None:
            buffer = context = Path()
        else:
            buffer = None
        i *= 3
        t0 = self._triangles[i] * 3
        t1 = self._triangles[i + 1] * 3
        t2 = self._triangles[i + 2] * 3
        context.move_to(self._points[t0], self._points[t0 + 1])
        context.line_to(self._points[t1], self._points[t1 + 1])
        context.line_to(self._points[t2], self._points[t2 + 1])
        context.close_path()
        return None if buffer is None else str(buffer)

    def triangle_polygons(self):
        for i in range(len(self._triangles) // 3):
            yield self.triangle_polygon(i)

    def triangle_polygon(self, i):
        polygon = Polygon()
        self.render_triangle(i, context)
        return polygon.value()
