from collections.abc import Callable
from math import cos, degrees, radians, sin, sqrt
from typing import Any, TypeVar

from ...array import argpass
from ...types import GeoJSON, Point2D, Vec2D
from ..clip import geo_clip_antimeridian, geo_clip_circle, geo_clip_rectangle
from ..common import PolygonStream, Projection, RawProjection, SpatialTransform
from ..compose import Compose
from ..rotation import RotateRadians
from ..transform import GeoTransformer
from .fit import fit_extent, fit_height, fit_size, fit_width
from .resample import resample

TProjectionMutator = TypeVar("ProjectionMutator", bound="ProjectionMutator")


def point(self, x: float, y: float):
    self._stream.point(radians(x), radians(y))


transform_radians = GeoTransformer({"point": point})


def transform_rotate(rotate: RotateRadians) -> GeoTransformer:
    def point(self, x: float, y: float):
        a, b = rotate(x, y)
        return self._stream.point(a, b)

    return GeoTransformer({"point": point})


class ScaleTranslate:
    def __init__(self, k: float, dx: float, dy: float, sx: float, sy: float):
        self._k = k
        self._dx = dx
        self._dy = dy
        self._sx = sx
        self._sy = sy

    def __call__(self, x: float, y: float) -> Point2D:
        x *= self._sx
        y *= self._sy
        return [self._dx + self._k * x, self._dy - self._k * y]

    def invert(self, x: float, y: float) -> Point2D:
        return [
            (x - self._dx) / self._k * self._sx,
            (self._dy - y) / self._k * self._sy,
        ]


class ScaleTranslateRotate:
    def __init__(
        self, k: float, dx: float, dy: float, sx: float, sy: float, alpha: float
    ):
        self._cos_alpha = cos(alpha)
        self._sin_alpha = sin(alpha)
        self._sx = sx
        self._sy = sy
        self._k = k
        self._dx = dx
        self._dy = dy
        self._a = self._cos_alpha * self._k
        self._b = self._sin_alpha * self._k
        self._ai = self._cos_alpha / self._k
        self._bi = self._sin_alpha / self._k
        self._ci = (self._sin_alpha * self._dy - self._cos_alpha * self._dx) / self._k
        self._fi = (self._sin_alpha * self._dx + self._cos_alpha * self._dy) / self._k

    def __call__(self, x: float, y: float) -> Point2D:
        x *= self._sx
        y *= self._sy
        return [
            self._a * x - self._b * y + self._dx,
            self._dy - self._b * x - self._a * y,
        ]

    def invert(self, x: float, y: float) -> Point2D:
        return [
            self._sx * (self._ai * x - self._bi * y + self._ci),
            self._sy * (self._fi - self._bi * x - self._ai * y),
        ]


def scale_translate_rotate(
    k: float, dx: float, dy: float, sx: float, sy: float, alpha: float
) -> SpatialTransform:
    if alpha:
        return ScaleTranslateRotate(k, dx, dy, sx, sy, alpha)
    else:
        return ScaleTranslate(k, dx, dy, sx, sy)


def identity(x):
    return x


class RawProjectionIdentity:
    def __call__(self, lambda_: float, phi: float) -> Point2D:
        return [lambda_, phi]

    def invert(self, x: float, y: float) -> Point2D:
        return self(x, y)


