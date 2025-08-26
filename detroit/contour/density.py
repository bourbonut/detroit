from collections.abc import Callable
from math import floor, isnan, log, sqrt, ulp
from operator import itemgetter
from typing import Generic, TypeVar

from ..array import argpass, blur2, ticks
from ..types import Accessor, MultiPolygonGeoJSON, Point2D, T
from .constant import constant
from .contours import Contours

TDensity = TypeVar("Density", bound="Density")

default_x = itemgetter(0)
default_y = itemgetter(1)


def default_weight() -> float:
    """
    Default weight function

    Returns
    -------
    float
        Output value :code:`1`
    """
    return 1


class Contour:
    """
    Class used to compute an arbitrary contour without needing to recompute the
    underlying grid.

    Parameters
    ----------
    values : list[float]
        Computed grid values
    contours : Contours
        Contours class
    pow4k : float
        Computed constant value
    transform : Callable[[GeoJSON], GeoJSON]
        Transform function
    """

    def __init__(
        self,
        values: list[float],
        contours: Contours,
        pow4k: float,
        transform: Callable[[MultiPolygonGeoJSON], MultiPolygonGeoJSON],
    ):
        self._values = values
        self._contours = contours
        self._pow4k = pow4k
        self._transform = transform

    def __call__(self, value: float) -> MultiPolygonGeoJSON:
        """
        Compute an arbitrary contour without needing to recompute the
        underlying grid.

        Parameters
        ----------
        value : float
            Threshold value

        Returns
        -------
        GeoJSON
            GeoJSON MultiPolygon geometry object
        """
        c = self._transform(self._contours.contour(self._values, value * self._pow4k))
        c["value"] = value
        return c

    def max(self) -> float:
        """
        Computes the maximum density of the grid.

        Returns
        -------
        float
            Maximum density of the grid
        """
        return max(self._values) / self._pow4k


