from collections.abc import Callable
from math import cosh, dist, exp, log, sinh, sqrt, tanh
from typing import TypeVar

EPSILON = 1e-12
SQRT2 = sqrt(2)

TZoomRho = TypeVar("ZoomRho", bound="ZoomRho")


class Base:
    def __init__(self, rho, p0, p1):
        ux0, uy0, w0 = p0
        ux1, uy1, w1 = p1
        dx = ux1 - ux0
        dy = uy1 - uy0
        self.rho = rho
        self.ux0 = ux0
        self.uy0 = uy0
        self.w0 = w0
        self.w1 = w1
        self.dx = dx
        self.dy = dy
        self.d2 = dx * dx + dy * dy


class SingularZoomRhoInterpolator(Base):
    def __init__(self, rho, rho2, rho4, p0, p1):
        super().__init__(rho, p0, p1)
        w0 = self.w0
        w1 = self.w1
        self.s = log(w1 / w0) / rho
        self.duration = self.s * 1000 * rho / SQRT2

    def __call__(self, t):
        return [
            self.ux0 + t * self.dx,
            self.uy0 + t * self.dy,
            self.w0 * exp(self.rho * t * self.s),
        ]


class GeneralZoomRhoInterpolator(Base):
    def __init__(self, rho, rho2, rho4, p0, p1):
        super().__init__(rho, p0, p1)
        d2 = self.d2
        w0 = self.w0
        w1 = self.w1

        self.rho2 = rho2
        self.d1 = d1 = sqrt(d2)

        b0 = (w1 * w1 - w0 * w0 + rho4 * d2) / (2 * w0 * rho2 * d1)
        b1 = (w1 * w1 - w0 * w0 - rho4 * d2) / (2 * w1 * rho2 * d1)
        self.r0 = r0 = log(sqrt(b0 * b0 + 1) - b0)
        self.r1 = r1 = log(sqrt(b1 * b1 + 1) - b1)

        self.s = (r1 - r0) / rho
        self.duration = self.s * 1000 * self.rho / SQRT2

    def __call__(self, t):
        c = self.w0 / (self.rho2 * self.d1)
        u = c * (cosh(self.r0) * tanh(self.rho * t * self.s + self.r0) - sinh(self.r0))
        return [
            self.ux0 + u * self.dx,
            self.uy0 + u * self.dy,
            self.w0 * cosh(self.r0) / cosh(self.rho * t * self.s + self.r0),
        ]


class ZoomRho:
    """
    An interpolator for zooming smoothly between two views of a two-dimensional
    plane based on "Smooth and efficient zooming and panning" by Jarke J. van
    Wijk and Wim A.A. Nuij.

    Each view is defined as an array of three numbers: cx, cy and width. The
    first two coordinates cx, cy represent the center of the viewport; the last
    coordinate width represents the size of the viewport.


    Parameters
    ----------
    a : list[float]
        View a
    b : list[float]
        View b

    Returns
    -------
    Callable[[float], float]
        Interpolator function

    Examples
    --------

    >>> interpolator = d3.interpolate_zoom([0, 0, 1], [10, 10, 5])
    >>> interpolator(0)
    [0.0, 0.0, 1.0]
    >>> interpolator(1)
    [10.00000000000023, 10.00000000000023, 5.0000000000001155]
    >>> interpolator(0.5)
    [1.666666666666673, 1.666666666666673, 10.775486583496573]
    """

    def __init__(self, rho, rho2, rho4):
        self.rho = rho
        self.rho2 = rho2
        self.rho4 = rho4

    def __call__(self, a: list[float], b: list[float]) -> Callable[[float], float]:
        """
        Returns an interpolator between the two views a and b. Each view is
        defined as an array of three numbers: cx, cy and width. The first two
        coordinates cx, cy represent the center of the viewport; the last
        coordinate width represents the size of the viewport.

        Parameters
        ----------
        a : list[float]
            View a
        b : list[float]
            View b

        Returns
        -------
        Callable[[float], float]
            Interpolator function
        """
        d = dist(a[:-1], b[:-1]) ** 2
        interpolator = (
            SingularZoomRhoInterpolator if d < EPSILON else GeneralZoomRhoInterpolator
        )
        return interpolator(self.rho, self.rho2, self.rho4, a, b)

    def set_rho(self, rho: float) -> TZoomRho:
        """
        Sets rho value and returns itself. When :code:`rho` is closed to 0, the
        interpolator is almost linear.

        Parameters
        ----------
        rho : float
            Rho value

        Returns
        -------
        ZoomRho
            Itself
        """
        new_rho = max(1e-3, float(rho))
        return ZoomRho(new_rho, new_rho * new_rho, new_rho**4)


interpolate_zoom = ZoomRho(SQRT2, 2, 4)
