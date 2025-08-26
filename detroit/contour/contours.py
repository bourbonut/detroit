from collections.abc import Callable
from math import floor, inf, isfinite, isnan, nan
from typing import TypeVar

from ..array import argpass, extent, nice, ticks
from ..array.threshold import threshold_sturges
from ..types import MultiPolygonGeoJSON, Point2D
from .area import area
from .constant import constant
from .contains import contains

TContours = TypeVar("Contours", bound="Contours")

CASES = [
    [],
    [[[1.0, 1.5], [0.5, 1.0]]],
    [[[1.5, 1.0], [1.0, 1.5]]],
    [[[1.5, 1.0], [0.5, 1.0]]],
    [[[1.0, 0.5], [1.5, 1.0]]],
    [[[1.0, 1.5], [0.5, 1.0]], [[1.0, 0.5], [1.5, 1.0]]],
    [[[1.0, 0.5], [1.0, 1.5]]],
    [[[1.0, 0.5], [0.5, 1.0]]],
    [[[0.5, 1.0], [1.0, 0.5]]],
    [[[1.0, 1.5], [1.0, 0.5]]],
    [[[0.5, 1.0], [1.0, 0.5]], [[1.5, 1.0], [1.0, 1.5]]],
    [[[1.5, 1.0], [1.0, 0.5]]],
    [[[0.5, 1.0], [1.5, 1.0]]],
    [[[1.0, 1.5], [1.5, 1.0]]],
    [[[0.5, 1.0], [1.0, 1.5]]],
    [],
]


def sign(x: float) -> int:
    """
    Returns the sign of the input.

    Parameters
    ----------
    x : float
        Input value

    Returns
    -------
    int
        Sign value
    """
    return -1 if x < 0 else 1


def finite(x: float) -> float:
    """
    Returns :code:`x` if it is finite else :code:`nan`

    Parameters
    ----------
    x : float
        Input value

    Returns
    -------
    float
        Output value
    """
    return x if isfinite(x) else nan


def valid(v: float | None) -> float:
    """
    Returns :code:`v` if it is valid else :code:`-inf`

    Parameters
    ----------
    v : float | None
        Input value

    Returns
    -------
    float
        Output value
    """
    if v is None or isnan(v):
        return -inf
    else:
        return v


def above(x: float | None, value: float) -> bool:
    """
    Returns if :code:`x` is above :code:`value`

    Parameters
    ----------
    x : float | None
        Input value
    value : float
        Value to compare

    Returns
    -------
    bool
        Output value
    """
    return False if x is None else (x >= value)


def get(values: list[float], index: int) -> float | None:
    """
    Getter function for list of float. If the index does not exist, returns
    :code:`None`

    Parameters
    ----------
    values : list[float]
        List of value
    index : int
        Index

    Returns
    -------
    float | None
        Desired value given the index if it exists
    """
    index = int(index)
    return values[index] if index < len(values) else None


def smooth1(x: float, v0: float, v1: float, value: float) -> float:
    """
    Smooth function in one dimension

    Parameters
    ----------
    x : float
        Input value
    v0 : float
        Min bound value
    v1 : float
        Max bound value
    value : float
        Target value

    Returns
    -------
    float
        Smooth value
    """
    a = value - v0
    b = v1 - v0
    d = 0.0
    if isfinite(a) or isfinite(b):
        d = a / b if b != 0.0 else nan
    else:
        d = sign(a) / sign(b)
    return x if isnan(d) else x + d - 0.5


