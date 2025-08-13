import math

from .string_round import string_round

TAU = 2 * math.pi
EPSILON = 1e-6
TAU_EPSILON = TAU - EPSILON


class Path:
    """
    Builds a path serializer

    Parameters
    ----------
    digits : int | None
        Number of digits to round

    Returns
    -------
    Path
        New path serializer
    """

    def __init__(self, digits: int | None = None):
        self.digit = digits or 3
        self._x0 = self._y0 = 0  # start of current subpath
        self._x1 = self._y1 = None  # end of current subpath
        self._string = ""

    def _round(self, *values):
        return (string_round(value, self.digit) for value in values)

    def move_to(self, x: int | float, y: int | float):
        """
        Move to the specified point (x, y).

        Parameters
        ----------
        x : int | float
            x position
        y : int | float
            y position
        """
        self._x0 = self._x1 = x
        self._y0 = self._y1 = y
        x, y = self._round(x, y)
        self._string += f"M{x},{y}"

    def close_path(self):
        """
        Ends the current subpath and causes an automatic straight line to be
        drawn from the current point to the initial point of the current
        subpath.
        """
        if self._x1 is not None:
            self._x1, self._y1 = self._x0, self._y0
            self._string += "Z"

    def line_to(self, x: int | float, y: int | float):
        """
        Draws a straight line from the current point to the specified point (x,
        y).

        Parameters
        ----------
        x : int | float
            x position
        y : int | float
            y position
        """
        self._x1 = x
        self._y1 = y
        x, y = self._round(x, y)
        self._string += f"L{x},{y}"

    def quadratic_curve_to(
        self, cpx: int | float, cpy: int | float, x: int | float, y: int | float
    ):
        """
        Draws a quadratic Bézier segment from the current point to the
        specified point (x, y), with the specified control point (cpx, cpy).

        Parameters
        ----------
        cpx : int | float
            Specified control x position
        cpy : int | float
            Specified control y position
        x : int | float
            x position
        y : int | float
            y position
        """
        self._x1 = x
        self._y1 = y
        x, y, cpx, cpy = self._round(x, y, cpx, cpy)
        self._string += f"Q{cpx},{cpy},{x},{y}"

    def bezier_curve_to(
        self,
        cpx1: int | float,
        cpy1: int | float,
        cpx2: int | float,
        cpy2: int | float,
        x: int | float,
        y: int | float,
    ):
        """
        Draws a cubic Bézier segment from the current point to the specified
        point (x, y), with the specified control points (cpx1, cpy1) and (cpx2,
        cpy2).

        Parameters
        ----------
        cpx1 : int | float
            Specified control x position 1
        cpy1 : int | float
            Specified control y position 1
        cpx2 : int | float
            Specified control x position 2
        cpy2 : int | float
            Specified control y position 2
        x : int | float
            x position
        y : int | float
            y position
        """
        self._x1 = x
        self._y1 = y
        x, y, cpx1, cpy1, cpx2, cpy2 = self._round(x, y, cpx1, cpy1, cpx2, cpy2)
        self._string += f"C{cpx1},{cpy1},{cpx2},{cpy2},{x},{y}"

    def arc_to(
        self,
        x1: int | float,
        y1: int | float,
        x2: int | float,
        y2: int | float,
        r: int | float,
    ):
        """
        Draws a circular arc segment with the specified radius that starts
        tangent to the line between the current point and the specified point
        (x1, y1) and ends tangent to the line between the specified points (x1,
        y1) and (x2, y2). If the first tangent point is not equal to the
        current point, a straight line is drawn between the current point and
        the first tangent point.

        Parameters
        ----------
        x1 : int | float
            Arc x position
        y1 : int | float
            Arc y position
        x2 : int | float
            Tangent x position
        y2 : int | float
            Tangent y position
        r : int | float
            Arc radius
        """
        # Is the radius negative? Error.
        if r < 0:
            raise ValueError(f"negative radius: {r}")

        x0, y0 = self._x1 or 0, self._y1 or 0
        x21, y21 = x2 - x1, y2 - y1
        x01, y01 = x0 - x1, y0 - y1
        l01_2 = x01 * x01 + y01 * y01

        # Is this path empty? Move to (x1,y1).
        if self._x1 is None:
            self._x1 = x1
            self._y1 = y1
            self._string += f"M{x1},{y1}"

        # Or, is (x1,y1) coincident with (x0,y0)? Do nothing.
        elif not (l01_2 > EPSILON):
            pass

        # Or, are (x0,y0), (x1,y1) and (x2,y2) collinear?
        # Equivalently, is (x1,y1) coincident with (x2,y2)?
        # Or, is the radius zero? Line to (x1,y1).
        elif not (abs(y01 * x21 - y21 * x01) > EPSILON) or not r:
            self._x1 = int(x1)
            self._y1 = int(y1)
            self._string += f"L{x1},{y1}"

        # Otherwise, draw an arc!
        else:
            x20, y20 = x2 - x0, y2 - y0
            l21_2 = x21 * x21 + y21 * y21
            l20_2 = x20 * x20 + y20 * y20
            l21 = math.sqrt(l21_2)
            l01 = math.sqrt(l01_2)
            l = r * math.tan(
                (math.pi - math.acos((l21_2 + l01_2 - l20_2) / (2 * l21 * l01))) / 2
            )
            t01 = l / l01
            t21 = l / l21

            # If the start tangent is not coincident with (x0,y0), line to.
            if abs(t01 - 1) > EPSILON:
                a1, a2 = self._round(x1 + t01 * x01, y1 + t01 * y01)
                self._string += f"L{a1},{a2}"

            m1 = int(y01 * x20 > x01 * y20)
            self._x1 = x1 + t21 * x21
            self._y1 = y1 + t21 * y21
            m2, m3 = self._round(self._x1, self._y1)
            self._string += f"A{r},{r},0,0,{m1},{m2},{m3}"

    def arc(
        self,
        x: int | float,
        y: int | float,
        r: int | float,
        start_angle: int | float,
        end_angle: int | float,
        ccw: bool = False,
    ):
        """
        Draws a circular arc segment with the specified center (x, y), radius,
        start_angle and end_angle. If anticlockwise is true, the arc is drawn
        in the anticlockwise direction; otherwise, it is drawn in the clockwise
        direction. If the current point is not equal to the starting point of
        the arc, a straight line is drawn from the current point to the start
        of the arc.

        Parameters
        ----------
        x : int | float
            Center x position
        y : int | float
            Center y position
        r : int | float
            Radius
        start_angle : int | float
            Start angle
        end_angle : int | float
            End angle
        ccw : bool
            Clockwise direction
        """
        # Is the radius negative? Error.
        if r < 0:
            raise ValueError(f"negative radius: {r}")

        a0 = start_angle
        a1 = end_angle
        dx = r * math.cos(a0)
        dy = r * math.sin(a0)
        x0 = x + dx
        y0 = y + dy
        cw = 1 ^ bool(ccw)
        da = a0 - a1 if ccw else a1 - a0

        # Is this path empty? Move to (x0, y0).
        if self._x1 is None:
            t1, t2 = self._round(x0, y0)
            self._string += f"M{t1},{t2}"

        # Or, is (x0,y0) not coincident with the previous point? Line to (x0,y0).
        elif abs(self._x1 - x0) > EPSILON or abs(self._y1 - y0) > EPSILON:
            t1, t2 = self._round(x0, y0)
            self._string += f"L{t1},{t2}"

        # Is this arc empty? We're done.
        if not r:
            return

        # Does the angle go the wrong way ? Flip the direction.
        if da < 0:
            new_da = da % TAU
            da = new_da if new_da else new_da + TAU

        # Is this a complete circle? Draw two arcs to complete the circle.
        if da > TAU_EPSILON:
            self._x1 = x0
            self._y1 = y0
            r, x0, y0, ddx, ddy = self._round(r, x0, y0, x - dx, y - dy)
            self._string += f"A{r},{r},0,1,{cw},{ddx},{ddy}A{r},{r},0,1,{cw},{x0},{y0}"

        # Is this arc non-empty? Draw an arc!
        elif da > EPSILON:
            self._x1 = x + r * math.cos(a1)
            self._y1 = y + r * math.sin(a1)
            r, x1, y1 = self._round(r, self._x1, self._y1)
            self._string += f"A{r},{r},0,{int(da >= math.pi)},{cw},{x1},{y1}"

    def rect(self, x: int | float, y: int | float, w: int | float, h: int | float):
        """
        Creates a new subpath containing just the four points (x, y), (x + w,
        y), (x + w, y + h), (x, y + h), with those four points connected by
        straight lines, and then marks the subpath as closed.

        Parameters
        ----------
        x : int | float
            Rectangle x position
        y : int | float
            Rectangle y position
        w : int | float
            Rectangle width
        h : int | float
            Rectangle height
        """
        self._x0 = self._x1 = x
        self._y0 = self._y1 = y
        x, y, w, h = self._round(x, y, w, h)
        self._string += f"M{x},{y}h{w}v{h}h-{w}Z"

    def __str__(self) -> str:
        return self._string
