from ..types import Point2D
from .length import geo_length


def geo_distance(a: Point2D, b: Point2D) -> float:
    """
    Returns the great-arc distance in radians between the two points a and b.
    Each point must be specified as a two-element array :code:`[longitude,
    latitude]` in degrees. This is the spherical equivalent of
    :func:`GeoPath.measure <detroit.geo.path.path.GeoPath.measure>` given a
    LineString of two points.

    Parameters
    ----------
    a : Point2D
        2D point
    b : Point2D
        2D point

    Returns
    -------
    float
        Distance
    """
    return geo_length({"type": "LineString", "coordinates": [a, b]})
