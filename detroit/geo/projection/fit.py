from ..stream import geo_stream
from ..path.bounds import BoundsStream
from ...types import GeoJSON, Point2D
from collections.abc import Callable
from typing import TypeVar

ProjectionMutator = TypeVar("ProjectionMutator")

def fit(projection: ProjectionMutator, fit_bounds: Callable[[float], None], obj: GeoJSON) -> ProjectionMutator:
    clip = projection.get_clip_extent() if hasattr(projection, "get_clip_extent") else None
    projection.scale(150).translate([0, 0])
    if clip is not None:
        projection.set_clip_extent(None)
    stream = BoundsStream()
    geo_stream(obj, projection.stream(stream))
    fit_bounds(stream.result())
    if clip is not None:
        projection.set_clip_extent(clip)
    return projection

def fit_extent(projection: ProjectionMutator, extent: tuple[Point2D, Point2D], obj: GeoJSON) -> ProjectionMutator:
    def fit_bounds(b: float):
        w = extent[1][0] - extent[0][0]
        h = extent[1][1] - extent[0][1]
        k = min(w / (b[1][0] - b[0][0]), h / (b[1][1] - b[0][1]))
        x = extent[0][0] + (w - k * (b[1][0] + b[0][0])) * 0.5
        y = extent[0][1] + (w - k * (b[1][1] + b[0][1])) * 0.5
        projection.scale(150 * k).translate([x, y])
    return fit(projection, fit_bounds, obj)

def fit_size(projection: ProjectionMutator, size: Point2D, obj: GeoJSON) -> ProjectionMutator:
    return fit_extent(projection, [[0, 0], size], obj)

def fit_width(projection: ProjectionMutator, width: float, obj: GeoJSON) -> ProjectionMutator:
    def fit_bounds(b: float):
        w = width
        k = w / (b[1][0] - b[0][0])
        x = (w - k * (b[1][0] + b[0][0])) / 2
        y = -k * b[0][1]
        projection.scale(150 * k).translate([x, y])
    return fit(projection, fit_bounds, obj)

def fit_height(projection: ProjectionMutator, height: float, obj: GeoJSON) -> ProjectionMutator:
    def fit_bounds(b: float):
        h = height
        k = h / (b[1][1] - b[0][1])
        x = -k * b[0][0]
        y = (h - k * (b[1][1] + b[0][1])) / 2
        projection.scale(150 * k).translate([x, y])
    return fit(projection, fit_bounds, obj)