class Density(Generic[T]):
    """
    Constructs a new density estimator with the default settings.
    """

    def __init__(self):
        self._x = argpass(default_x)
        self._y = argpass(default_y)
        self._weight = argpass(default_weight)
        self._dx = 960
        self._dy = 500
        self._r = 20
        self._k = 2
        self._o = self._r * 3
        self._n = (self._dx + self._o * 2) >> self._k
        self._m = (self._dy + self._o * 2) >> self._k
        self._threshold = constant(20)

    def _grid(self, data: list[T]) -> list[float]:
        """
        Computes density values given data input.

        Parameters
        ----------
        data : list[T]
            Data input

        Returns
        -------
        list[float]
            Grid values
        """
        values = [0.0] * (self._n * self._m)
        pow2k = pow(2, -self._k)
        i = -1

        for d in data:
            xi = (self._x(d, i, data) + self._o) * pow2k
            i += 1
            yi = (self._y(d, i, data) + self._o) * pow2k
            wi = self._weight(d, i, data)
            if (
                wi
                and not isnan(wi)
                and xi >= 0.0
                and xi < self._n
                and yi >= 0.0
                and yi < self._m
            ):
                x0 = floor(xi)
                y0 = floor(yi)
                xt = xi - x0 - 0.5
                yt = yi - y0 - 0.5
                values[x0 + y0 * self._n] += (1 - xt) * (1 - yt) * wi
                values[x0 + 1 + y0 * self._n] += xt * (1 - yt) * wi
                values[x0 + 1 + (y0 + 1) * self._n] += xt * yt * wi
                values[x0 + (y0 + 1) * self._n] += (1 - xt) * yt * wi

        blur2({"data": values, "width": self._n, "height": self._m}, self._r * pow2k)
        return values

    def __call__(self, data: list[T]) -> list[MultiPolygonGeoJSON]:
        """
        Estimates the density contours for the given array of data, returning
        an array of GeoJSON MultiPolygon geometry objects.

        Parameters
        ----------
        data : list[T]
            Data input

        Returns
        -------
        list[GeoJSON]
            List of GeoJSON MultiPolygon geometry objects
        """
        values = self._grid(data)
        tz = self._threshold(values)
        pow4k = pow(2, 2 * self._k)

        if not isinstance(tz, list):
            max_values = max(values)
            tz = ticks(ulp(0.0), max_values / pow4k, tz) if max_values != 0.0 else []

        density = (
            Contours()
            .set_size([self._n, self._m])
            .set_thresholds(list(map(lambda d: d * pow4k, tz)))(values)
        )

        def transform(pair: tuple[int, MultiPolygonGeoJSON]) -> MultiPolygonGeoJSON:
            i, c = pair
            c["value"] = tz[i]
            return self._transform(c)

        return list(map(transform, enumerate(density)))

    def contours(self, data: list[T]) -> Contour:
        """
        Return a :class:`Contour <detroit.contour.density.Contour>` callable
        class that can be used to compute an arbitrary contour on the given
        data without needing to recompute the underlying grid. The returned
        contour class also exposes a :func:`Contour.max
        <detroit.contour.density.Contour.max>` value which represents the
        maximum density of the grid.

        Parameters
        ----------
        data : list[T]
            Data input

        Returns
        -------
        Contour
            Callable class
        """
        contours = Contours().set_size([self._n, self._m])
        values = self._grid(data)
        pow4k = pow(2, 2 * self._k)
        return Contour(values, contours, pow4k, self._transform)

    def _transform(self, geometry: MultiPolygonGeoJSON) -> MultiPolygonGeoJSON:
        """
        Transforms each coordinate of the geometry given density values.

        Parameters
        ----------
        geometry : GeoJSON
            Geometry

        Returns
        -------
        GeoJSON
            Transformed geometry
        """
        for coordinates in geometry["coordinates"]:
            self._transform_polygon(coordinates)
        return geometry

    def _transform_polygon(self, coordinates: list[list[Point2D]]):
        """
        Transforms a polygon of a geometry given density values.

        Parameters
        ----------
        coordinates : list[list[Point2D]]
            Polygon coordinates
        """
        for ring in coordinates:
            self._transform_ring(ring)

    def _transform_ring(self, ring: list[Point2D]):
        """
        Transforms a ring of a polygon given density values.

        Parameters
        ----------
        ring : list[Point2D]
            Ring coordinates
        """
        for point in ring:
            self._transform_point(point)

    def _transform_point(self, coordinates: Point2D):
        """
        Transforms a 2D point given density values.

        Parameters
        ----------
        coordinates : Point2D
            2D point coordinates
        """
        coordinates[0] = coordinates[0] * pow(2, self._k) - self._o
        coordinates[1] = coordinates[1] * pow(2, self._k) - self._o

    def _resize(self) -> TDensity:
        """
        Recomputes density values from updated attributes and returns itself.

        Returns
        -------
        Density
            Itself
        """
        self._o = self._r * 3
        self._n = int(self._dx + self._o * 2) >> self._k
        self._m = int(self._dy + self._o * 2) >> self._k
        return self

    def x(self, x: Accessor[T, float] | float) -> TDensity:
        """
        Sets the x coordinate accessor and returns itself.

        Parameters
        ----------
        x : Accessor[T, float] | float
            X accessor or constant value

        Returns
        -------
        Density
            Itself
        """
        if callable(x):
            self._x = argpass(x)
        else:
            self._x = argpass(constant(x))
        return self

    def y(self, y: Accessor[T, float] | float) -> TDensity:
        """
        Sets the y coordinate accessor and returns itself.

        Parameters
        ----------
        y : Accessor[T, float] | float
            Y accessor or constant value

        Returns
        -------
        Density
            Itself
        """
        if callable(y):
            self._y = argpass(y)
        else:
            self._y = argpass(constant(y))
        return self

    def set_weight(self, weight: Accessor[T, float] | float) -> TDensity:
        """
        Sets the weight accessor and returns itself.

        Parameters
        ----------
        x : Accessor[T, float] | float
            Weight accessor or constant value

        Returns
        -------
        Density
            Itself
        """
        if callable(weight):
            self._weight = argpass(weight)
        else:
            self._weight = argpass(constant(weight))
        return self

    def set_size(self, size: tuple[float, float]) -> TDensity:
        """
        Sets the size of the density estimator to the specified bounds and
        returns itself. The size is specified as an array :code:`[width,
        height]` where :code:`width` is the maximum x-value and :code:`height`
        is the maximum y-value.

        Parameters
        ----------
        size : tuple[float, float]
            Size of the density estimator; default value :code:`[960, 500]`

        Returns
        -------
        Density
            Itself
        """
        dx = size[0]
        dy = size[1]
        if dx < 0.0 or dy < 0.0:
            raise ValueError("Invalid size: negative values")
        self._dx = dx
        self._dy = dy
        return self._resize()

    def set_cell_size(self, cell_size: float) -> TDensity:
        """
        Sets the size of individual cells in the underlying bin grid of the
        positive integer and returns itself.

        Parameters
        ----------
        cell_size : float
            Cell size; default value :code:`4`

        Returns
        -------
        Density
            Itself
        """
        self._k = floor(log(cell_size) / log(2))
        return self._resize()

    def set_thresholds(
        self,
        thresholds: Callable[[list[float], ...], float | list[float]]
        | list[float]
        | float,
    ) -> TDensity:
        """
        Sets the threshold function to the contour generator and returns
        itself.

        Thresholds are defined as an array of values :math:`[x_0, x_1, ...]`.
        The first generated density contour corresponds to the area where the
        estimated density is greater than or equal to :math:`x_0`; the second
        contour corresponds to the area where the estimated density is greater
        than or equal to :math:`x_1`, and so on. Thus, there is exactly one
        generated MultiPolygon geometry object for each specified threshold
        value; the threshold value is exposed as :code:`geometry["value"]`. The
        first value :math:`x_0` should typically be greater than zero.

        Parameters
        ----------
        thresholds : Callable[[list[float], ...], float | list[float]] | list[float] | float
            Threshold function or array or constant value


        Returns
        -------
        Density
            Itself
        """
        if callable(thresholds):
            self._threshold = thresholds
        else:
            self._threshold = constant(thresholds)
        return self

    def set_bandwidth(self, bandwidth: float) -> TDensity:
        """
        Sets the bandwidth (the standard deviation) of the Gaussian kernel and
        returns itself.

        Parameters
        ----------
        bandwidth : float
            Bandwidth value

        Returns
        -------
        Density
            Itself
        """
        self._r = (sqrt(4 * bandwidth * bandwidth + 1) - 1) / 2
        return self._resize()

    def get_x(self) -> Accessor[T, float]:
        return self._x

    def get_y(self) -> Accessor[T, float]:
        return self._y

    def get_weight(self) -> Accessor[T, float]:
        return self._weight

    def get_size(self) -> tuple[float, float]:
        return [self._dx, self._dy]

    def get_cell_size(self) -> int:
        return 1 << self._k

    def get_thresholds(self) -> Callable[[list[float], ...], float | list[float]]:
        return self._threshold

    def get_bandwidth(self) -> float:
        return sqrt(self._r * (self._r + 1))
