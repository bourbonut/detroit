from .polygon_contains import polygon_contains
from .distance import geo_distance
from math import radians, nan

EPSILON2 = 1e-12

class ContainsObjectType:
    def Feature(obj, point):
        return contains_geometry(obj["geometry"], point)

    def FeatureCollection(obj, point):
        for feature in obj["features"]:
            if contains_geometry(feature["geometry"], point):
                return True
        return False

class ContainsGeometryType:
    def Sphere(obj, point):
        return True

    def Point(obj, point):
        return contains_point(obj["coordinates"], point)

    def MultiPoint(obj, point):
        for coordinates in obj["coordinates"]:
            if contains_point(coordinates, point):
                return True
        return False

    def LineString(obj, point):
        return contains_line(obj["coordinates"], point)

    def MultiLineString(obj, point):
        for coordinates in obj["coordinates"]:
            if contains_line(coordinates, point):
                return True
        return False

    def Polygon(obj, point):
        return contains_polygon(obj["coordinates"], point)

    def MultiPolygon(obj, point):
        for coordinates in obj["coordinates"]:
            if contains_polygon(coordinates, point):
                return True
        return False

    def GeometryCollection(obj, point):
        for geometry in obj["geometries"]:
            if contains_geometry(geometry, point):
                return True
        return False

def contains_geometry(geometry, point):
    if geometry and hasattr(ContainsGeometryType, geometry["type"]):
        return getattr(ContainsGeometryType, geometry["type"])(geometry, point)
    return False

def contains_point(coordinates, point):
    return geo_distance(coordinates, point) == 0

def contains_line(coordinates, point):
    ao = nan
    for i in range(len(coordinates)):
        bo = geo_distance(coordinates[i], point)
        if bo == 0:
            return True
        if i > 0:
            ab = geo_distance(coordinates[i], coordinates[i - 1])
            if (
                ab > 0 and
                ao <= ab and
                bo <= ab and
                (ao + bo - ab) * (1 - pow((ao - bo) / ab, 2)) < EPSILON2 * ab
            ):
                return True
        ao = bo
    return False

def contains_polygon(coordinates, point):
    return not(not(polygon_contains(list(map(ring_radians, coordinates)), point_radians(point))))

def ring_radians(ring):
    ring = [point_radians(p) for p in ring]
    ring.pop()
    return ring

def point_radians(point):
    return [radians(point[0]), radians(point[1])]

def geo_contains(obj, point):
    if obj and hasattr(ContainsObjectType, obj["type"]):
        return getattr(ContainsObjectType, obj["type"])(obj, point)
    else:
        return contains_geometry(obj, point)
