from math import atan, exp, pi, log, tan
from .mercator import MercatorProjection
from ..common import Projection
from ...types import Point2D

half_pi = pi * 0.5

class TransverseMercatorRaw:

    def __call__(self, lambda_: float, phi: float) -> Point2D:
        return [log(tan((half_pi + phi) / 2)), -lambda_]

    def invert(self, x: float, y: float) -> Point2D:
        return [-y, 2 * atan(exp(x)) - half_pi]


class TransverseMercatorProjection(MercatorProjection):
    def set_center(self, center: Point2D) -> Projection:
        center = [-center[1], center[0]]
        return super().set_center(center)

    def get_center(self) -> Point2D:
        center = super().get_center()
        return [center[1], -center[0]]

    def rotate(self, angles: tuple[float, float, float]) -> Projection:
        angles = [angles[0], angles[1], angles[2] + 90 if len(angles) > 2 else 90]
        return super().rotate(angles)

    def get_angle(self) -> tuple[float, float, float]:
        angles = super().get_angle()
        return [angles[0], angles[1], angles[2] - 90]

def geo_transverse_mercator():
    return TransverseMercatorProjection(TransverseMercatorRaw()).rotate([0, 0, 90]).scale(159.155)
