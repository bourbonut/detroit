from math import atan, exp, inf, log, pi, tan

from ...types import Point2D
from ..common import Projection, RawProjection
from .mercator import MercatorProjection

half_pi = pi * 0.5


class TransverseMercatorRaw:
    def __call__(self, lambda_: float, phi: float) -> Point2D:
        t = tan((half_pi + phi) / 2)
        return [log(t) if t > 0.0 else -inf, -lambda_]

    def invert(self, x: float, y: float) -> Point2D:
        return [-y, 2 * atan(exp(x)) - half_pi]


class TransverseMercatorProjection(MercatorProjection):
    def __init__(self, project: RawProjection):
        MercatorProjection.__init__(self, project)
        super().rotate([0, 0, 90])
        super().scale(159.155)

    def set_center(self, center: Point2D) -> Projection:
        center = [-center[1], center[0]]
        return super().set_center(center)

    def get_center(self) -> Point2D:
        center = super().get_center()
        return [center[1], -center[0]]

    def rotate(self, angles: tuple[float, float, float]) -> Projection:
        angles = [angles[0], angles[1], angles[2] + 90 if len(angles) > 2 else 90]
        return super().rotate(angles)

    def get_rotation(self) -> tuple[float, float, float]:
        angles = super().get_rotation()
        return [angles[0], angles[1], angles[2] - 90]


def geo_transverse_mercator() -> Projection:
    """
    The transverse spherical Mercator projection. Defines a default
    :func:`Projection.set_clip_extent
    <detroit.geo.common.Projection.set_clip_extent>` such that the world is
    projected to a square, clipped to approximately :math:`\\pm 85°` latitude.

    Returns
    -------
    Projection
        Projection object
    """
    return TransverseMercatorProjection(TransverseMercatorRaw())
