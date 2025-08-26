from collections.abc import Callable
from math import cos, degrees, radians, sin

from ...types import GeoJSON, Point2D, Vec2D
from ..clip import geo_clip_rectangle
from ..common import PolygonStream, Projection
from ..transform import GeoTransformer
from .fit import fit_extent, fit_height, fit_size, fit_width


def transform(projection: Projection) -> GeoTransformer:
    def point(self, x: float, y: float):
        x = projection([x, y])
        self._stream.point(x[0], x[1])

    return GeoTransformer({"point": point})


def identity(x: PolygonStream) -> PolygonStream:
    return x


class GeoIdentity(Projection):
    def __init__(self):
        self._k = 1
        self._tx = 0
        self._ty = 0
        self._sx = 1
        self._sy = 1
        self._alpha = 0
        self._ca = None
        self._sa = None
        self._x0 = None
        self._y0 = None
        self._x1 = None
        self._y1 = None
        self._kx = 1
        self._ky = 1
        self._transform = transform(self)
        self._postclip = identity
        self._cache = None
        self._cache_stream = None

    def __call__(self, point: Point2D) -> Point2D:
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
        x = point[0] * self._kx
        y = point[1] * self._ky
        if self._alpha:
            t = y * self._ca - x * self._sa
            x = x * self._ca + y * self._sa
            y = t
        return [x + self._tx, y + self._ty]

    def invert(self, point: Point2D) -> Point2D:
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
        x = point[0] - self._tx
        y = point[1] - self._ty
        if self._alpha:
            t = y * self._ca + x * self._sa
            x = x * self._ca - y * self._sa
            y = t
        return [x / self._kx, y / self._ky]

    def stream(self, stream: PolygonStream) -> PolygonStream:
        """
        Returns a projection stream for the specified output stream. Any input
        geometry is projected before being streamed to the output stream. A
        typical projection involves several geometry transformations: the input
        geometry is first converted to radians, rotated on three axes, clipped
        to the small circle or cut along the antimeridian, and lastly projected
        to the plane with adaptive resampling, scale and translation.

        Parameters
        ----------
        stream : PolygonStream
            Stream object

        Returns
        -------
        PolygonStream
            Modified stream object
        """
        if self._cache and self._cache_stream == stream:
            return self._cache
        self._cache_stream = stream
        self._cache = self._transform(self._postclip(self._cache_stream))
        return self._cache

    def set_preclip(
        self, preclip: Callable[[PolygonStream], PolygonStream]
    ) -> Projection:
        """
        If preclip is specified, sets the projection's spherical clipping to
        the specified function and returns the projection; preclip is a
        function that takes a projection stream and returns a clipped stream.

        Parameters
        ----------
        preclip : Callable[[PolygonStream], PolygonStream]
            Preclip function

        Returns
        -------
        Projection
            Itself
        """
        raise NotImplementedError("Unsupported method for GeoIdentity")

    def set_postclip(
        self, postclip: Callable[[PolygonStream], PolygonStream]
    ) -> Projection:
        """
        If postclip is specified, sets the projection's Cartesian clipping to
        the specified function and returns the projection; postclip is a
        function that takes a projection stream and returns a clipped stream.

        Parameters
        ----------
        postclip : Callable[[PolygonStream], PolygonStream]
            Postclip function

        Returns
        -------
        Projection
            Itself
        """
        self._postclip = postclip
        self._x0 = None
        self._x1 = None
        self._y0 = None
        self._y1 = None
        return self.reset()

    def set_clip_extent(
        self, clip_extent: tuple[Point2D, Point2D] | None = None
    ) -> Projection:
        """
        If extent is specified, sets the projection's viewport clip extent to
        the specified bounds in pixels and returns the projection. The extent
        bounds are specified as an array :math:`[[x_0, y_0], [x_1, y_1]]`,
        where :math:`x_0` is the left-side of the viewport, :math:`y_0` is the
        top, :math:`x_1` is the right and :math:`y_1` is the bottom. If extent
        is :code:`None`, no viewport clipping is performed. If extent is not
        specified, returns the current viewport clip extent which defaults to
        :code:`None`. Viewport clipping is independent of small-circle clipping
        via projection.clipAngle.

        Parameters
        ----------
        clip_extent : tuple[Point2D, Point2D] | None


        Returns
        -------
        Projection
            Itself
        """
        if clip_extent is None:
            self._x0 = None
            self._x1 = None
            self._y0 = None
            self._y1 = None
            self._postclip = identity
        else:
            self._x0 = clip_extent[0][0]
            self._x1 = clip_extent[1][0]
            self._y0 = clip_extent[0][1]
            self._y1 = clip_extent[1][1]
            self._postclip = geo_clip_rectangle(self._x0, self._y0, self._x1, self._y1)
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
        self._k = k
        return self.reset()

    def translate(self, translation: Vec2D) -> Projection:
        """
        If translate is specified, sets the projection's translation offset to
        the specified two-element array :code:`[tx, ty]` and returns the
        projection. The translation offset determines the pixel coordinates of
        the projection's center. The default translation offset places
        :math:`[0°,0°]` at the center of a :math:`960 \\times 500` area.

        Parameters
        ----------
        translation : Vec2D
            Translation 2D vector

        Returns
        -------
        Projection
            Itself
        """
        self._tx = translation[0]
        self._ty = translation[1]
        return self.reset()

    def set_center(self, center: Point2D) -> Projection:
        """
        If center is specified, sets the projection's center to the specified
        center, a two-element array of :code:`[longitude, latitude]` in degrees
        and returns the projection.

        Parameters
        ----------
        center : Point2D
            Center point

        Returns
        -------
        Projection
            Itself
        """
        raise NotImplementedError("Unsupported method for GeoIdentity")

    def rotate(
        self, angles: tuple[float, float] | tuple[float, float, float]
    ) -> Projection:
        """
        If angles is specified, sets the projection's three-axis spherical
        rotation to the specified value, which must be a two- or three-element
        array of numbers :math:`[\\lambda, \\phi, \\gamma]` specifying the
        rotation angles in degrees about each spherical axis. (These correspond
        to yaw, pitch and roll).

        Parameters
        ----------
        angles : tuple[float, float] | tuple[float, float, float]
            :math:`[\\lambda, \\phi, \\gamma]` values or :math:`[\\lambda, \\phi]` values

        Returns
        -------
        Projection
            Itself
        """
        raise NotImplementedError("Unsupported method of GeoIdentity")

    def set_angle(self, angle: float) -> Projection:
        """
        If angle is specified, sets the projection's post-projection planar
        rotation angle to the specified angle in degrees and returns the
        projection.

        Parameters
        ----------
        angle : float
            Angle value

        Returns
        -------
        Projection
            Itself
        """
        self._alpha = radians(angle)
        self._sa = sin(self._alpha)
        self._ca = cos(self._alpha)
        return self.reset()

    def set_reflect_x(self, reflect_x: bool) -> Projection:
        """
        If reflect is specified, sets whether or not the x-dimension is
        reflected (negated) in the output. This can be useful to display sky
        and astronomical data with the orb seen from below: right ascension
        (eastern direction) will point to the left when North is pointing up.

        Parameters
        ----------
        reflect_x : bool
            Boolean value

        Returns
        -------
        Projection
            Itself
        """
        self._sx = -1 if reflect_x else 1
        return self.reset()

    def set_reflect_y(self, reflect_y: bool) -> Projection:
        """
        If reflect is specified, sets whether or not the y-dimension is
        reflected (negated) in the output. This is especially useful for
        transforming from standard spatial reference systems, which treat
        positive y as pointing up, to display coordinate systems such as Canvas
        and SVG, which treat positive y as pointing down.

        Parameters
        ----------
        reflect_y : bool
            Boolean value

        Returns
        -------
        Projection
            Itself
        """
        self._sy = -1 if reflect_y else 1
        return self.reset()

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
        raise NotImplementedError("Unsupported method of GeoIdentity")

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

    def reset(self) -> Projection:
        self._kx = self._k * self._sx
        self._ky = self._k * self._sy
        self._cache = None
        self._cache_stream = None
        return self

    def get_postclip(self) -> Callable[[PolygonStream], PolygonStream]:
        return self._postclip

    def get_clip_extent(self) -> tuple[Point2D, Point2D] | None:
        if self._x0 is None:
            return None
        else:
            return [[self._x0, self._y0], [self._x1, self._y1]]

    def get_scale(self) -> float:
        return self._k

    def get_translation(self) -> Vec2D:
        return [self._x, self._y]

    def get_angle(self) -> float:
        return degrees(self._alpha)

    def get_reflect_x(self) -> bool:
        return self._sx < 0

    def get_reflect_y(self) -> bool:
        return self._sy < 0


def geo_identity() -> GeoIdentity:
    return GeoIdentity()
