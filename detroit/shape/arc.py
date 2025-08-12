from collections.abc import Callable
from math import acos, asin, atan2, cos, nan, pi, sin, sqrt
from typing import TypeVar

from ..selection.selection import Selection
from .constant import constant
from .path import WithPath

TArc = TypeVar("Arc", bound="Arc")

EPSILON = 1e-12


def arc_inner_radius(d, *args):
    return d.get("inner_radius", 0)


def arc_outer_radius(d, *args):
    return d.get("outer_radius", 0)


def arc_start_angle(d, *args):
    return d.get("start_angle", 0)


def arc_end_angle(d, *args):
    return d.get("end_angle", 0)


def arc_pad_angle(d={}, *args):
    return d.get("pad_angle", 0)


def intersect(x0, y0, x1, y1, x2, y2, x3, y3):
    x10 = x1 - x0
    y10 = y1 - y0
    x32 = x3 - x2
    y32 = y3 - y2
    t = y32 * x10 - x32 * y10
    if t * t < EPSILON:
        return
    t = (x32 * (y0 - y2) - y32 * (x0 - x2)) / t
    return x0 + t * x10, y0 + t * y10


class CornerTangents:
    def __init__(self, x0, y0, x1, y1, r1, rc, cw):
        x01 = x0 - x1
        y01 = y0 - y1
        lo = (rc if cw else -rc) / sqrt(x01 * x01 + y01 * y01)
        ox = lo * y01
        oy = -lo * x01
        x11 = x0 + ox
        y11 = y0 + oy
        x10 = x1 + ox
        y10 = y1 + oy
        x00 = (x11 + x10) / 2
        y00 = (y11 + y10) / 2
        dx = x10 - x11
        dy = y10 - y11
        d2 = dx * dx + dy * dy
        r = r1 - rc
        D = x11 * y10 - x10 * y11
        d = (-1 if dy < 0 else 1) * sqrt(max(0, r * r * d2 - D * D))
        cx0 = (D * dy - dx * d) / d2
        cy0 = (-D * dx - dy * d) / d2
        cx1 = (D * dy + dx * d) / d2
        cy1 = (-D * dx + dy * d) / d2
        dx0 = cx0 - x00
        dy0 = cy0 - y00
        dx1 = cx1 - x00
        dy1 = cy1 - y00

        if dx0 * dx0 + dy0 * dy0 > dx1 * dx1 + dy1 * dy1:
            cx0 = cx1
            cy0 = cy1

        self.cx = cx0
        self.cy = cy0
        self.x01 = -ox
        self.y01 = -oy
        self.x11 = cx0 * (r1 / r - 1)
        self.y11 = cy0 * (r1 / r - 1)


