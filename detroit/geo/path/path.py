from collections.abc import Callable
from math import floor, isnan
from typing import Any, TypeVar

from ...types import GeoJSON, Point2D
from ..common import Context, Projection
from ..stream import geo_stream
from .area import AreaStream
from .bounds import BoundsStream
from .centroid import CentroidStream
from .context import PathContext
from .measure import LengthStream
from .string import PathString

TGeoPath = TypeVar("GeoPath", bound="GeoPath")


def identity(x):
    return x


class GeoPath:
    """
    Creates a new geographic path generator with the default settings. If
    projection is specified, sets the current projection. If context is
    specified, sets the current context.

    Parameters
    ----------
    projection : Projection | None
        Projection
    context : Context | None
        Context
    """

    def __init__(
        self, projection: Projection | None = None, context: Context | None = None
    ):
        self._digits = 3
        self._point_radius = 4.5
        self._projection = projection
        self._projection_stream = identity if projection is None else projection.stream
        self._context = context
        self._context_stream = (
            PathString(self._digits) if context is None else PathContext(context)
        )

    def __call__(self, obj: GeoJSON, *args: Any) -> str | None:
        """
        Renders the given object, which may be any GeoJSON feature or geometry
        object:

        * :code:`Point` - a single position
        * :code:`MultiPoint` - an array of positions
        * :code:`LineString` - an array of positions forming a continuous line
        * :code:`MultiLineString` - an array of arrays of positions forming \
        several lines
        * :code:`Polygon` - an array of arrays of positions forming a polygon \
        (possibly with holes)
        * :code:`MultiPolygon` - a multidimensional array of positions forming \
        multiple polygons
        * :code:`GeometryCollection` - an array of geometry objects
        * :code:`Feature` - a feature containing one of the above geometry \
        objects
        * :code:`FeatureCollection` - an array of feature objects

        The type Sphere is also supported, which is useful for rendering the
        outline of the globe; a sphere has no coordinates. Any additional
        arguments are passed along to the pointRadius accessor.

        Parameters
        ----------
        obj : GeoJSON
            GeoJSON object
        *args : Any
            Additional arguments passed to :code:`point_radius` function

        Returns
        -------
        str | None
            Path
        """
        if obj:
            if callable(self._point_radius):
                self._context_stream.point_radius(self._point_radius(*args))
            geo_stream(obj, self._projection_stream(self._context_stream))

        return self._context_stream.result()

    def area(self, obj: GeoJSON) -> float:
        """
        Returns the projected planar area (typically in square pixels) for the
        specified GeoJSON object.

        Parameters
        ----------
        obj : GeoJSON
            GeoJSON object

        Returns
        -------
        float
            Area in px²
        """
        path_area = AreaStream()
        geo_stream(obj, self._projection_stream(path_area))
        return path_area.result()

    def measure(self, obj: GeoJSON) -> float:
        """
        Returns the projected planar length (typically in pixels) for the
        specified GeoJSON object.

        Parameters
        ----------
        obj : GeoJSON
            GeoJSON object

        Returns
        -------
        float
            Projected planar length in px
        """
        path_measure = LengthStream()
        geo_stream(obj, self._projection_stream(path_measure))
        return path_measure.result()

    def bounds(self, obj: GeoJSON) -> tuple[Point2D, Point2D]:
        """
        Returns the projected planar bounding box (typically in pixels) for the
        specified GeoJSON object.

        Parameters
        ----------
        obj : GeoJSON
            GeoJSON object

        Returns
        -------
        tuple[Point2D, Point2D]
            Projected planar bounding box
        """
        path_bounds = BoundsStream()
        geo_stream(obj, self._projection_stream(path_bounds))
        return path_bounds.result()

    def centroid(self, obj: GeoJSON) -> Point2D:
        """
        Returns the projected planar centroid (typically in pixels) for the
        specified GeoJSON object.

        Parameters
        ----------
        obj : GeoJSON
            GeoJSON object

        Returns
        -------
        Point2D
            Projected planar centroid
        """
        path_centroid = CentroidStream()
        geo_stream(obj, self._projection_stream(path_centroid))
        return path_centroid.result()

    def set_projection(self, projection: Projection | None = None) -> TGeoPath:
        """
        If a projection is specified, sets the current projection to the
        specified projection.
        The projection defaults to :code:`None`, which represents the identity
        transformation: the input geometry is not projected and is instead
        rendered directly in raw coordinates. This can be useful for fast
        rendering of pre-projected geometry, or for fast rendering of the
        equirectangular projection.

        The given projection is typically one of built-in geographic
        projections; however, any object that exposes a projection.stream
        function can be used, enabling the use of custom projections.

        Parameters
        ----------
        projection : Projection | None
            Projection

        Returns
        -------
        GeoPath
            Itself
        """
        if projection is None:
            self._projection = None
            self._projection_stream = identity
        else:
            self._projection = projection
            self._projection_stream = projection.stream
        return self

    def set_context(self, context: Context | None = None) -> TGeoPath:
        """
        If context is specified, sets the current render context and returns
        the path generator. If the context is :code:`None`, then the path
        generator will return an SVG path string; if the context is not
        :code:`None`, the path generator will instead call methods on the
        specified context to render geometry.

        Parameters
        ----------
        context : Context | None
            Context

        Returns
        -------
        GeoPath
            Itself
        """
        if context is None:
            self._context = None
            self._context_stream = PathString(self._digits)
        else:
            self._context = context
            self._context_stream = PathContext(context)
        return self

    def set_point_radius(self, radius: Callable[..., float] | float) -> TGeoPath:
        """
        If radius is specified, sets the radius used to display Point and
        MultiPoint geometries to the specified number.

        Parameters
        ----------
        radius : Callable[..., float] | float
            Radius function or constant value

        Returns
        -------
        GeoPath
            Itself
        """
        if callable(radius):
            self._point_radius = radius
        else:
            self._context_stream.point_radius(radius)
            self._point_radius = radius
        return self

    def set_digits(self, digits: str | float | None = None) -> TGeoPath:
        """
        If digits is specified (as a non-negative number), sets the number of
        fractional digits for coordinates generated in SVG path strings.

        Parameters
        ----------
        digits : str | float | None
            Digits value

        Returns
        -------
        GeoPath
            Itself
        """
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
