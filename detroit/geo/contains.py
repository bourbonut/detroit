from math import nan, radians

from ..types import GeoJSON, Point2D
from .distance import geo_distance
from .polygon_contains import polygon_contains

EPSILON2 = 1e-12


class ContainsObjectType:
    def Feature(obj: GeoJSON, point: Point2D) -> bool:
        return contains_geometry(obj["geometry"], point)

    def FeatureCollection(obj: GeoJSON, point: Point2D) -> bool:
        for feature in obj["features"]:
            if contains_geometry(feature["geometry"], point):
                return True
        return False


class ContainsGeometryType:
    def Sphere(obj: GeoJSON, point: Point2D) -> bool:
        return True

    def Point(obj: GeoJSON, point: Point2D) -> bool:
        return contains_point(obj["coordinates"], point)

    def MultiPoint(obj: GeoJSON, point: Point2D) -> bool:
        for coordinates in obj["coordinates"]:
            if contains_point(coordinates, point):
                return True
        return False

    def LineString(obj: GeoJSON, point: Point2D) -> bool:
        return contains_line(obj["coordinates"], point)

    def MultiLineString(obj: GeoJSON, point: Point2D) -> bool:
        for coordinates in obj["coordinates"]:
            if contains_line(coordinates, point):
                return True
        return False

    def Polygon(obj: GeoJSON, point: Point2D) -> bool:
        return contains_polygon(obj["coordinates"], point)

    def MultiPolygon(obj: GeoJSON, point: Point2D) -> bool:
        for coordinates in obj["coordinates"]:
            if contains_polygon(coordinates, point):
                return True
        return False

    def GeometryCollection(obj: GeoJSON, point: Point2D) -> bool:
        for geometry in obj["geometries"]:
            if contains_geometry(geometry, point):
                return True
        return False


def contains_geometry(geometry: GeoJSON, point: Point2D) -> bool:
    if geometry and hasattr(ContainsGeometryType, geometry["type"]):
        return getattr(ContainsGeometryType, geometry["type"])(geometry, point)
    return False


def contains_point(coordinates: GeoJSON, point: Point2D) -> bool:
    return geo_distance(coordinates, point) == 0


def contains_line(coordinates: list[Point2D], point: Point2D) -> bool:
    ao = nan
    for i in range(len(coordinates)):
        bo = geo_distance(coordinates[i], point)
        if bo == 0:
            return True
        if i > 0:
            ab = geo_distance(coordinates[i], coordinates[i - 1])
            if (
                ab > 0
                and ao <= ab
                and bo <= ab
                and (ao + bo - ab) * (1 - pow((ao - bo) / ab, 2)) < EPSILON2 * ab
            ):
                return True
        ao = bo
    return False


def contains_polygon(coordinates: list[list[Point2D]], point: Point2D) -> bool:
    return not (
        not (
            polygon_contains(list(map(ring_radians, coordinates)), point_radians(point))
        )
    )


def ring_radians(ring: list[Point2D]) -> list[Point2D]:
    ring = [point_radians(p) for p in ring]
    ring.pop()
    return ring


def point_radians(point: Point2D):
    return [radians(point[0]), radians(point[1])]


def geo_contains(obj: GeoJSON, point: Point2D) -> bool:
    """
    Returns :code:`True` if and only if the specified GeoJSON object contains
    the specified point, or :code:`False` if the object does not contain the
    point. The point must be specified as a two-element array
    :code:`[longitude, latitude]` in degrees. For Point and MultiPoint
    geometries, an exact test is used; for a Sphere, true is always returned;
    for other geometries, an epsilon threshold is applied.

    Parameters
    ----------
    obj : GeoJSON
        GeoJSON object
    point : Point2D
        2D point

    Returns
    -------
    bool
       :code:`True` if the GeoJSON object contains the point else :code:`False`
    """
    if obj and hasattr(ContainsObjectType, obj["type"]):
        return getattr(ContainsObjectType, obj["type"])(obj, point)
    else:
        return contains_geometry(obj, point)
