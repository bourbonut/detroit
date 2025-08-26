from math import asin, atan2, cos, fsum, pi, sin

from ..types import Point2D
from .cartesian import cartesian, cartesian_cross, cartesian_normalize_in_place

EPSILON = 1e-6
EPSILON2 = 1e-12
TAU = 2 * pi
half_pi = pi * 0.5
quarter_pi = pi * 0.25


def sign(x: float) -> float:
    return -1 if x < 0 else 1


def longitude(point: Point2D) -> float:
    if abs(point[0]) <= pi:
        return point[0]
    else:
        return sign(point[0]) * ((abs(point[0]) + pi) % TAU - pi)


def polygon_contains(polygon: list[list[float]], point: tuple[float, float]) -> int:
    lambda_ = longitude(point)
    phi = point[1]
    sin_phi = sin(phi)
    normal = [sin(lambda_), -cos(lambda_), 0]
    angle = 0
    winding = 0

    sum = []

    if sin_phi == 1.0:
        phi = half_pi + EPSILON
    elif sin_phi == -1.0:
        phi = -half_pi - EPSILON

    for ring in polygon:
        m = len(ring)
        if m == 0:
            continue
        point0 = ring[m - 1]
        lambda0 = longitude(point0)
        phi0 = point0[1] * 0.5 + quarter_pi
        sin_phi0 = sin(phi0)
        cos_phi0 = cos(phi0)

        for j in range(m):
            point1 = ring[j]
            lambda1 = longitude(point1)
            phi1 = point1[1] * 0.5 + quarter_pi
            sin_phi1 = sin(phi1)
            cos_phi1 = cos(phi1)
            delta = lambda1 - lambda0
            sign_ = sign(delta)
            abs_delta = sign_ * delta
            antimeridian = abs_delta > pi
            k = sin_phi0 * sin_phi1

            sum.append(
                atan2(
                    k * sign_ * sin(abs_delta), cos_phi0 * cos_phi1 + k * cos(abs_delta)
                )
            )
            angle += delta + sign_ * TAU if antimeridian else delta

            if (antimeridian ^ (lambda0 >= lambda_)) ^ (lambda1 >= lambda_):
                arc = cartesian_cross(cartesian(point0), cartesian(point1))
                cartesian_normalize_in_place(arc)
                intersection = cartesian_cross(normal, arc)
                cartesian_normalize_in_place(intersection)
                phi_arc = (-1 if antimeridian ^ (delta >= 0) else 1) * asin(
                    intersection[2]
                )
                if phi > phi_arc or phi == phi_arc and (arc[0] or arc[1]):
                    winding += 1 if antimeridian ^ (delta >= 0) else -1

            lambda0 = lambda1
            sin_phi0 = sin_phi1
            cos_phi0 = cos_phi1
            point0 = point1

    return (angle < -EPSILON or angle < EPSILON and fsum(sum) < -EPSILON2) ^ (
        winding & 1
    )