class ProjectionMutator(Projection):
    """
    Projections transform spherical polygonal geometry to planar polygonal
    geometry. Several classes of standard projections are provided:

    - Azimuthal projections
    - Conic projections
    - Cylindrical projections

    Parameters
    ----------
    project : RawProjection
        Projection object
    """

    def __init__(self, project: RawProjection):
        self._project = project
        self._invert = (
            self._invert_default if hasattr(project, "invert") else self._invert_error
        )
        self._k = 150
        self._x = 480
        self._y = 250
        self._lambda = 0
        self._phi = 0
        self._delta_lambda = 0
        self._delta_phi = 0
        self._delta_gamma = 0
        self._rotate = None
        self._alpha = 0
        self._sx = 1
        self._sy = 1
        self._theta = None
        self._preclip = geo_clip_antimeridian
        self._x0 = None
        self._y0 = None
        self._x1 = None
        self._y1 = None
        self._postclip = identity
        self._delta2 = 0.5
        self._project_resample = None
        self._project_transform = None
        self._project_rotate_transform = None
        self._cache = None
        self._cache_stream = None
        self.recenter()

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
        return self._project_rotate_transform(radians(point[0]), radians(point[1]))

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
        return self._invert(point)

    def _invert_default(self, point: Point2D) -> Point2D:
        point = self._project_rotate_transform.invert(point[0], point[1])
        if point is not None:
            return [degrees(point[0]), degrees(point[1])]

    def _invert_error(self, point: Point2D):
        raise NotImplementedError("Projection does not support invert method.")

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
        clipped_stream = self._preclip(self._project_resample(self._postclip(stream)))
        self._cache = transform_radians(transform_rotate(self._rotate)(clipped_stream))
        return self._cache

    def set_project(self, project: RawProjection) -> TProjectionMutator:
        """
        Updates the raw projection object and returns itself

        Parameters
        ----------
        project : RawProjection
            Raw projection object

        Returns
        -------
        ProjectionMutator
            Itself
        """
        self._project = project
        self._invert = (
            self._invert_default if hasattr(project, "invert") else self._invert_error
        )
        return self.recenter()

    def set_preclip(
        self, preclip: Callable[[PolygonStream], PolygonStream]
    ) -> TProjectionMutator:
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
        ProjectionMutator
            Itself
        """
        self._preclip = preclip
        self._theta = None
        return self.reset()

    def set_postclip(
        self, postclip: Callable[[PolygonStream], PolygonStream]
    ) -> TProjectionMutator:
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
        ProjectionMutator
            Itself
        """
        self._postclip = postclip
        self._x0 = None
        self._x1 = None
        self._y0 = None
        self._y1 = None
        return self.reset()

    def set_clip_angle(self, clip_angle: float | None = None) -> TProjectionMutator:
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
        ProjectionMutator
            Itself
        """
        if clip_angle:
            self._theta = radians(clip_angle)
            self._preclip = geo_clip_circle(self._theta)
        else:
            self._theta = None
            self._preclip = geo_clip_antimeridian
        return self.reset()

    def set_clip_extent(
        self, clip_extent: tuple[Point2D, Point2D] | None = None
    ) -> TProjectionMutator:
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
        ProjectionMutator
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

    def scale(self, k: float) -> TProjectionMutator:
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
        ProjectionMutator
            Itself
        """
        self._k = k
        return self.recenter()

    def translate(self, translation: Vec2D) -> TProjectionMutator:
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
        ProjectionMutator
            Itself
        """
        self._x = translation[0]
        self._y = translation[1]
        return self.recenter()

    def set_center(self, center: Point2D) -> TProjectionMutator:
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
        ProjectionMutator
            Itself
        """
        self._lambda = radians(center[0])
        self._phi = radians(center[1])
        return self.recenter()

    def rotate(
        self, angles: tuple[float, float] | tuple[float, float, float]
    ) -> TProjectionMutator:
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
        ProjectionMutator
            Itself
        """
        self._delta_lambda = radians(angles[0])
        self._delta_phi = radians(angles[1])
        self._delta_gamma = radians(angles[2]) if len(angles) > 2 else 0
        return self.recenter()

    def set_angle(self, angle: float) -> TProjectionMutator:
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
        ProjectionMutator
            Itself
        """
        self._alpha = radians(angle)
        return self.recenter()

    def set_reflect_x(self, reflect_x: bool) -> TProjectionMutator:
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
        ProjectionMutator
            Itself
        """
        self._sx = -1 if reflect_x else 1
        return self.recenter()

    def set_reflect_y(self, reflect_y: bool) -> TProjectionMutator:
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
        ProjectionMutator
            Itself
        """
        self._sy = -1 if reflect_y else 1
        return self.recenter()

    def set_precision(self, precision: float) -> TProjectionMutator:
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
        ProjectionMutator
            Itself
        """
        self._delta2 = precision * precision
        self._project_resample = resample(self._project_transform, self._delta2)
        return self.reset()

    def fit_extent(
        self, extent: tuple[Point2D, Point2D], obj: GeoJSON
    ) -> TProjectionMutator:
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
        ProjectionMutator
            Itself
        """
        return fit_extent(self, extent, obj)

    def fit_size(self, size: Point2D, obj: GeoJSON) -> TProjectionMutator:
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
        ProjectionMutator
            Itself
        """
        return fit_size(self, size, obj)

    def fit_width(self, width: float, obj: GeoJSON) -> TProjectionMutator:
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
        ProjectionMutator
            Itself
        """
        return fit_width(self, width, obj)

    def fit_height(self, height: float, obj: GeoJSON) -> TProjectionMutator:
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
        ProjectionMutator
            Itself
        """
        return fit_height(self, height, obj)

    def recenter(self) -> TProjectionMutator:
        center = scale_translate_rotate(self._k, 0, 0, self._sx, self._sy, self._alpha)(
            *self._project(self._lambda, self._phi)
        )
        transform = scale_translate_rotate(
            self._k,
            self._x - center[0],
            self._y - center[1],
            self._sx,
            self._sy,
            self._alpha,
        )
        self._rotate = RotateRadians(
            self._delta_lambda, self._delta_phi, self._delta_gamma
        )
        self._project_transform = Compose(self._project, transform)
        self._project_rotate_transform = Compose(self._rotate, self._project_transform)
        self._project_resample = resample(self._project_transform, self._delta2)
        return self.reset()

    def reset(self) -> TProjectionMutator:
        self._cache = None
        self._cache_stream = None
        return self

    def get_preclip(self) -> Callable[[PolygonStream], PolygonStream]:
        return self._preclip

    def get_postclip(self) -> Callable[[PolygonStream], PolygonStream]:
        return self._postclip

    def get_clip_angle(self) -> float:
        return radians(self._theta)

    def get_clip_extent(self) -> tuple[Point2D, Point2D] | None:
        if self._x0 is None:
            return None
        else:
            return [[self._x0, self._y0], [self._x1, self._y1]]

    def get_scale(self) -> float:
        return self._k

    def get_translation(self) -> Vec2D:
        return [self._x, self._y]

    def get_center(self) -> Point2D:
        return [degrees(self._lambda), degrees(self._phi)]

    def get_rotation(self) -> tuple[float, float, float]:
        return [
            degrees(self._delta_lambda),
            degrees(self._delta_phi),
            degrees(self._delta_gamma),
        ]

    def get_angle(self) -> float:
        return degrees(self._alpha)

    def get_reflect_x(self) -> bool:
        return self._sx < 0

    def get_reflect_y(self) -> bool:
        return self._sy < 0

    def get_precision(self) -> float:
        return sqrt(self._delta2)


def geo_projection(project: RawProjection) -> Projection:
    """
    Constructs a new projection from the specified raw projection :code:`project`.
    The :code:`project` function takes the longitude and latitude of a given
    point in radians, often referred to as :code:`lambda` (:math:`\\lambda`)
    and :code:`phi` (:math:`\\phi`), and returns a two-element array :code:`[x,
    y]` representing its unit projection. The project function does not need to
    scale or translate the point, as these are applied automatically by
    projection.scale, projection.translate, and projection.center. Likewise,
    the project function does not need to perform any spherical rotation, as
    projection.rotate is applied prior to projection.

    Parameters
    ----------
    project : RawProjection
        Projection object

    Returns
    -------
    Projection
        Projection object
    """
    return ProjectionMutator(project)


def geo_projection_mutator(
    project: Callable[..., RawProjection],
) -> Callable[..., Projection]:
    """
    Constructs a new projection from the specified raw projection factory and
    returns a mutate function to call whenever the raw projection changes. The
    factory must return a raw projection. The returned mutate function returns
    the wrapped projection. For example, a conic projection typically has two
    configurable parallels.

    Parameters
    ----------
    project : Callable[..., RawProjection]
        Function which generates a projection object

    Returns
    -------
    Callable[..., Projection]
        Projection object
    """
    projection = ProjectionMutator(RawProjectionIdentity())

    def projection_constructor(*args: Any) -> Projection:
        return projection.set_project(argpass(project)(*args))

    return projection_constructor
