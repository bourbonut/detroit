from collections.abc import Callable
from itertools import chain
from math import ceil
from typing import Iterable, TypeVar

from ..types import GeoJSON, Point2D

EPSILON = 1e-6


def frange(start: float, stop: float, step: float) -> list[float]:
    return [start + i * step for i in range(max(0, ceil((stop - start) / step)))]


def graticule_x(y0: float, y1: float, dy: float) -> Callable[[float], list[Point2D]]:
    ly = frange(y0, y1 - EPSILON, dy) + [y1]

    def local_graticule_x(x: float) -> Point2D:
        return [[x, y] for y in ly]

    return local_graticule_x


def graticule_y(x0: float, x1: float, dx: float) -> Callable[[float], list[Point2D]]:
    lx = frange(x0, x1 - EPSILON, dx) + [x1]

    def local_graticule_y(y: float) -> Point2D:
        return [[x, y] for x in lx]

    return local_graticule_y


TGraticule = TypeVar("Graticule", bound="Graticule")


class Graticule:
    def __init__(self):
        self._x0 = 0.0
        self._x1 = 0.0
        self._y0 = 0.0
        self._y1 = 0.0

        self._X0 = 0.0
        self._X1 = 0.0
        self._Y0 = 0.0
        self._Y1 = 0.0

        self._dx = 10
        self._dy = 10
        self._DX = 90
        self._DY = 360
        self._x = None
        self._y = None
        self._X = None
        self._Y = None
        self._precision = 2.5

        self.set_extent_major([[-180, -90 + EPSILON], [180, 90 - EPSILON]])
        self.set_extent_minor([[-180, -80 - EPSILON], [180, 80 + EPSILON]])

    def __call__(self) -> GeoJSON:
        """
        Returns a GeoJSON MultiLineString geometry object representing all
        meridians and parallels for this graticule.


        Returns
        -------
        GeoJSON
            GeoJSON object
        """
        return {"type": "MultiLineString", "coordinates": list(self._lines())}

    def lines(self) -> list[GeoJSON]:
        """
        Returns an array of GeoJSON LineString geometry objects, one for each
        meridian or parallel for this graticule.

        Returns
        -------
        list[GeoJSON]
            List of GeoJSON LineString geometry objects
        """

        def coordinates(coordinates: list[Point2D]) -> GeoJSON:
            return {"type": "LineString", "coordinates": coordinates}

        return list(map(coordinates, self._lines()))

    def _lines(self) -> Iterable[list[Point2D]]:
        def filter_x(x: float) -> bool:
            return abs(x % self._DX) > EPSILON

        def filter_y(y: float) -> bool:
            return abs(y % self._DY) > EPSILON

        return chain(
            map(
                self._X,
                frange(ceil(self._X0 / self._DX) * self._DX, self._X1, self._DX),
            ),
            map(
                self._Y,
                frange(ceil(self._Y0 / self._DY) * self._DY, self._Y1, self._DY),
            ),
            map(
                self._x,
                filter(
                    filter_x,
                    frange(ceil(self._x0 / self._dx) * self._dx, self._x1, self._dx),
                ),
            ),
            map(
                self._y,
                filter(
                    filter_y,
                    frange(ceil(self._y0 / self._dy) * self._dy, self._y1, self._dy),
                ),
            ),
        )

    def outline(self) -> GeoJSON:
        """
        Returns a GeoJSON Polygon geometry object representing the outline of
        this graticule, i.e. along the meridians and parallels defining its
        extent.

        Returns
        -------
        GeoJSON
            GeoJSON object
        """
        return {
            "type": "Polygon",
            "coordinates": [
                self._X(self._X0)
                + self._Y(self._Y1)[1:]
                + self._X(self._X1)[-2::-1]
                + self._Y(self._Y0)[-2::-1]
            ],
        }

    def set_extent(self, extent: tuple[Point2D, Point2D]) -> TGraticule:
        """
        Sets the major and minor extents of this graticule.

        Parameters
        ----------
        extent : tuple[Point2D, Point2D]
            Extent values

        Returns
        -------
        Graticule
            Itself
        """
        return self.set_extent_major(extent).set_extent_minor(extent)

    def set_extent_major(self, extent: tuple[Point2D, Point2D]) -> TGraticule:
        """
        Sets the major extent of this graticule.

        Parameters
        ----------
        extent : tuple[Point2D, Point2D]
            Extent values

        Returns
        -------
        Graticule
            Itself
        """
        self._X0 = extent[0][0]
        self._Y0 = extent[0][1]
        self._X1 = extent[1][0]
        self._Y1 = extent[1][1]
        if self._X0 > self._X1:
            extent = self._X0
            self._X0 = self._X1
            self._X1 = extent
        if self._Y0 > self._Y1:
            extent = self._Y0
            self._Y0 = self._Y1
            self._Y1 = extent
        return self.set_precision(self.get_precision())

    def set_extent_minor(self, extent: tuple[Point2D, Point2D]) -> TGraticule:
        """
        Sets the minor extent of this graticule.

        Parameters
        ----------
        extent : tuple[Point2D, Point2D]
            Extent values

        Returns
        -------
        Graticule
            Itself
        """
        self._x0 = extent[0][0]
        self._y0 = extent[0][1]
        self._x1 = extent[1][0]
        self._y1 = extent[1][1]
        if self._x0 > self._x1:
            extent = self._x0
            self._x0 = self._x1
            self._x1 = extent
        if self._y0 > self._y1:
            extent = self._y0
            self._y0 = self._y1
            self._y1 = extent
        return self.set_precision(self.get_precision())

    def set_step(self, step: Point2D) -> TGraticule:
        """
        Sets the major and minor step for this graticule.

        Parameters
        ----------
        step : Point2D
            Step values

        Returns
        -------
        Graticule
            Itself
        """
        return self.set_step_major(step).set_step_minor(step)

    def set_step_major(self, step: Point2D) -> TGraticule:
        """
        Sets the major step for this graticule.

        Parameters
        ----------
        step : Point2D
            Step values

        Returns
        -------
        Graticule
            Itself
        """
        self._DX = step[0]
        self._DY = step[1]
        return self

    def set_step_minor(self, step: Point2D) -> TGraticule:
        """
        Sets the minor step for this graticule.

        Parameters
        ----------
        step : Point2D
            Step values

        Returns
        -------
        Graticule
            Itself
        """
        self._dx = step[0]
        self._dy = step[1]
        return self

    def set_precision(self, precision: float) -> TGraticule:
        """
        Sets the precision for this graticule.

        Parameters
        ----------
        precision : float
            Precision value

        Returns
        -------
        Graticule
            Itself
        """
        self._precision = precision
        self._x = graticule_x(self._y0, self._y1, 90)
        self._y = graticule_y(self._x0, self._x1, precision)
        self._X = graticule_x(self._Y0, self._Y1, 90)
        self._Y = graticule_y(self._X0, self._X1, precision)
        return self

    def get_extent(self) -> tuple[Point2D, Point2D]:
        return self.get_extent_minor()

    def get_extent_major(self) -> tuple[Point2D, Point2D]:
        return [[self._X0, self._Y0], [self._X1, self._Y1]]

    def get_extent_minor(self) -> tuple[Point2D, Point2D]:
        return [[self._x0, self._y0], [self._x1, self._y1]]

    def get_step(self) -> Point2D:
        return self.get_step_minor()

    def get_step_major(self) -> Point2D:
        return [self._DX, self._DY]

    def get_step_minor(self) -> Point2D:
        return [self._dx, self._dy]

    def get_precision(self):
        return self._precision


def geo_graticule() -> Graticule:
    """
    Constructs a geometry generator for creating graticules: a uniform grid of
    meridians and parallels for showing projection distortion. The default
    graticule has meridians and parallels every :math:`10°` between :math:`\\pm
    80°` latitude; for the polar regions, there are meridians every
    :math:`90°`.

    Returns
    -------
    Graticule
        Graticule object
    """
    return Graticule()


def geo_graticule_10() -> GeoJSON:
    """
    A convenience method for directly generating the default :math:`10°` global
    graticule as a GeoJSON MultiLineString geometry object.

    Returns
    -------
    GeoJSON
        GeoJSON object
    """
    return Graticule()()
