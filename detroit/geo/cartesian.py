from math import asin, atan2, cos, nan, sin, sqrt

from ..types import Point3D, Vec3D


def spherical(cartesian: Point3D) -> Point3D:
    return [atan2(cartesian[1], cartesian[0]), asin(cartesian[2])]


def cartesian(spherical: Point3D) -> Point3D:
    lambda_ = spherical[0]
    phi = spherical[1]
    cos_phi = cos(phi)
    return [cos_phi * cos(lambda_), cos_phi * sin(lambda_), sin(phi)]


def cartesian_dot(a: Vec3D, b: Vec3D) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cartesian_cross(a: Vec3D, b: Vec3D) -> Vec3D:
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


def cartesian_add_in_place(a: Vec3D, b: Vec3D):
    a[0] += b[0]
    a[1] += b[1]
    a[2] += b[2]


def cartesian_scale(vector: Vec3D, k: float) -> Vec3D:
    return [vector[0] * k, vector[1] * k, vector[2] * k]


def cartesian_normalize_in_place(d: Vec3D):
    length = sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2])
    if length == 0.0:
        return [nan, nan, nan]
    d[0] /= length
    d[1] /= length
    d[2] /= length
