from collections.abc import Iterator
from math import floor, inf, isnan
from typing import TypeVar

from .context import Context
from .path import Path
from .polygon import Polygon

Delaunay = TypeVar("Delaunay", bound="Delaunay")
TVoronoi = TypeVar("Voronoi", bound="Voronoi")


def sign(x: float) -> float:
    if x == 0:
        return 0
    elif x < 0:
        return -1
    else:
        return 1


class Voronoi:
    """
    Voronoi diagram for the given Delaunay triangulation. When rendering, the
    diagram will be clipped to the specified :code:`bounds = [xmin, ymin, xmax,
    ymax]`.

    Parameters
    ----------
    delaunay : Delaunay
        Delaunay object
    bounds : tuple[float, float, float, float] | None
        The bounds of the viewport :code:`[xmin, ymin, xmax, ymax]` for
        rendering the Voronoi diagram. If :code:`bounds` is not specified, it
        defaults to :code:`[0, 0, 960, 500]`

    Attributes
    ----------
    delaunay : Delaunay
        Delaunay object
    vectors : list[float]
        List :math:`[v_{x_0}, v_{y_0}, w_{x_0}, w_{y_0}, \\ldots]`  where each
        non-zero quadruple describes an open (infinite) cell on the outer hull,
        giving the directions of two open half-lines.
    circumcenters : list[float]
        The circumcenters of the Delaunay triangles :math:`[c_{x_0}, c_{y_0},
        c_{x_1}, c_{y_1}, \\ldots]`. Each contiguous pair of coordinates
        :math:`c_x`, :math:`c_y` is the circumcenter for the corresponding
        triangle. These circumcenters form the coordinates of the Voronoi cell
        polygons.
    xmin : float
        Bound of viewport
    xmax : float
        Bound of viewport
    ymin : float
        Bound of viewport
    ymax : float
        Bound of viewport
    """

    def __init__(
        self,
        delaunay: Delaunay,
        bounds: tuple[float, float, float, float] | None = None,
    ):
        if bounds is None:
            bounds = [0, 0, 960, 500]

        xmin, ymin, xmax, ymax = bounds
        if xmax < xmin or ymax < ymin:
            raise ValueError("Invalid bounds")

        self._circumcenters = [0.0] * (len(delaunay.points) * 2)

        self.delaunay = delaunay
        self.vectors = [0.0] * (len(delaunay.points) * 2)
        self.circumcenters = self._circumcenters
        self.xmax = xmax
        self.xmin = xmin
        self.ymax = ymax
        self.ymin = ymin

        self._initialize()

    def update(self) -> TVoronoi:
        """
        Updates the Voronoi diagram and underlying triangulation after the
        points have been modified in-place — useful for Lloyd's relaxation.

        Returns
        -------
        Voronoi
            Itself
        """
        self.delaunay.update()
        self._initialize()
        return self

    def _initialize(self):
        points = self.delaunay.points
        hull = self.delaunay.hull
        triangles = self.delaunay.triangles

        circumcenters = self.circumcenters = self._circumcenters[
            0 : len(triangles) // 3 * 2
        ]
        bx = None
        by = None
        i = 0
        j = 0
        n = len(triangles)
        while i < n:
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
                    for k in hull:
                        bx += points[k * 2]
                        by += points[k * 2 + 1]
                    length = len(hull)
                    bx /= length
                    by /= length
                a = 1e9 * sign((bx - x1) * ey - (by - y1) * ex)
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

            i += 3
            j += 2

        h = hull[-1]
        p0 = None
        p1 = h * 4
        x0 = None
        x1 = points[2 * h]
        y0 = None
        y1 = points[2 * h + 1]
        vectors = self.vectors = [0 for _ in self.vectors]
        for h in hull:
            p0 = p1
            x0 = x1
            y0 = y1
            p1 = h * 4
            x1 = points[2 * h]
            y1 = points[2 * h + 1]
            vectors[p0 + 2] = vectors[p1] = y0 - y1
            vectors[p0 + 3] = vectors[p1 + 1] = x1 - x0

    def render(self, context: Context | None = None) -> str | None:
        """
        Renders the mesh of Voronoi cells to the specified context. If a
        :code:`context` is not specified, an SVG path string is returned
        instead.

        Parameters
        ----------
        context : Context | None
            Context object

        Returns
        -------
        str | None
            SVG path string
        """
        if context is None:
            buffer = context = Path()
        else:
            buffer = None

        halfedges = self.delaunay.halfedges
        inedges = self.delaunay.inedges
        hull = self.delaunay.hull
        circumcenters = self.circumcenters
        vectors = self.vectors

        if len(hull) <= 1:
            return None

        for i, j in enumerate(halfedges):
            if j < i:
                continue
            ti = floor(i / 3) * 2
            tj = floor(j / 3) * 2
            xi = circumcenters[ti]
            yi = circumcenters[ti + 1]
            xj = circumcenters[tj]
            yj = circumcenters[tj + 1]
            self._render_segment(xi, yi, xj, yj, context)

        h0 = None
        h1 = hull[-1]
        for i in range(len(hull)):
            h0 = h1
            h1 = hull[i]
            t = floor(inedges[h1] / 3) * 2
            x = circumcenters[t]
            y = circumcenters[t + 1]
            v = h0 * 4
            p = self._project(x, y, vectors[v + 2], vectors[v + 3])
            if p:
                self._render_segment(x, y, p[0], p[1], context)
        return None if buffer is None else str(buffer)

    def render_bounds(self, context: Context | None = None) -> str | None:
        """
        Renders the viewport extent to the specified :code:`context`.
        Equivalent to :code:`context.rect(voronoi.xmin, voronoi.ymin,
        voronoi.xmax - voronoi.xmin, voronoi.ymax - voronoi.ymin)`. If a
        :code:`context` is not specified, an SVG path string is returned
        instead.

        Parameters
        ----------
        context : Context | None
            Context object

        Returns
        -------
        str | None
            SVG path string
        """
        if context is None:
            buffer = context = Path()
        else:
            buffer = None

        context.rect(
            self.xmin,
            self.ymin,
            self.xmax - self.xmin,
            self.ymax - self.ymin,
        )
        return None if buffer is None else str(buffer)

    def render_cell(self, i: int, context: Context | None = None) -> str | None:
        """
        Renders the cell with the specified index :code:`i` to the specified
        context. If a :code:`context` is not specified, an SVG path string is
        returned instead.

        Parameters
        ----------
        context : Context | None
            Context object
        i : int
           Cell index

        Returns
        -------
        str | None
            SVG path string
        """
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
        for i in range(2, n, 2):
            if points[i] != points[i - 2] or points[i + 1] != points[i - 1]:
                context.line_to(points[i], points[i + 1])
        context.close_path()
        return None if buffer is None else str(buffer)

    def cell_polygons(self) -> Iterator[list[tuple[float, float]] | None]:
        """
        Returns an iterable over the non-empty polygons for each cell, with the
        cell index as property.

        Returns
        -------
        Iterator[list[tuple[float, float]] | None]
            Non-empty polygons for each cell
        """
        points = self.delaunay.points
        for i in range(len(points) // 2):
            cell = self.cell_polygon(i)
            if cell:
                # cell.index = i # lists cannot have attributes
                yield cell

    def cell_polygon(self, i: int) -> list[tuple[float, float]] | None:
        """
        Returns the convex closed polygon :math:`[[x_0, y_0], [x_1, y_1],
        \\ldots, [x_0, y_0]]` representing the cell for the specified point
        :code:`i`.

        Parameters
        ----------
        i : int
            Point index

        Returns
        -------
        list[tuple[float, float]] | None
            Convex closed polygon :math:`[[x_0, y_0], [x_1, y_1], \\ldots,
            [x_0, y_0]]`
        """
        polygon = Polygon()
        self.render_cell(i, polygon)
        return polygon.value()

    def _render_segment(
        self,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        context=None,
    ):
        c0 = self._regioncode(x0, y0)
        c1 = self._regioncode(x1, y1)
        if c0 == 0 and c1 == 0:
            context.move_to(x0, y0)
            context.line_to(x1, y1)
        elif S := self._clip_segment(x0, y0, x1, y1, c0, c1):
            context.move_to(S[0], S[1])
            context.line_to(S[2], S[3])

    def contains(self, i: int, x: float, y: float) -> bool:
        """
        Returns :code:`True` if the cell with the specified index :code:`i`
        contains the specified point :math:`(x, y)`; i.e., whether the point
        :code:`i` is the closest point in the diagram to the specified point.
        (This method is not affected by the associated Voronoi diagram's
        viewport bounds.)

        Parameters
        ----------
        i : int
            Cell index
        x : float
            X-coordinate point
        y : float
            Y-coordinate point

        Returns
        -------
        bool
            :code:`True` if cell contains the specified point
        """
        if isnan(x) or isnan(y):
            return False
        return self.delaunay._step(i, x, y) == i

    def neighbors(self, i: int) -> Iterator[int]:
        """
        Returns an iterable over the indexes of the cells that share a common
        edge with the specified cell :code:`i`. Voronoi neighbors are always
        neighbors on the Delaunay graph, but the converse is false when the
        common edge has been clipped out by the Voronoi diagram's viewport.

        Parameters
        ----------
        i : int
            Cell index

        Returns
        -------
        Iterator[int]
            Iterable over the indexes of the cells
        """
        ci = self._clip(i)
        if not ci:
            return
        for j in self.delaunay.neighbors(i):
            cj = self._clip(j)
            if not cj:
                continue

            break_loop = False
            li = len(ci)
            for ai in range(0, li, 2):
                lj = len(cj)
                for aj in range(0, lj, 2):
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

    def _cell(self, i: int) -> list[float] | None:
        circumcenters = self.circumcenters
        inedges = self.delaunay.inedges
        halfedges = self.delaunay.halfedges
        triangles = self.delaunay.triangles

        e0 = inedges[i]
        if e0 == -1:
            return None

        points = []
        e = e0
        while True:
            t = floor(e / 3)
            points.extend([circumcenters[t * 2], circumcenters[t * 2 + 1]])
            e = e - 2 if e % 3 == 2 else e + 1
            if triangles[e] != i:
                break
            e = halfedges[e]
            if e == e0 or e == -1:
                break
        return points

    def _clip(self, i: int) -> tuple[float, float, float, float, float, float]:
        if i == 0 and len(self.delaunay.hull) == 1:
            return [
                self.xmax,
                self.ymin,
                self.xmax,
                self.ymax,
                self.xmin,
                self.ymax,
                self.xmin,
                self.ymin,
            ]

        points = self._cell(i)
        if points is None:
            return None

        vectors = self.vectors
        v = i * 4
        return self._simplify(
            self._clip_infinite(
                i, points, vectors[v], vectors[v + 1], vectors[v + 2], vectors[v + 3]
            )
            if vectors[v] or vectors[v + 1]
            else self._clip_finite(i, points)
        )

    def _clip_finite(
        self,
        i: int,
        points: list[float],
    ) -> tuple[float, float, float, float, float, float]:
        n = len(points)
        P = None
        x0 = None
        y0 = None
        x1 = points[n - 2]
        y1 = points[n - 1]
        c0 = None
        c1 = self._regioncode(x1, y1)
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
            (self.xmin + self.xmax) * 0.5,
            (self.ymin + self.ymax) * 0.5,
        ):
            return [
                self.xmax,
                self.ymin,
                self.xmax,
                self.ymax,
                self.xmin,
                self.ymax,
                self.xmin,
                self.ymin,
            ]
        return P

    def _clip_segment(
        self,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        c0: float,
        c1: float,
    ) -> tuple[float, float, float, float] | None:
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
                x = x0 + (x1 - x0) * (self.ymax - y0) / (y1 - y0)
                y = self.ymax
            elif c & 0b0100:
                x = x0 + (x1 - x0) * (self.ymin - y0) / (y1 - y0)
                y = self.ymin
            elif c & 0b0010:
                y = y0 + (y1 - y0) * (self.xmax - x0) / (x1 - x0)
                x = self.xmax
            else:
                y = y0 + (y1 - y0) * (self.xmin - x0) / (x1 - x0)
                x = self.xmin
            if c0:
                x0 = x
                y0 = y
                c0 = self._regioncode(x0, y0)
            else:
                x1 = x
                y1 = y
                c1 = self._regioncode(x1, y1)

    def _clip_infinite(
        self,
        i: int,
        points: list[float],
        vx0: float,
        vy0: float,
        vxn: float,
        vyn: float,
    ) -> tuple[float, float, float, float, float, float]:
        P = list(points)
        p = self._project(P[0], P[1], vx0, vy0)
        if p:
            P.insert(0, p[1])
            P.insert(0, p[0])
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
        elif self.contains(
            i, (self.xmin + self.xmax) * 0.5, (self.ymin + self.ymax) * 0.5
        ):
            P = [
                self.xmin,
                self.ymin,
                self.xmax,
                self.ymin,
                self.xmax,
                self.ymax,
                self.xmin,
                self.ymax,
            ]
        return P

    def _edge(self, i: int, e0: float, e1: float, P: list[float], j: int) -> int:
        while e0 != e1:
            match e0:
                case 0b0101:
                    e0 = 0b0100
                    continue
                case 0b0100:
                    e0 = 0b0110
                    x = self.xmax
                    y = self.ymin
                case 0b0110:
                    e0 = 0b0010
                    continue
                case 0b0010:
                    e0 = 0b1010
                    x = self.xmax
                    y = self.ymax
                case 0b1010:
                    e0 = 0b1000
                    continue
                case 0b1000:
                    e0 = 0b1001
                    x = self.xmin
                    y = self.ymax
                case 0b1001:
                    e0 = 0b0001
                    continue
                case 0b0001:
                    e0 = 0b0101
                    x = self.xmin
                    y = self.ymin

            if (j >= len(P) or P[j] != x or P[j + 1] != y) and self.contains(i, x, y):
                P.insert(j, x)
                P.insert(j + 1, y)
                j += 2
        return j

    def _project(
        self, x0: float, y0: float, vx: float, vy: float
    ) -> tuple[float, float]:
        t = inf
        if vy < 0:
            if y0 <= self.ymin:
                return None
            c = (self.ymin - y0) / vy
            if c < t:
                y = self.ymin
                t = c
                x = x0 + t * vx
        elif vy > 0:
            if y0 >= self.ymax:
                return None
            c = (self.ymax - y0) / vy
            if c < t:
                y = self.ymax
                t = c
                x = x0 + t * vx

        if vx > 0:
            if x0 >= self.xmax:
                return None
            c = (self.xmax - x0) / vx
            if c < t:
                x = self.xmax
                t = c
                y = y0 + t * vy
        elif vx < 0:
            if x0 <= self.xmin:
                return None
            c = (self.xmin - x0) / vx
            if c < t:
                x = self.xmin
                t = c
                y = y0 + t * vy

        return [x, y]

    def _edgecode(self, x: float, y: float) -> int:
        if x == self.xmin:
            a = 0b0001
        elif x == self.xmax:
            a = 0b0010
        else:
            a = 0b0000

        if y == self.ymin:
            b = 0b0100
        elif y == self.ymax:
            b = 0b1000
        else:
            b = 0b0000

        return a | b

    def _regioncode(self, x: float, y: float) -> int:
        if x < self.xmin:
            a = 0b0001
        elif x > self.xmax:
            a = 0b0010
        else:
            a = 0b0000

        if y < self.ymin:
            b = 0b0100
        elif y > self.ymax:
            b = 0b1000
        else:
            b = 0b0000

        return a | b

    def _simplify(self, P: list[float]) -> list[float] | None:
        if P and len(P) > 4:
            n = len(P)
            i = 0
            while i < n:
                j = (i + 2) % n
                k = (i + 4) % n
                if (
                    P[i] == P[j]
                    and P[j] == P[k]
                    or P[i + 1] == P[j + 1]
                    and P[j + 1] == P[k + 1]
                ):
                    P.pop(j)
                    P.pop(j)
                    n = len(P)
                else:
                    i += 2
            if not n:
                P = None
        return P
