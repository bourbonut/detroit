from math import asin, atan2, cos, sin, sqrt

def spherical(cartesian):
    return [atan2(cartesian[1], cartesian[0]), asin(cartesian[2])]

def cartesian(spherical):
    lambda_ = spherical[0]
    phi = spherical[1]
    cos_phi = cos(phi)
    return [cos_phi * cos(lambda_), cos_phi * sin(lambda_), sin(phi)]

def cartesian_dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def cartesian_cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]

def cartesian_add_in_place(a, b):
    a[0] += b[0]
    a[1] += b[1]
    a[2] += b[2]

def cartesian_scale(vector, k):
    return [vector[0] * k, vector[1] * k, vector[2] * k]

def cartesian_normalize_in_place(d):
    length = sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2])
    d[0] /= length
    d[1] /= length
    d[2] /= length
