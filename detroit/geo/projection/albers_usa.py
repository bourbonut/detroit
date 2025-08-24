from .albers import geo_albers
from .conic_equal_area import geo_conic_equal_area
from .fit import fit_extent, fit_size, fit_width, fit_height
from ...types import Point2D, Vec2D, GeoJSON
from ..common import PolygonStream
from typing import TypeVar

EPSILON = 1e-6

TAlbersUsaProjection = TypeVar("AlbersUsaProjection", bound="AlbersUsaProjection")


class Multiplex:
    def __init__(self, streams: list[PolygonStream]):
        self._streams = streams

    def point(self, x: float, y: float):
        for stream in self._streams:
            stream.point(x, y)

    def line_start(self):
        for stream in self._streams:
            stream.line_start()

    def line_end(self):
        for stream in self._streams:
            stream.line_end()

    def polygon_start(self):
        for stream in self._streams:
            stream.polygon_start()

    def polygon_end(self):
        for stream in self._streams:
            stream.polygon_end()

    def sphere(self):
        for stream in self._streams:
            stream.sphere()


class PointStream:
    def __init__(self):
        self._point = None

    def point(self, x: float, y: float):
        self._point = [x, y]

    def __str__(self) -> str:
        return "AlbertUsaPointStream()"


class AlbersUsaProjection:
    def __init__(self):
        self._cache = None
        self._cache_stream = None
        self._lower48 = geo_albers()
        self._lower48_point = None
        self._alaska = (
            geo_conic_equal_area()
            .rotate([154, 0])
            .set_center([-2, 58.5])
            .parallels([55, 65])
        )
        self._alaska_point = None
        self._hawaii = (
            geo_conic_equal_area()
            .rotate([157, 0])
            .set_center([-3, 19.9])
            .parallels([8, 18])
        )
        self._hawaii_point = None
        self._point_stream = PointStream()

    def __call__(self, coordinates: Point2D) -> Point2D:
        x = coordinates[0]
        y = coordinates[1]
        self._point_stream._point is None
        self._lower48_point.point(x, y)
        if point := self._point_stream._point:
            return point
        self._alaska_point.point(x, y)
        if point := self._point_stream._point:
            return point
        self._hawaii_point.point(x, y)
        if point := self._point_stream._point:
            return point

    def invert(self, coordinates: Point2D) -> Point2D:
        k = self._lower48.get_scale()
        t = self._lower48.get_translation()
        x = (coordinates[0] - t[0]) / k
        y = (coordinates[1] - t[1]) / k
        if 0.120 <= y < 0.234 and -0.425 <= x < -0.214:
            return self._alaska.invert(coordinates)
        if 0.166 <= y < 0.234 and -0.214 <= x < -0.115:
            return self._hawaii.invert(coordinates)
        else:
            self._lower48.invert(coordinates)

    def stream(self, stream: PointStream):
        if self._cache is not None and self._cache_stream == stream:
            return self._cache
        else:
            self._cache_stream = stream
            self._cache = Multiplex(
                [
                    self._lower48.stream(stream),
                    self._alaska.stream(stream),
                    self._hawaii.stream(stream),
                ]
            )
            return self._cache

    def set_precision(self, precision: float) -> TAlbersUsaProjection:
        self._lower48.set_precision(precision)
        self._alaska.set_precision(precision)
        self._hawaii.set_precision(precision)
        return self.reset()

    def scale(self, k: float) -> TAlbersUsaProjection:
        self._lower48.scale(k)
        self._alaska.scale(k * 0.35)
        self._hawaii.scale(k)
        return self.translate(self._lower48.get_translation())

    def translate(self, translation: Vec2D) -> TAlbersUsaProjection:
        k = self._lower48.get_scale()
        x = translation[0]
        y = translation[1]

        self._lower48_point = (
            self._lower48.translate(translation)
            .set_clip_extent(
                [[x - 0.455 * k, y - 0.238 * k], [x + 0.455 * k, y + 0.238 * k]]
            )
            .stream(self._point_stream)
        )

        self._alaska_point = (
            self._alaska.translate([x - 0.307 * k, y + 0.201 * k])
            .set_clip_extent(
                [
                    [x - 0.425 * k + EPSILON, y + 0.120 * k + EPSILON],
                    [x - 0.214 * k - EPSILON, y + 0.234 * k - EPSILON],
                ]
            )
            .stream(self._point_stream)
        )

        self._hawaii_point = (
            self._hawaii.translate([x - 0.205 * k, y + 0.212 * k])
            .set_clip_extent(
                [
                    [x - 0.214 * k + EPSILON, y + 0.166 * k + EPSILON],
                    [x - 0.115 * k - EPSILON, y + 0.234 * k - EPSILON],
                ]
            )
            .stream(self._point_stream)
        )

        return self.reset()

    def fit_extent(
        self, extent: tuple[Point2D, Point2D], obj: GeoJSON
    ) -> TAlbersUsaProjection:
        return fit_extent(self, extent, obj)

    def fit_size(self, size: Point2D, obj: GeoJSON) -> TAlbersUsaProjection:
        return fit_size(self, size, obj)

    def fit_width(self, width: float, obj: GeoJSON) -> TAlbersUsaProjection:
        return fit_width(self, width, obj)

    def fit_height(self, height: float, obj: GeoJSON) -> TAlbersUsaProjection:
        return fit_height(self, height, obj)

    def reset(self):
        self._cache = None
        self._cache_stream = None
        return self

    def get_precision(self) -> float:
        return self._lower48.get_precision()

    def get_scale(self) -> float:
        return self._lower48.get_scale()

    def get_translation(self) -> Vec2D:
        return self._lower48.translate()


def geo_albers_usa():
    return AlbersUsaProjection().scale(1070)
