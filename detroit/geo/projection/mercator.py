from math import atan, exp, inf, log, pi, tan

from ...types import Point2D, Vec2D
from ..common import Projection, RawProjection
from ..rotation import geo_rotation
from .projection import ProjectionMutator

TAU = 2 * pi
half_pi = pi / 2


class MercatorRaw:
    def __call__(self, lambda_: float, phi: float) -> Point2D:
        t = tan((half_pi + phi) / 2)
        return [lambda_, log(t) if t > 0.0 else -inf]

    def invert(self, x: float, y: float) -> Point2D:
        return [x, 2 * atan(exp(y)) - half_pi]


class MercatorProjection(ProjectionMutator):
    def __init__(self, project: RawProjection):
        ProjectionMutator.__init__(self, project)
        self._project = project
        self._mx0 = None
        self._my0 = None
        self._mx1 = None
        self._my1 = None
        self.reclip()

    def scale(self, k: float) -> Projection:
        super().scale(k)
        return self.reclip()

    def translate(self, translation: Vec2D) -> Projection:
        super().translate(translation)
        return self.reclip()

    def set_center(self, center: Point2D) -> Projection:
        super().set_center(center)
        return self.reclip()

    def set_clip_extent(
        self, clip_extent: tuple[Point2D, Point2D] | None = None
    ) -> Projection:
        if clip_extent is None:
            self._mx0 = None
            self._my0 = None
            self._mx1 = None
            self._my1 = None
        else:
            self._mx0 = clip_extent[0][0]
            self._my0 = clip_extent[0][1]
            self._mx1 = clip_extent[1][0]
            self._my1 = clip_extent[1][1]
        return self.reclip()

    def get_clip_extent(self) -> tuple[Point2D, Point2D] | None:
        if self._mx0 is None:
            return None
        else:
            return [[self._mx0, self._my0], [self._mx1, self._my1]]

    def reclip(self) -> Projection:
        k = pi * self.get_scale()
        t = self(geo_rotation(self.get_rotation()).invert([0, 0]))
        if self._mx0 is None:
            return super().set_clip_extent([[t[0] - k, t[1] - k], [t[0] + k, t[1] + k]])
        elif isinstance(self._project, MercatorRaw):
            return super().set_clip_extent(
                [
                    [max(t[0] - k, self._mx0), self._my0],
                    [min(t[0] + k, self._mx1), self._my1],
                ]
            )
        else:
            return super().set_clip_extent(
                [
                    [self._mx0, max(t[1] - k, self._my0)],
                    [self._mx1, min(t[1] + k, self._my1)],
                ]
            )


def geo_mercator() -> Projection:
    """
    The spherical Mercator projection. Defines a default
    :func:`Projection.set_clip_extent
    <detroit.geo.common.Projection.set_clip_extent>` such that the world is
    projected to a square, clipped to approximately :math:`\\pm 85°` latitude.

    Returns
    -------
    Projection
        Projection object
    """
    return MercatorProjection(MercatorRaw()).scale(961 / TAU)
