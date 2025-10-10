from .path import Path
from .polygon import Polygon
from math import floor, isnan, inf

class Voronoi:

    def __init__(
        self,
        delaunay,
        bounds: tuple[float, float, float, float] | None = None,
    ):
        if bounds is None:
            bounds = [0, 0, 960, 500]

        if xmax < xmin or ymax < ymin:
            raise ValueError("Invalid bounds")

        xmin, ymin, xmax, ymax = bounds

        self._delaunay = delaunay

        self._circumcenters = [None] * (len(delaunay._points) * 2)
        self._vectors = [None] * (len(delaunay._points) * 2)

        self._xmax = xmax
        self._xmin = xmin
        self._ymax = ymax
        self._ymin = ymin

        self._initialize()


    def update(self):
        self._delaunay.update()
        self._initialize()
        return self

    def _initialize(self):
        self._circumcenters = self._circumcenters[0:len(self._delaunay) / 3 * 2]
        bx = None
        by = None
        triangles = self._delaunay.triangles
        i = 0
        j = 0
        n = len(triangles)
        while i < n:
            i += 3
            j += 2
            t1 = triangles[i] * 2
            t2 = triangles[i + 1] * 2
            t3 = triangles[i + 2] * 2
            x1 = points[t1]
            y1 = points[t1 + 1]
            x2 = points[t2]
            y2 = points[t2 + 1]
            x3 = points[t3]
            y3 = points[t3 + 1]

            dx = x2 - x1
            dy = y2 - y1
            ex = x3 - x1
            ey = y3 - y1
            ab = (dx * ey - dy * ex) * 2

            if abs(ab) < 1e-9:
                if bx is None:
                    bx = by = 0
                    for i in self._delaunay.hull:
                        bx += points[i * 2]
                        by += points[i * 2 + 1]
                    length = len(self._delaunay.hull)
                    bx /= length
                    by /= length
                a = 1e9 * (-1 if (bx - x1) * ey - (by - y1) * ex < 0 else 1)
                x = (x1 + x3) / 2 - a * ey
                y = (y1 + y3) / 2 + a * ex
            else:
                d = 1 / ab
                bl = dx * dx + dy * dy
                cl = ex * ex + ey * ey
                x = x1 + (ey * bl - dy * cl) * d
                y = y1 + (dx * cl - ex * bl) * d
            circumcenters[j] = x
            circumcenters[j + 1] = y

        h = self._delaunay.hull[-1]
        p0 = None
        p1 = h * 4
        x0 = None
        x1 = self._delaunay.coords[2 * h]
        y0 = None
        y1 = self._delaunay.coords[2 * h + 1]
        self._vectors = [0 for _ in self._vectors]
        for h in self._delaunay.hull:
            p0 = p1
            x0 = x1
            y0 = y1
            self._vectors[p0 + 2] = self._vectors[p1] = y0 - y1
            self._vectors[p0 + 3] = self._vectors[p1 + 1] = x1 - x0

    def render(self, context=None):
        if context is None:
            buffer = context = Path()
        else:
            buffer = None

        if len(self._delaunay.hull) <= 1:
            return None

        for i, j in enumerate(self._delaunay.halfedges):
            if j < i:
                continue
            ti = floor(i / 3) * 2
            tj = floor(j / 3) * 2
            xi = self._circumcenters[ti]
            yi = self._circumcenters[ti + 1]
            xj = self._circumcenters[tj]
            yj = self._circumcenters[tj + 1]
            self._render_segment(xi, yi, xj, yj, context)

        h0 = None
        h1 = self._delaunay.hull[-1]
        for i in range(len(self._delaunay.hull)):
            h0 = h1
            h1 = self._delaunay.hull[i]
            t = floor(self._delaunay.inedges[h1] / 3) * 2
            x = self._circumcenters[t]
            y = self._circumcenters[t + 1]
            v = h0 * 4
            p = self._project(x, y, self._vectors[v + 2], self._vectors[v + 3])
            if p:
                self._render_segment(x, y, p[0], p[1], context)
        return None if buffer is None else str(buffer)

    def _render_bounds(self, context=None):
        if context is None:
            buffer = context = Path()
        else:
            buffer = None
        
        context.rect(
            self._xmin,
            self._ymin,
            self._xmax - self._xmin,
            self._ymax - self._ymin,
        )
        return None if buffer is None else str(buffer)

    def render_cell(self, i, context=None):
        if context is None:
            buffer = context = Path()
        else:
            buffer = None

        points = self._clip(i)
        if points is None or len(points) == 0:
            return
        context.move_to(points[0], points[1])
        n = len(points)
        while points[0] == points[n - 2] and points[1] == points[n - 1] and n > 1:
            n -= 2
        for i in range(2, len(n), 2):
            if points[i] != points[i - 2] or points[i + 1] != points[i - 1]:
                context.line_to(points[i], points[i + 1])
        context.close_path()
        return None if buffer is None else str(buffer)

    def cell_polygons(self):
        for i in range(len(self._delaunay.coords) // 2):
            cell = self.cell_polygon(i)
            if cell:
                cell.index = i
                yield cell

    def cell_polygon(self, i):
        polygon = Polygon()
        self._render_cell(i, polygon)
        return polygon.value()

    def _render_segment(self, x0, y0, x1, y1, context=None):
        c0 = self._regioncode(x0, y0)
        c1 = self._regioncode(x1, y1)
        if c0 == 0 and c1 == 0:
            context.move_to(x0, y0)
            context.line_to(x1, y1)
        elif S:=self._clip_segment(x0, y0, x1, y1, c0, c1):
            context.move_to(S[0], S[1])
            context.line_to(S[2], S[3])

    def contains(self, i, x, y):
        if isnan(x) or isnan(y):
            return False
        return self._delaunay._step(i, x, y) == i


    def neighbors(self, i):
        ci = self._clip(i)
        if ci:
            for j in self._delaunay.neighbors(i):
                cj = self._clip(j)
                if cj:
                    break_loop = False
                    for ai in range(0, len(ci), 2):
                        for aj in range(0, len(cj), 2):
                            if (
                                ci[ai] == cj[aj]
                                and ci[ai + 1] == cj[aj + 1]
                                and ci[(ai + 2) % li] == cj[(aj + lj - 2) % lj]
                                and ci[(ai + 3) % li] == cj[(aj + lj - 1) % lj]
                            ):
                                yield j
                                break_loop = True
                                break
                        if break_loop:
                            break

    def _cell(self, i):
        e0 = self._delaunay.inedges[i]
        if e0 == -1:
            return None
        points = []
        e = e0
        while True:
            t = floor(e / 3)
            points.append(self._circumcenters[t * 2], self._circumcenters[t * 2 + 1])
            e = e - 2 if e % 3 == 2 else e + 1
            if self._delaunay.triangles[e] != i:
                break
            e = self._delaunay.halfedges[e]
            if e == e0 or e == -1:
                break
        return points

    def _clip(self, i):
        if i == 0 and len(self._delaunay.hull) == 1:
            return [
                self._xmax,
                self._ymin,
                self._xmax,
                self._ymax,
                self._xmin,
                self._ymax,
                self._xmin,
                self._ymin,
            ]

        points = self._cell(i)
        if points is None:
            return None
        v = i * 4
        return (
            self._clip_infinite(
                i,
                points,
                self._vectors[v],
                self._vectors[v + 1],
                self._vectors[v + 2],
                self._vectors[v + 3]
            ) if self._simplify(
                self._vectors[v] or self._vectors[v + 1]
            ) else self._clip_finite(i, points)
        )

    def _clip_finite(self, i, points):
        n = len(points)
        P = None
        x0 = None
        y0 = None
        x1 = points[n - 2]
        y1 = points[n - 1]
        c0 = None
        c1 = sefl._regioncode(x1, y1)
        e0 = None
        e1 = 0
        for j in range(0, n, 2):
            x0 = x1
            y0 = y1
            x1 = points[j]
            y1 = points[j + 1]
            c0 = c1
            c1 = self._regioncode(x1, y1)
            if c0 == 0 and c1 == 0:
                e0 = e1
                e1 = 0
                if P:
                    P.extend([x1, y1])
                else:
                    P = [x1, y1]
            else:
                if c0 == 0:
                    S = self._clip_segment(x0, y0, x1, y1, c0, c1)
                    if S is None:
                        continue
                    sx0, sy0, sx1, sy1 = S
                else:
                    S = self._clip_segment(x1, y1, x0, y0, c1, c0)
                    if S is None:
                        continue
                    sx1, sy1, sx0, sy0 = S
                    e0 = e1
                    e1 = self._edgecode(sx0, sy0)
                    if e0 and e1:
                        self._edge(i, e0, e1, P, len(P))
                    if P:
                        P.extend([sx0, sy0])
                    else:
                        P = [sx0, sy0]
            e0 = e1
            e1 = self._edgecode(sx1, sy1)
            if e0 and e1:
                self._edge(i, e0, e1, P, len(P))
            if P:
                P.extend([sx1, sy1])
            else:
                P = [sx1, sy1]
        if P:
            e0 = e1
            e1 = self._edgecode(P[0], P[1])
            if e0 and e1:
                self._edge(i, e0, e1, P, len(P))
            elif self.contains(
                i,
                (self._xmin + self._xmax) * 0.5,
                (self._ymin + self._ymax) * 0.5,
            ):
                return [
                    self._xmax,
                    self._ymin,
                    self._xmax,
                    self._ymax,
                    self._xmin,
                    self._ymax,
                    self._xmin,
                    self._ymin,
                ]
        return P


    def _clip_segment(self, x0, y0, x1, y1, c0, c1):
        flip = c0 < c1
        if flip:
            x0, y0, x1, y1, c0, c1 = x1, y1, x0, y0, c1, c0

        while True:
            if c0 == 0 and c1 == 0:
                return [x1, y1, x0, y0] if flip else [x0, y0, x1, y1]
            if c0 & c1:
                return None
            c = c0 or c1
            if c & 0b1000:
                x = x0 + (x1 - x0) * (self._ymax - y0) / (y1 - y0)
                y = self._ymax
            elif c & 0b0100:
                x = x0 + (x1 - x0) * (self._ymin - y0) / (y1 - y0)
                y = self._ymin
            elif c & 0b0010:
                y = y0 + (y1 - y0) * (self._xmax - x0) / (x1 - x0)
                x = self._xmax
            else:
                y = y0 + (y1 - y0) * (self._xmin - x0) / (x1 - x0)
                x = self._xmin
            if c0:
                x0 = x
                y0 = y
                c0 = self._regioncode(x0, y0)
            else:
                x1 = x
                y1 = y
                c1 = self._regioncode(x1, y1)

    def _clip_infinite(self, i, points, vx0, vy0, vxn, vyn):
        P = list(points)
        p = self._project(P[0], P[1], vx0, vy0)
        if p:
            P.pop(p[0])
            P.pop(p[1])
        p = self._project(P[-2], P[-1], vxn, vyn)
        if p:
            P.append(p[0])
            P.append(p[1])
        P = self._clip_finite(i, P)
        if P:
            c1 = self._edgecode(P[-2], P[-1])
            n = len(P)
            j = 0
            while j < n:
                c0 = c1
                c1 = self._edgecode(P[j], P[j + 1])
                if c0 and c1:
                    j = self._edge(i, c0, c1, P, j)
                    n = len(P)
                j += 2

        elif self.contains(i, (self._xmin + self._xmax) * 0.5, (self._ymin + self._ymax) * 0.5):
            P = [
                self._xmin,
                self._ymin,
                self._xmax,
                self._ymin,
                self._xmax,
                self._ymax,
                self._xmin,
                self._ymax,
            ]
        return P

    def _edge(self, i, e0, e1, P, j):
        while e0 != e1:
            match e0:
                case 0b0101:
                    e0 = 0b0100
                    continue
                case 0b0100:
                    e0 = 0b0110
                    x = self._xmax
                    y = self._ymin
                case 0b0110:
                    e0 = 0b0010
                    continue
                case 0b0010:
                    e0 = 0b1010
                    x = self._xmax
                    y = self._ymax
                case 0b1010:
                    e0 = 0b1000
                    continue
                case 0b1000:
                    e0 = 0b1001
                    x = self._xmin
                    y = self._ymax
                case 0b1001:
                    e0 = 0b0001
                    continue
                case 0b0001:
                    e0 = 0b0101
                    x = self._xmin
                    y = self._ymin

            if P[j] != x or P[j + 1] != y and self.contains(i, x, y):
                P.insert(j, x)
                P.insert(j + 1, y)
                j += 2
        return j

    def _project(self, x0, y0, vx, vy):
        t = inf
        if vy < 0:
            if y0 <= self._ymin:
                return None
            c = (self._ymin - y0) / vy
            if c < t:
                y = self._ymin
                t = c
                x = x0 + t * vx
        elif vy > 0:
            if y0 >= self._ymax:
                return None
            c = (self._ymax - y0) / vy
            if c < t:
                y = self._ymax
                t = c
                x = x0 + t * vx

        if vx > 0:
            if x0 >= self._xmax:
                return None
            c = (self._xmax - x0) / vx
            if c < t:
                x = self._xmax
                t = c
                y = y0 + t * vy
        elif vx < 0:
            if x0 <= self._xmin:
                return None
            c = (self._xmin - x0) / vx
            if c < t:
                x = self._xmin
                t = c
                y = y0 + t * vym

        return [x, y]


    def _edgecode(self, x, y):
        if x == self._xmin:
            a = 0b0001
        elif x == self._xmax:
            a = 0b0010
        else:
            a = 0b0000

        if y == self._ymin:
            b = 0b0100
        elif y == self._ymax:
            b = 0b1000
        else:
            b = 0b0000

        return a | b

    def _regioncode(self, x, y):
        if x < self._xmin:
            a = 0b0001
        elif x > self._xmax:
            a = 0b0010
        else:
            a = 0b0000

        if y < self._ymin:
            b = 0b0100
        elif y > self._ymax:
            b = 0b1000
        else:
            b = 0b0000

        return a | b

    def _simplify(self, P):
        if P and len(P) > 4:
            n = len(P)
            i = 0
            while i < n:
                j = (i + 2) % n
                k = (i + 4) % n
                if P[i] == P[j] and P[j] == P[k] or P[i + 1] == P[j + 1] and P[j + 1] == P[k + 1]:
                    P.pop(j)
                    P.pop(j)
                    n = len(P)
                else:
                    i += 2
            if not n:
                P = None
        return P
