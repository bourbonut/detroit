from ..stream import geo_stream
from .area import AreaStream
from .bounds import BoundsStream
from .centroid import CentroidStream
from .context import PathContext
from .measure import LengthStream
from .string import PathString

from math import floor, isnan

def identity(x):
    return x

class GeoPath:

    def __init__(self, projection = None, context = None):
        self._digits = 3
        self._point_radius = 4.5
        self._projection = projection
        self._projection_stream = identity
        self._context = context
        self._context_stream = PathString(self._digits) if context is None else PathContext(context)

    def __call__(self, obj, *args):
        if obj:
            if callable(self._point_radius):
                self._context_stream.point_radius(self._point_radius(*args))
            geo_stream(obj, self._projection_stream(self._context_stream))

        return self._context_stream.result()


    def area(self, obj):
        path_area = AreaStream()
        geo_stream(obj, self._projection_stream(path_area))
        return path_area.result()

    def measure(self, obj):
        path_measure = LengthStream()
        geo_stream(obj, self._projection_stream(path_measure))
        return path_measure.result()

    def bounds(self, obj):
        path_bounds = BoundsStream()
        geo_stream(obj, self._projection_stream(path_bounds))
        return path_bounds.result()

    def centroid(self, obj):
        path_centroid = CentroidStream()
        geo_stream(obj, self._projection_stream(path_centroid))
        return path_centroid.result()

    def set_projection(self, projection = None):
        if projection is None:
            self._projection = None
            self._projection_stream = identity
        else:
            self._projection = projection
            self._projection_stream = projection.stream
        return self

    def set_context(self, context = None):
        if context is None:
            self._context = None
            self._context_stream = PathString(self._digits)
        else:
            self._context = context
            self._context_stream = PathContext(context)
        return self

    def set_point_radius(self, point_radius):
        if callable(point_radius):
            self._point_radius = point_radius
        else:
            self._context_stream.point_radius(point_radius)
            self._point_radius = point_radius
        return self

    def set_digits(self, digits = None):
        if digits is None:
            self._digits = None
        else:
            d = floor(float(digits)) if digits else 0
            if isnan(d) or d < 0:
                raise ValueError(f"Invalid digits: {digits}")
            self._digits = d
        if self._context is None:
            self._context_stream = PathString(self._digits)
        return self

    def get_projection(self):
        return self._projection

    def get_context(self):
        return self._context

    def get_point_radius(self):
        return self._point_radius

    def get_digits(self):
        return self._digits