class Arc(WithPath):
    """
    The arc generator produces a circular or annular sector,
    as in a pie or donut chart. Arcs are centered at the origin;
    use a transform to move the arc to a different position

    Examples
    --------

    >>> from math import pi
    >>> arc = d3.arc()
    ...     .set_inner_radius(0)
    ...     .set_outer_radius(100)
    ...     .set_start_angle(0)
    ...     .set_end_angle(pi / 2)
    """

    def __init__(self):
        super().__init__()
        self._inner_radius = arc_inner_radius
        self._outer_radius = arc_outer_radius
        self._corner_radius = constant(0)
        self._pad_radius = None
        self._start_angle = arc_start_angle
        self._end_angle = arc_end_angle
        self._pad_angle = arc_pad_angle
        self._context = None

    def __call__(self, *args) -> str | None:
        """
        Generates an arc for the given arguments. The arguments
        are arbitrary; they are propagated to the arc generator's
        accessor functions along with the this object.

        Parameters
        ----------
        args : Any
            Additional arguments

        Returns
        -------
        str | None
            Generated arc if the arc is not associated to a context

        Examples
        --------

        >>> from math import pi
        >>> d3.arc()
        ...     .set_inner_radius(0)
        ...     .set_outer_radius(100)
        ...     .set_start_angle(0)
        ...     .set_end_angle(pi / 2)()
        """
        r0 = self._inner_radius(*args)
        r1 = self._outer_radius(*args)
        a0 = self._start_angle(*args) - pi * 0.5
        a1 = self._end_angle(*args) - pi * 0.5
        da = abs(a1 - a0)
        cw = a1 > a0

        buffer = None
        if self._context is None:
            self._context = buffer = self._path()

        if r1 < r0:
            r = r1
            r1 = r0
            r0 = r

        if r1 <= EPSILON:
            self._context.move_to(0, 0)
        elif da > 2 * pi - EPSILON:
            self._context.move_to(r1 * cos(a0), r1 * sin(a0))
            self._context.arc(0, 0, r1, a0, a1, not cw)
            if r0 > EPSILON:
                self._context.move_to(r0 * cos(a1), r0 * sin(a1))
                self._context.arc(0, 0, r0, a1, a0, cw)
        else:
            a01 = a0
            a11 = a1
            a00 = a0
            a10 = a1
            da0 = da
            da1 = da
            ap = self._pad_angle(*args) / 2
            rp = (
                self._pad_radius(*args)
                if self._pad_radius
                else sqrt(r0 * r0 + r1 * r1)
                if ap > EPSILON
                else 0
            )
            rc = min(abs(r1 - r0) / 2, self._corner_radius(*args))
            rc0 = rc
            rc1 = rc

            if rp > EPSILON:
                tmp = rp / r0 * sin(ap) if r0 != 0 else nan
                p0 = asin(tmp) if 0 <= tmp <= 1 else nan
                p1 = asin(rp / r1 * sin(ap))

                da0 -= p0 * 2
                if da0 > EPSILON:
                    p0 *= 1 if cw else -1
                    a00 += p0
                    a10 -= p0
                else:
                    da0 = 0
                    a00 = a10 = (a0 + a1) / 2

                da1 -= p1 * 2
                if da1 > EPSILON:
                    p1 *= 1 if cw else -1
                    a01 += p1
                    a11 -= p1
                else:
                    da1 = 0
                    a01 = a11 = (a0 + a1) / 2

            x01 = r1 * cos(a01)
            y01 = r1 * sin(a01)
            x10 = r0 * cos(a10)
            y10 = r0 * sin(a10)

            if rc > EPSILON:
                x11 = r1 * cos(a11)
                y11 = r1 * sin(a11)
                x00 = r0 * cos(a00)
                y00 = r0 * sin(a00)

                if da < pi:
                    if oc := intersect(x01, y01, x00, y00, x11, y11, x10, y10):
                        ax = x01 - oc[0]
                        ay = y01 - oc[1]
                        bx = x11 - oc[0]
                        by = y11 - oc[1]
                        kc = 1 / sin(
                            acos(
                                (ax * bx + ay * by)
                                / (sqrt(ax * ax + ay * ay) * sqrt(bx * bx + by * by))
                            )
                            / 2
                        )
                        lc = sqrt(oc[0] * oc[0] + oc[1] * oc[1])
                        rc0 = min(rc, (r0 - lc) / (kc - 1))
                        rc1 = min(rc, (r1 - lc) / (kc + 1))
                    else:
                        rc0 = rc1 = 0

            if da1 <= EPSILON:
                self._context.move_to(x01, y01)
            elif rc1 > EPSILON:
                t0 = CornerTangents(x00, y00, x01, y01, r1, rc1, cw)
                t1 = CornerTangents(x11, y11, x10, y10, r1, rc1, cw)
                self._context.move_to(t0.cx + t0.x01, t0.cy + t0.y01)

                if rc1 < rc:
                    self._context.arc(
                        t0.cx,
                        t0.cy,
                        rc1,
                        atan2(t0.y01, t0.x01),
                        atan2(t1.y01, t1.x01),
                        not cw,
                    )
                else:
                    self._context.arc(
                        t0.cx,
                        t0.cy,
                        rc1,
                        atan2(t0.y01, t0.x01),
                        atan2(t0.y11, t0.x11),
                        not cw,
                    )
                    self._context.arc(
                        0,
                        0,
                        r1,
                        atan2(t0.cy + t0.y11, t0.cx + t0.x11),
                        atan2(t1.cy + t1.y11, t1.cx + t1.x11),
                        not cw,
                    )
                    self._context.arc(
                        t1.cx,
                        t1.cy,
                        rc1,
                        atan2(t1.y11, t1.x11),
                        atan2(t1.y01, t1.x01),
                        not cw,
                    )
            else:
                self._context.move_to(x01, y01)
                self._context.arc(0, 0, r1, a01, a11, not cw)

            if r0 <= EPSILON or da0 <= EPSILON:
                self._context.line_to(x10, y10)
            elif rc0 > EPSILON:
                t0 = CornerTangents(x10, y10, x11, y11, r0, -rc0, cw)
                t1 = CornerTangents(x01, y01, x00, y00, r0, -rc0, cw)

                self._context.line_to(t0.cx + t0.x01, t0.cy + t0.y01)

                if rc0 < rc:
                    self._context.arc(
                        t0.cx,
                        t0.cy,
                        rc0,
                        atan2(t0.y01, t0.x01),
                        atan2(t1.y01, t1.x01),
                        not cw,
                    )
                else:
                    self._context.arc(
                        t0.cx,
                        t0.cy,
                        rc0,
                        atan2(t0.y01, t0.x01),
                        atan2(t0.y11, t0.x11),
                        not cw,
                    )
                    self._context.arc(
                        0,
                        0,
                        r0,
                        atan2(t0.cy + t0.y11, t0.cx + t0.x11),
                        atan2(t1.cy + t1.y11, t1.cx + t1.x11),
                        cw,
                    )
                    self._context.arc(
                        t1.cx,
                        t1.cy,
                        rc0,
                        atan2(t1.y11, t1.x11),
                        atan2(t1.y01, t1.x01),
                        not cw,
                    )
            else:
                self._context.arc(0, 0, r0, a10, a00, cw)

        self._context.close_path()
        if buffer is not None:
            self._context = None
            return str(buffer) or None

    def centroid(self, *args) -> tuple[float, float]:
        """
        Computes the midpoint [x, y] of the center line of
        the arc that would be generated by the given arguments.

        Parameters
        ----------
        args : Any
            Additional arguments

        Returns
        -------
        tuple[float, float]
            Midpoint coordinates
        """
        r = (self._inner_radius(*args) + self._outer_radius(*args)) * 0.5
        a = (self._start_angle(*args) + self._end_angle(*args)) * 0.5 - pi * 0.5
        return cos(a) * r, sin(a) * r

    def set_inner_radius(
        self, inner_radius: Callable[..., float] | float | int
    ) -> TArc:
        """
        If radius is specified, sets the inner radius to the specified
        function or number and returns this arc generator.

        Parameters
        ----------
        inner_radius : Callable[..., float] | float | int
            Inner radius

        Returns
        -------
        Arc
            Itself
        """
        if callable(inner_radius):
            self._inner_radius = inner_radius
        else:
            self._inner_radius = constant(inner_radius)
        return self

    def set_outer_radius(
        self, outer_radius: Callable[..., float] | float | int
    ) -> TArc:
        """
        If radius is specified, sets the outer radius to the specified
        function or number and returns this arc generator.

        Parameters
        ----------
        outer_radius : Callable[..., float] | float | int
            Outer radius

        Returns
        -------
        Arc
            Itself
        """
        if callable(outer_radius):
            self._outer_radius = outer_radius
        else:
            self._outer_radius = constant(outer_radius)
        return self

    def set_corner_radius(
        self, corner_radius: Callable[..., float] | float | int
    ) -> TArc:
        """
        If angle is specified, sets the corner angle to the specified
        function or number and returns this arc generator.

        Parameters
        ----------
        corner_radius : Callable[..., float] | float | int
            Corner radius

        Returns
        -------
        Arc
            Itself
        """
        if callable(corner_radius):
            self._corner_radius = corner_radius
        else:
            self._corner_radius = constant(corner_radius)
        return self

    def set_pad_radius(
        self, pad_radius: Callable[..., float] | float | int | None = None
    ) -> TArc:
        """
        If angle is specified, sets the pad radius to the specified
        function or number and returns this arc generator.

        Parameters
        ----------
        pad_radius : Callable[..., float] | float | int | None
            Pad radius

        Returns
        -------
        Arc
            Itself
        """
        if pad_radius is None:
            self._pad_radius = None
        elif callable(pad_radius):
            self._pad_radius = pad_radius
        else:
            self._pad_radius = constant(pad_radius)
        return self

    def set_start_angle(self, start_angle: Callable[..., float] | float | int) -> TArc:
        """
        If angle is specified, sets the start angle to the specified
        function or number and returns this arc generator.

        Parameters
        ----------
        start_angle : Callable[..., float] | float | int
            Start angle

        Returns
        -------
        Arc
            Itself
        """
        if callable(start_angle):
            self._start_angle = start_angle
        else:
            self._start_angle = constant(start_angle)
        return self

    def set_end_angle(self, end_angle: Callable[..., float] | float | int) -> TArc:
        """
        If angle is specified, sets the end angle to the specified
        function or number and returns this arc generator.

        Parameters
        ----------
        end_angle : Callable[..., float] | float | int
            End angle

        Returns
        -------
        Arc
            Itself
        """
        if callable(end_angle):
            self._end_angle = end_angle
        else:
            self._end_angle = constant(end_angle)
        return self

    def set_pad_angle(self, pad_angle: Callable[..., float] | float | int) -> TArc:
        """
        If angle is specified, sets the pad angle to the specified
        function or number and returns this arc generator.

        Parameters
        ----------
        pad_angle : Callable[..., float] | float | int
            Pad angle

        Returns
        -------
        Arc
            Itself
        """
        if callable(pad_angle):
            self._pad_angle = pad_angle
        else:
            self._pad_angle = constant(pad_angle)
        return self

    def set_context(self, context: Selection | None = None) -> TArc:
        """
        If context is specified, sets the context and
        returns this arc generator.

        Parameters
        ----------
        context : Selection | None
            Context

        Returns
        -------
        Arc
            Itself
        """
        self._context = context
        return self

    def get_inner_radius(self) -> Callable[..., float]:
        return self._inner_radius

    def get_outer_radius(self) -> Callable[..., float]:
        return self._outer_radius

    def get_corner_radius(self) -> Callable[..., float]:
        return self._corner_radius

    def get_pad_radius(self) -> Callable[..., float]:
        return self._pad_radius

    def get_pad_angle(self) -> Callable[..., float]:
        return self._pad_angle

    def get_context(self) -> Selection:
        return self._context
