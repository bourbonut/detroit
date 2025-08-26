from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Protocol, TypeAlias, TypeVar

from ..types import GeoJSON, Point2D, Vec2D


class SpatialTransform(Protocol):
    """
    Describes a spatial transformation
    """

    def __call__(self, x: float, y: float) -> Point2D:
        """
        Transforms the x and y values into two new values.

        Parameters
        ----------
        x : float
            x value
        y : float
            y value

        Returns
        -------
        Point2D
            New values
        """
        ...

    def invert(self, x: float, y: float) -> Point2D:
        """
        Optional method which makes the invert transformation.

        Parameters
        ----------
        x : float
            x value
        y : float
            y value

        Returns
        -------
        Point2D
            Inverted values
        """
        ...


class LineStream(ABC):
    @abstractmethod
    def line_start(self):
        """
        Indicates the start of a line or ring. Within a polygon, indicates the
        start of a ring. The first ring of a polygon is the exterior ring, and
        is typically clockwise. Any subsequent rings indicate holes in the
        polygon, and are typically counterclockwise.
        """
        ...

    @abstractmethod
    def line_end(self):
        """
        Indicates the end of a line or ring. Within a polygon, indicates the
        end of a ring. Unlike GeoJSON, the redundant closing coordinate of a
        ring is not indicated via point, and instead is implied via lineEnd
        within a polygon.
        """
        ...

    @abstractmethod
    def point(self, x: float, y: float):
        """
        Indicates a point with the specified coordinates x and y (and
        optionally z). The coordinate system is unspecified and
        implementation-dependent; for example, projection streams require
        spherical coordinates in degrees as input. Outside the context of a
        polygon or line, a point indicates a point geometry object (Point or
        MultiPoint). Within a line or polygon ring, the point indicates a
        control point.

        Parameters
        ----------
        x : float
            x value
        y : float
            y value
        """
        ...

    def sphere(self):
        """
        Indicates the sphere (the globe; the unit sphere centered at (0,0,0)).
        """
        ...


class PolygonStream(LineStream):
    @abstractmethod
    def polygon_start(self):
        """
        Indicates the start of a polygon. The first line of a polygon indicates
        the exterior ring, and any subsequent lines indicate interior holes.
        """
        ...

    @abstractmethod
    def polygon_end(self):
        """
        Indicates the end of a polygon.
        """
        ...


Stream: TypeAlias = LineStream | PolygonStream


class Context(ABC):
    """
    Context definition
    """

    @abstractmethod
    def arc(self, x: float, y: float, r: float):
        """
        Adds an arc

        Parameters
        ----------
        x : float
            x value of the end point
        y : float
            y value of the end point
        r : float
            radius value
        """
        ...

    @abstractmethod
    def move_to(self, x: float, y: float):
        """
        Moves to a specific point

        Parameters
        ----------
        x : float
            x value of the end point
        y : float
            y value of the end point
        """
        ...

    @abstractmethod
    def line_to(self, x: float, y: float):
        """
        Makes a line

        Parameters
        ----------
        x : float
            x value of the end point
        y : float
            y value of the end point
        """
        ...

    @abstractmethod
    def close_path(self):
        """
        Closes the path
        """
        ...


class RawProjection(Protocol):
    """
    Raw projections are point transformation functions that are used to
    implement custom projections; they typically passed to geo_projection or
    geo_projection_mutator. They are exposed here to facilitate the derivation
    of related projections. Raw projections take spherical coordinates
    :code:`[lambda, phi]` in radians (not degrees!) and return a point
    :code:`[x, y]`, typically in the unit square centered around the origin.
    """

    def __call__(self, lambda_: float, phi: float) -> Point2D:
        """
        Projects the specified point :code:`[lambda, phi]` in radians,
        returning a new point :code:`[x, y]` in unitless coordinates.

        Parameters
        ----------
        lambda_ : float
            :math:`\\lambda` value
        phi : float
            :math:`\\phi` value

        Returns
        -------
        Point2D
            New point
        """
        ...

    def invert(self, x: float, y: float) -> Point2D:
        """
        Optional method: the inverse of the projection.

        Parameters
        ----------
        x : float
            x value
        y : float
            y value

        Returns
        -------
        Point2D
            :code:`[lambda, phi]` coordinates in radians
        """
        ...


TProjection = TypeVar("Projection", bound="Projection")


class Projection(ABC):
    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    def set_preclip(
        self, preclip: Callable[[PolygonStream], PolygonStream]
    ) -> TProjection:
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
        ...

    def set_postclip(
        self, postclip: Callable[[PolygonStream], PolygonStream]
    ) -> TProjection:
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
        ...

    def set_clip_angle(self, clip_angle: float | None = None) -> TProjection:
        """
        If angle is specified, sets the projection's clipping circle radius to
        the specified angle in degrees and returns the projection. If angle is
        :code:`None`, switches to antimeridian cutting rather than small-circle
        clipping. If angle is not specified, returns the current clip angle
        which defaults to :code:`None`. Small-circle clipping is independent of
        viewport clipping via projection.clipExtent.

        Parameters
        ----------
        clip_angle : float | None
            Clip angle

        Returns
        -------
        Projection
            Itself
        """
        ...

    def set_clip_extent(
        self, clip_extent: tuple[Point2D, Point2D] | None = None
    ) -> TProjection:
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
        ...

    @abstractmethod
    def scale(self, k: float) -> TProjection:
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
        ...

    @abstractmethod
    def translate(self, translation: Vec2D) -> TProjection:
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
        ...

    def set_center(self, center: Point2D) -> TProjection:
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
        ...

    def rotate(
        self, angles: tuple[float, float] | tuple[float, float, float]
    ) -> TProjection:
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
        ...

    def set_angle(self, angle: float) -> TProjection:
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
        ...

    def set_reflect_x(self, reflect_x: bool) -> TProjection:
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
        ...

    def set_reflect_y(self, reflect_y: bool) -> TProjection:
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
        ...

    @abstractmethod
    def set_precision(self, precision: float) -> TProjection:
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
        ...

    @abstractmethod
    def fit_extent(self, extent: tuple[Point2D, Point2D], obj: GeoJSON) -> TProjection:
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
        ...

    @abstractmethod
    def fit_size(self, size: Point2D, obj: GeoJSON) -> TProjection:
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
        ...

    @abstractmethod
    def fit_width(self, width: float, obj: GeoJSON) -> TProjection:
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
        ...

    @abstractmethod
    def fit_height(self, height: float, obj: GeoJSON) -> TProjection:
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
        ...
