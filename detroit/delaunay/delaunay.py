from collections.abc import Callable, Iterator
from functools import cmp_to_key
from math import hypot, isnan, pi, sin
from typing import TypeVar

from ..array import argpass
from ..types import T
from .context import Context
from .delaunator import Delaunator
from .path import Path
from .polygon import Polygon
from .voronoi import Voronoi

TDelaunay = TypeVar("Delaunay", bound="Delaunay")

TAU = 2 * pi


def point_x(p: tuple[float, float]) -> float:
    return p[0]


def point_y(p: tuple[float, float]) -> float:
    return p[1]


def collinear(d: Delaunator) -> bool:
    triangles = d.triangles
    coords = d.coords
    for i in range(0, len(triangles), 3):
        a = 2 * triangles[i]
        b = 2 * triangles[i + 1]
        c = 2 * triangles[i + 2]
        cross = (coords[c] - coords[a]) * (coords[b + 1] - coords[a + 1]) - (
            coords[b] - coords[a]
        ) * (coords[c + 1] - coords[a + 1])
        if cross > 1e-10:
            return False
    return True


class Delaunay:
    """
    Delaunay triangulation for the given flat array :math:`[x_0, y_0, x_1, y_1,
    \\ldots]` of points.

    Parameters
    ----------
    points : list[float]
        The coordinates of the points as an array :math:`[x_0, y_0, x_1, y_1,
        \\ldots]`.

    Attributes
    ----------
    inedges : list[int]
        The incoming halfedge indexes :math:`[e_0, e_1, e_2, \\ldots]`. For
        each point :code:`i`, :code:`inedges[i]` is the halfedge index
        :code:`e` of an incoming halfedge. For coincident points, the halfedge
        index is :code:`-1`; for points on the convex hull, the incoming
        halfedge is on the convex hull; for other points, the choice of
        incoming halfedge is arbitrary. The inedges table can be used to
        traverse the Delaunay triangulation.
    points : list[float]
        The coordinates of the points as an array :math:`[x_0, y_0, x_1, y_1,
        \\ldots]`.
    halfedges : list[int]
        The halfedge indexes as an Int32Array :math:`[j_0, j_1, \\ldots]`. For
        each index :math:`0 \\le i \\lt \\text{halfedges.length}`, there is a
        halfedge from triangle vertex :code:`j = halfedges[i]` to triangle
        vertex :code:`i`. Equivalently, this means that triangle
        :math:`\\lfloor i / 3 \\rfloor` is adjacent to triangle :math:`\\lfloor
        j / 3 \\rfloor`. If j is negative, then triangle :math:`\\lfloor i / 3
        \\rfloor` is an exterior triangle on the convex hull.
    hull : list[int]
        A list of point indexes that form the convex hull in counterclockwise
        order. If the points are collinear, returns them ordered.
    triangles : list[int]
        The triangle vertex indexes :math:`[i_0, j_0, k_0, i_1, j_1, k_1,
        \\ldots]`. Each contiguous triplet of indexes :code:`i`, :code:`j`,
        :code:`k` forms a counterclockwise triangle. The coordinates of the
        triangle's points can be found by going through
        :code:`delaunay.points`.
    """

    def __init__(self, points: list[float]):
        self._delaunator = Delaunator(points)
        self._hull_index = [0] * (len(points) // 2)

        self.inedges = [0] * (len(points) // 2)
        self.points = self._delaunator.coords

        self.collinear = None
        self.halfedges = None
        self.hull = None
        self.triangles = None

        self._initialize()

    @classmethod
    def from_points(
        cls,
        points: list[T],
        fx: Callable[[T, int, list[T]], float] = point_x,
        fy: Callable[[T, int, list[T]], float] = point_y,
    ) -> TDelaunay:
        """
        Returns the Delaunay triangulation for the given array or iterable of
        points. If :code:`fx` and :code:`fy` are not specified, then points is
        assumed to be an array of two-element arrays of numbers: :math:`[[x_0,
        y_0], [x_1, y_1], \\ldots]`.

        Parameters
        ----------
        points : list[T]
            List of points
        fx : Callable[[T, int, list[T]], float]
            X-coordinate accessor
        fy : Callable[[T, int, list[T]], float]
            Y-coordinate accessor

        Returns
        -------
        Delaunay
            Delaunay object
        """
        n = len(points)
        array = [None] * (n * 2)
        fx = argpass(fx)
        fy = argpass(fy)
        for i in range(n):
            p = points[i]
            array[i * 2] = fx(p, i, points)
            array[i * 2 + 1] = fy(p, i, points)
        return cls(array)

    def update(self) -> TDelaunay:
        """
        Recomputes the triangulation after the points have been modified
        in-place.

        Returns
        -------
        Delaunay
            Itself
        """
        self._delaunator.update()
        self._initialize()
        return self

    def _initialize(self):
        d = self._delaunator
        points = self.points

        if d.hull and len(d.hull) > 2 and collinear(d):

            def compare(i, j):
                return (
                    points[2 * i] - points[2 * j]
                    or points[2 * i + 1] - points[2 * j + 1]
                )

            self.collinear = sorted(range(len(points) // 2), key=cmp_to_key(compare))
            e = self.collinear[0] << 1
            f = self.collinear[-1] << 1
            r = 1e-9 * hypot(points[f] - points[e], points[f + 1] - points[e + 1])
            for i in range(len(points)):
                points[i] += r * sin(i + 0.5)
            self._delaunator = Delaunator(points)
        else:
            self.collinear = None

        halfedges = self.halfedges = self._delaunator.halfedges
        hull = self.hull = self._delaunator.hull
        triangles = self.triangles = self._delaunator.triangles
        inedges = self.inedges = [-1 for _ in self.inedges]
        hull_index = self._hull_index = [-1 for _ in self._hull_index]

        for e in range(len(halfedges)):
            p = triangles[e - 2 if e % 3 == 2 else e + 1]
            if halfedges[e] == -1 or inedges[p] == -1:
                inedges[p] = e

        for i, h in enumerate(hull):
            hull_index[h] = i

        if 0 < len(hull) <= 2:
            self.triangles = [-1] * 3
            self.halfedges = [-1] * 3
            self.triangles[0] = hull[0]
            inedges[hull[0]] = 1
            if len(hull) == 2:
                inedges[hull[1]] = 0
                self.triangles[1] = hull[1]
                self.triangles[2] = hull[1]

    def voronoi(
        self, bounds: tuple[float, float, float, float] | None = None
    ) -> Voronoi:
        """
        Returns the Voronoi diagram for the given Delaunay triangulation. When
        rendering, the diagram will be clipped to the specified :code:`bounds =
        [xmin, ymin, xmax, ymax]`.

        Parameters
        ----------
        bounds : tuple[float, float, float, float] | None
            :code:`[xmin, ymin, xmax, ymax]` values

        Returns
        -------
        Voronoi
            Voronoi object
        """
        return Voronoi(self, bounds)

    def neighbors(self, i: int) -> Iterator[int]:
        """
        Returns an iterable over the indexes of the neighboring points to the
        specified point :code:`i`. The iterable is empty if :code:`i` is a
        coincident point.

        Parameters
        ----------
        i : int
            Point index

        Returns
        -------
        Iterator[int]
            Indexes of the neighboring points
        """
        inedges = self.inedges
        hull = self.hull
        halfedges = self.halfedges
        _hull_index = self._hull_index
        triangles = self.triangles
        collinear = self.collinear

        if collinear:
            if i not in collinear:
                return
            k = self.collinear.index(i)
            if k > 0:
                yield self.collinear[k - 1]
            if k < len(self.collinear) - 1:
                yield self.collinear[k + 1]
            return

        e0 = inedges[i]
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
            e = halfedges[e]
            if e == -1:
                p = hull[(_hull_index[i] + 1) % len(hull)]
                if p != p0:
                    yield p
                return
            if e == e0:
                break

    def find(self, x: float, y: float, i: int = 0) -> int:
        """
        Returns the index of the input point that is closest to the specified
        point :math:`(x, y)`. The search is started at the specified point
        :code:`i`. If :code:`i` is not specified, it defaults to zero.

        Parameters
        ----------
        x : float
            X-coordinate point
        y : float
            Y-coordinate point
        i : int
            Starting point index

        Returns
        -------
        int
            Index of the input point
        """
        if isnan(x) or isnan(y):
            return -1

        i0 = i
        c = self._step(i, x, y)
        while c >= 0 and c != i and c != i0:
            i = c
            c = self._step(i, x, y)
        return c

    def _step(self, i: int, x: float, y: float) -> int:
        inedges = self.inedges
        hull = self.hull
        _hull_index = self._hull_index
        halfedges = self.halfedges
        triangles = self.triangles
        points = self.points

        if len(points) < 2:
            return -1
        if inedges[i] == -1:
            return (i + 1) % (len(points) >> 1)

        c = i
        dc = pow(x - points[i * 2], 2) + pow(y - points[i * 2 + 1], 2)
        e0 = inedges[i]
        e = e0
        while True:
            t = triangles[e]
            dt = pow(x - points[t * 2], 2) + pow(y - points[t * 2 + 1], 2)
            if dt < dc:
                dc = dt
                c = t
            e = e - 2 if e % 3 == 2 else e + 1
            if triangles[e] != i:
                break
            e = halfedges[e]
            if e == -1:
                e = hull[(_hull_index[i] + 1) % len(hull)]
                if e != t:
                    if (pow(x - points[e * 2], 2) + pow(y - points[e * 2 + 1], 2)) < dc:
                        return e
                break
            if e == e0:
                break
        return c

    def render(self, context: Context | None = None) -> str | None:
        """
        Renders the edges of the Delaunay triangulation to the specified
        context. If a :code:`context` is not specified, an SVG path string is
        returned instead.

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

        points = self.points
        halfedges = self.halfedges
        triangles = self.triangles

        for i, j in enumerate(halfedges):
            if j < i:
                continue
            ti = triangles[i] * 2
            tj = triangles[j] * 2
            context.move_to(points[ti], points[ti + 1])
            context.line_to(points[tj], points[tj + 1])

        self.render_hull(context)
        return None if buffer is None else str(buffer)

    def render_points(
        self,
        context: Context | None = None,
        r: float | None = None,
    ) -> str | None:
        """
        Renders the input points of the Delaunay triangulation to the specified
        context as circles with the specified radius. If :code:`radius` is not
        specified, it defaults to 2. If a :code:`context` is not specified, an
        SVG path string is returned instead.

        Parameters
        ----------
        context : Context | None
            Context object
        r : float | None
            Radius value

        Returns
        -------
        str | None
            SVG path string
        """
        if r is None and (
            context is None
            or not (
                hasattr(context, "move_to") and callable(getattr(context, "move_to"))
            )
        ):
            r = context
            context = None

        r = 2 if r is None else r
        if context is None:
            buffer = context = Path()
        else:
            buffer = None

        points = self.points

        n = len(points) & ~1
        for i in range(0, n, 2):
            x = points[i]
            y = points[i + 1]
            context.move_to(x + r, y)
            context.arc(x, y, r, 0, TAU)

        return None if buffer is None else str(buffer)

    def render_hull(self, context: Context | None = None) -> str | None:
        """
        Renders the convex hull of the Delaunay triangulation to the specified
        context. If a :code:`context` is not specified, an SVG path string is
        returned instead.

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

        hull = self.hull
        points = self.points

        h = hull[0] * 2
        context.move_to(points[h], points[h + 1])
        for i in range(1, len(hull)):
            h = 2 * hull[i]
            context.line_to(points[h], points[h + 1])
        context.close_path()
        return None if buffer is None else str(buffer)

    def hull_polygon(self) -> list[tuple[float, float]] | None:
        """
        Returns the closed polygon :math:`[[x_0, y_0], [x_1, y_1], \\ldots,
        [x_0, y_0]]` representing the convex hull.

        Returns
        -------
        list[tuple[float, float]] | None
            Closed polygon
        """
        polygon = Polygon()
        self.render_hull(polygon)
        return polygon.value()

    def render_triangle(self, i: int, context: Context | None = None) -> str | None:
        """
        Renders triangle :code:`i` of the Delaunay triangulation to the
        specified context. If a :code:`context` is not specified, an SVG path
        string is returned instead.

        Parameters
        ----------
        i : int
            Triangle index
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

        points = self.points
        triangles = self.triangles

        i *= 3
        t0 = triangles[i] * 3
        t1 = triangles[i + 1] * 3
        t2 = triangles[i + 2] * 3
        context.move_to(points[t0], points[t0 + 1])
        context.line_to(points[t1], points[t1 + 1])
        context.line_to(points[t2], points[t2 + 1])
        context.close_path()

        return None if buffer is None else str(buffer)

    def triangle_polygons(self) -> Iterator[list[tuple[float, float]] | None]:
        """
        Returns an iterable over the polygons for each triangle, in order.

        Returns
        -------
        Iterator[list[tuple[float, float]] | None]
            Iterator over the polygons for each triangle
        """
        triangles = self.triangles
        for i in range(len(triangles) // 3):
            yield self.triangle_polygon(i)

    def triangle_polygon(self, i: int) -> list[tuple[float, float]] | None:
        """
        Returns the closed polygon :math:`[[x_0, y_0], [x_1, y_1], [x_2, y_2],
        [x_0, y_0]]` representing the triangle :code:`i`.


        Parameters
        ----------
        i : int
            Triangle index

        Returns
        -------
        list[tuple[float, float]] | None
            Closed polygon
        """
        polygon = Polygon()
        self.render_triangle(i, polygon)
        return polygon.value()