class Contours:
    """
    For each threshold value, the contour generator constructs a GeoJSON
    MultiPolygon geometry object representing the area where the input values
    are greater than or equal to the threshold value. The geometry is in planar
    coordinates, where :math:`(i + 0.5, j + 0.5)` corresponds to element
    :code:`i + j * n` in the input values array.
    """

    def __init__(self):
        self._dx = 1
        self._dy = 1
        self._threshold = threshold_sturges
        self._smooth = argpass(self._smooth_linear)

    def __call__(self, values: list[float]) -> list[MultiPolygonGeoJSON]:
        """
        Computes the contours for the given array of values, returning an array
        of GeoJSON MultiPolygon geometry objects.

        Parameters
        ----------
        values : list[float]
            Input grid values which must be an array of length :math:`n \\times
            m` where :math:`[n, m]` is the contour generator's size;
            furthermore, each :code:`values[i + j * n]` must represent the value
            at the position :math:`(i, j)`.

        Returns
        -------
        list[GeoJSON]
            Geometry objects
        """
        tz = self._threshold(values)
        if not isinstance(tz, list):
            e = extent(values, finite)
            tz = ticks(*nice(e[0], e[1], tz), tz)
            while tz[len(tz) - 1] >= e[1]:
                tz.pop()
            while tz[1] < e[0]:
                tz.pop(0)
        else:
            tz = sorted(tz)

        return list(map(lambda value: self.contour(values, value), tz))

    def contour(self, values: list[float], value: float) -> MultiPolygonGeoJSON:
        """
        Computes a single contour

        Parameters
        ----------
        values : list[float]
            Input grid values which must be an array of length :math:`n \\times
            m` where :math:`[n, m]` is the contour generator's size;
            furthermore, each :code:`values[i + j * n]` must represent the value
            at the position :math:`(i, j)`.
        value : float
            Threshold value; the input values are greater than or equal to this
            value.

        Returns
        -------
        GeoJSON
            GeoJSON MultiPolygon geometry object
        """
        v = nan if value is None else value
        if not isinstance(v, (int, float)) or isnan(v):
            raise ValueError(f"Invalid value: {value}")

        polygons = []
        holes = []

        def callback(ring: list[Point2D]):
            self._smooth(ring, values, v)
            if area(ring) > 0:
                polygons.append([ring])
            else:
                holes.append(ring)

        self._isorings(values, v, callback)
        for hole in holes:
            for polygon in polygons:
                if contains(polygon[0], hole) != -1:
                    polygon.append(hole)
                    break

        return {
            "type": "MultiPolygon",
            "value": value,
            "coordinates": polygons,
        }

    def _isorings(
        self,
        values: list[float],
        value: float,
        callback: Callable[[list[Point2D]], None],
    ):
        """
        Finds contour polygons and passes them to :code:`callback` function.

        Parameters
        ----------
        values : list[float]
            Input grid values
        value : float
            Threshold value
        callback : Callable[[list[Point2D]], None]
            Callback function called when a ring is found
        """
        fragment_by_start = {}
        fragment_by_end = {}

        x = y = -1

        def stitch(line: list[Point2D]):
            start = [line[0][0] + x, line[0][1] + y]
            end = [line[1][0] + x, line[1][1] + y]
            start_index = self._index(start)
            end_index = self._index(end)
            if f := fragment_by_end.get(start_index):
                if g := fragment_by_start.get(end_index):
                    fragment_by_end.pop(f["end"])
                    fragment_by_start.pop(g["start"])
                    if f == g:
                        f["ring"].append(end)
                        callback(f["ring"])
                    else:
                        fragment_by_start[f["start"]] = fragment_by_end[g["end"]] = {
                            "start": f["start"],
                            "end": g["end"],
                            "ring": f["ring"] + g["ring"],
                        }
                else:
                    fragment_by_end.pop(f["end"])
                    f["ring"].append(end)
                    f["end"] = end_index
                    fragment_by_end[end_index] = f
            elif f := fragment_by_start.get(end_index):
                if g := fragment_by_end.get(start_index):
                    fragment_by_start.pop(f["start"])
                    fragment_by_end.pop(g["end"])
                    if f == g:
                        f["ring"].append(end)
                        callback(f["ring"])
                    else:
                        fragment_by_start[g["start"]] = fragment_by_end[f["end"]] = {
                            "start": g["start"],
                            "end": f["end"],
                            "ring": g["ring"] + f["ring"],
                        }
                else:
                    fragment_by_start.pop(f["start"])
                    f["ring"].insert(0, start)
                    f["start"] = start_index
                    fragment_by_start[start_index] = f
            else:
                fragment_by_start[start_index] = fragment_by_end[end_index] = {
                    "start": start_index,
                    "end": end_index,
                    "ring": [start, end],
                }

        t1 = above(get(values, 0), value)
        for line in CASES[t1 << 1]:
            stitch(line)

        while x + 1 < self._dx - 1:
            x += 1
            t0 = t1
            t1 = above(get(values, x + 1), value)
            for line in CASES[t0 | t1 << 1]:
                stitch(line)
        x += 1
        for line in CASES[t1 << 0]:
            stitch(line)

        while y + 1 < self._dy - 1:
            y += 1
            x = -1
            t1 = above(get(values, y * self._dx + self._dx), value)
            t2 = above(get(values, y * self._dx), value)
            for line in CASES[t1 << 1 | t2 << 2]:
                stitch(line)
            while x + 1 < self._dx - 1:
                x += 1
                t0 = t1
                t1 = above(get(values, y * self._dx + self._dx + x + 1), value)
                t3 = t2
                t2 = above(get(values, y * self._dx + x + 1), value)
                for line in CASES[t0 | t1 << 1 | t2 << 2 | t3 << 3]:
                    stitch(line)
            x += 1
            for line in CASES[t1 | t2 << 3]:
                stitch(line)

        y += 1
        x = -1
        t2 = get(values, y * self._dx) >= value
        for line in CASES[t2 << 2]:
            stitch(line)
        while x + 1 < self._dx - 1:
            x += 1
            t3 = t2
            t2 = above(get(values, y * self._dx + x + 1), value)
            for line in CASES[t2 << 2 | t3 << 3]:
                stitch(line)

        x += 1
        for line in CASES[t2 << 3]:
            stitch(line)

    def _smooth_linear(self, ring: list[Point2D], values: list[float], value: float):
        """
        Function for smoothing contour polygons using linear interpolatation.

        Parameters
        ----------
        ring : list[Point2D]
            Contour polygons
        values : list[float]
            Input grid values
        value : float
            Threshold value
        """
        for point in ring:
            x = point[0]
            y = point[1]
            xt = int(x)
            yt = int(y)
            v1 = valid(get(values, yt * self._dx + xt))
            if x > 0 and x < self._dx and xt == x:
                point[0] = smooth1(
                    x, valid(get(values, yt * self._dx + xt - 1)), v1, value
                )
            if y > 0 and y < self._dy and yt == y:
                point[1] = smooth1(
                    y, valid(get(values, (yt - 1) * self._dx + xt)), v1, value
                )

    def _index(self, point: Point2D) -> int:
        """
        Returns the index given 2D point coordinates

        Parameters
        ----------
        point : Point2D
            2D point coordinates

        Returns
        -------
        int
            Index value
        """
        return int(point[0] * 2 + point[1] * (self._dx + 1) * 4)

    def set_size(self, size: tuple[float, float]) -> TContours:
        """
        Sets the size of the input values to the contour generator and returns
        itself.

        Parameters
        ----------
        size : tuple[float, float]
            Size of the input values

        Returns
        -------
        Contours
            Itself
        """
        dx = floor(size[0])
        dy = floor(size[1])
        if dx < 0.0 or dy < 0.0:
            raise ValueError("Invalid size: negative values")
        self._dx = dx
        self._dy = dy
        return self

    def set_thresholds(
        self,
        thresholds: Callable[[list[float], ...], float | list[float]]
        | list[float]
        | float,
    ) -> TContours:
        """
        Sets the threshold function to the contour generator and returns
        itself.

        Parameters
        ----------
        thresholds : Callable[[list[float], ...], float | list[float]] | list[float] | float
            Threshold function or array or constant value; default
            :func:`d3.threshold_sturges <detroit.threshold_sturges>`

        Returns
        -------
        Contours
            Itself
        """
        if callable(thresholds):
            self._threshold = thresholds
        else:
            self._threshold = constant(thresholds)
        return self

    def set_smooth(self, smooth: bool) -> TContours:
        """
        Sets if contour polygons are smoothed using interpolatation and returns
        itself.

        Parameters
        ----------
        smooth : bool
            Boolean value

        Returns
        -------
        Contours
            Itself
        """

        def noop():
            return

        self._smooth = argpass(self._smooth_linear if smooth else noop)
        return self

    def get_size(self) -> tuple[float, float]:
        return [self._dx, self._dy]

    def get_thresholds(self) -> Callable[[list[float], ...], float | list[float]]:
        return self._threshold

    def get_smooth(self) -> bool:
        return self._smooth == self._smooth_linear
