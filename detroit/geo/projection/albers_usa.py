from ...types import GeoJSON, Point2D, Vec2D
from ..common import PolygonStream, Projection
from .albers import geo_albers
from .conic_equal_area import geo_conic_equal_area
from .fit import fit_extent, fit_height, fit_size, fit_width

EPSILON = 1e-6


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
        return f"AlbertUsaPointStream({self._point})"


class AlbersUsaProjection(Projection):
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
        """
        Returns a new array :code:`[x, y]` (typically in pixels) representing
        the projected point of the given point. The point must be specified as
        a two-element array :code:`[longitude, latitude]` in degrees. May
        return :code:`None` if the specified point has no defined projected position,
        such as when the point is outside the clipping bounds of the
        projection.

        Parameters
        ----------
        point : Point2D
            Point :code:`[longitude, latitude]`

        Returns
        -------
        Point2D
            New projected point :code:`[x, y]`
        """
        x = coordinates[0]
        y = coordinates[1]
        self._point_stream._point = None
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
        """
        Returns a new array :code:`[longitude, latitude]` in degrees
        representing the unprojected point of the given projected point. The
        point must be specified as a two-element array :code:`[x, y]`
        (typically in pixels). May return null if the specified point has no
        defined projected position, such as when the point is outside the
        clipping bounds of the projection.

        This method is only defined on invertible projections.

        Parameters
        ----------
        point : Point2D
            2D point where coordinates are in pixels

        Returns
        -------
        Point2D
            2D point where coordinates are in degrees
        """
        k = self._lower48.get_scale()
        t = self._lower48.get_translation()
        x = (coordinates[0] - t[0]) / k
        y = (coordinates[1] - t[1]) / k
        if 0.120 <= y < 0.234 and -0.425 <= x < -0.214:
            return self._alaska.invert(coordinates)
        if 0.166 <= y < 0.234 and -0.214 <= x < -0.115:
            return self._hawaii.invert(coordinates)
        else:
            return self._lower48.invert(coordinates)

    def stream(self, stream: PointStream):
        """
        Returns a projection stream for the specified output stream.

        Parameters
        ----------
        stream : PolygonStream
            Stream object

        Returns
        -------
        PolygonStream
            Modified stream object
        """
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

    def set_precision(self, precision: float) -> Projection:
        """
        If precision is specified, sets the threshold for the projection's
        adaptive resampling to the specified value in pixels and returns the
        projection. This value corresponds to the Douglas–Peucker distance.

        Parameters
        ----------
        precision : float
            Precision value

        Returns
        -------
        Projection
            Itself
        """
        self._lower48.set_precision(precision)
        self._alaska.set_precision(precision)
        self._hawaii.set_precision(precision)
        return self.reset()

    def scale(self, k: float) -> Projection:
        """
        If scale is specified, sets the projection's scale factor to the
        specified value and returns the projection. The scale factor
        corresponds linearly to the distance between projected points; however,
        absolute scale factors are not equivalent across projections.

        Parameters
        ----------
        k : float
            Scale factor

        Returns
        -------
        Projection
            Itself
        """
        self._lower48.scale(k)
        self._alaska.scale(k * 0.35)
        self._hawaii.scale(k)
        return self.translate(self._lower48.get_translation())

    def translate(self, translation: Vec2D) -> Projection:
        """
        If translate is specified, sets the projection's translation offset to
        the specified two-element array :code:`[tx, ty]` and returns the
        projection. The translation offset determines the pixel coordinates of
        the projection's center.

        Parameters
        ----------
        translation : Vec2D
            Translation 2D vector

        Returns
        -------
        Projection
            Itself
        """
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

    def fit_extent(self, extent: tuple[Point2D, Point2D], obj: GeoJSON) -> Projection:
        """
        Sets the projection's scale and translate to fit the specified GeoJSON
        object in the center of the given extent. The extent is specified as an
        array :math:`[[x_0, y_0], [x_1, y_1]]`, where :math:`x_0` is the left
        side of the bounding box, :math:`y_0` is the top, :math:`x_1`₁ is the
        right and :math:`y_1` is the bottom. Returns the projection.

        Any clip extent is ignored when determining the new scale and
        translate. The precision used to compute the bounding box of the given
        object is computed at an effective scale of 150.

        Parameters
        ----------
        extent : tuple[Point2D, Point2D]
            Extent values
        obj : GeoJSON
            GeoJSON object

        Returns
        -------
        Projection
            Itself
        """
        return fit_extent(self, extent, obj)

    def fit_size(self, size: Point2D, obj: GeoJSON) -> Projection:
        """
        A convenience method for projection.fit_extent where the top-left
        corner of the extent is [0, 0].

        Parameters
        ----------
        size : Point2D
            Size values
        obj : GeoJSON
            GeoJSON object

        Returns
        -------
        Projection
            Itself
        """
        return fit_size(self, size, obj)

    def fit_width(self, width: float, obj: GeoJSON) -> Projection:
        """
        A convenience method for projection.fit_size where the height is
        automatically chosen from the aspect ratio of object and the given
        constraint on width.

        Parameters
        ----------
        width : float
            Width value
        obj : GeoJSON
            GeoJSON object

        Returns
        -------
        Projection
            Itself
        """
        return fit_width(self, width, obj)

    def fit_height(self, height: float, obj: GeoJSON) -> Projection:
        """
        A convenience method for projection.fit_size where the width is
        automatically chosen from the aspect ratio of object and the given
        constraint on height.

        Parameters
        ----------
        height : float
            Height value
        obj : GeoJSON
            GeoJSON object

        Returns
        -------
        Projection
            Itself
        """
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
        return self._lower48.get_translation()


def geo_albers_usa() -> Projection:
    """
    This is a U.S.-centric composite projection of three geoConicEqualArea
    projections: :func:`d3.geo_albers <geo_albers>` is used for the lower
    forty-eight states, and separate conic equal-area projections are used for
    Alaska and Hawaii. The scale for Alaska is diminished: it is projected at
    :math:`0.35 \\times` its true relative area.

    The constituent projections have fixed clip, center and rotation, and thus
    this projection does not support :func:`Projection.set_center
    <detroit.geo.common.Projection.set_center>`, :func:`Projection.rotate
    <detroit.geo.common.Projection.rotate>`, :func:`Projection.set_clip_angle
    <detroit.geo.common.Projection.set_clip_angle>` or
    :func:`Projection.set_clip_extent
    <detroit.geo.common.Projection.set_clip_extent>`.

    Returns
    -------
    Projection
        Projection object
    """
    return AlbersUsaProjection().scale(1070)
