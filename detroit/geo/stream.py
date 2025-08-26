from ..array import argpass
from ..types import GeoJSON, T
from .common import PolygonStream


def get(values: list[T], index: int) -> T | None:
    return values[index] if index < len(values) else None


def stream_geometry(geometry: GeoJSON, stream: PolygonStream):
    if geometry and hasattr(StreamGeometryType, geometry["type"]):
        getattr(StreamGeometryType, geometry["type"])(geometry, stream)


class StreamObjectType:
    @staticmethod
    def Feature(obj: GeoJSON, stream: PolygonStream):
        stream_geometry(obj["geometry"], stream)

    @staticmethod
    def FeatureCollection(obj: GeoJSON, stream: PolygonStream):
        features = obj["features"]
        for feature in features:
            stream_geometry(feature["geometry"], stream)


class StreamGeometryType:
    @staticmethod
    def Sphere(obj: GeoJSON, stream: PolygonStream):
        stream.sphere()

    @staticmethod
    def Point(obj: GeoJSON, stream: PolygonStream):
        obj = obj["coordinates"]
        argpass(stream.point)(get(obj, 0), get(obj, 1), get(obj, 2))

    @staticmethod
    def MultiPoint(obj: GeoJSON, stream: PolygonStream):
        coordinates = obj["coordinates"]
        for obj in coordinates:
            argpass(stream.point)(get(obj, 0), get(obj, 1), get(obj, 2))

    @staticmethod
    def LineString(obj: GeoJSON, stream: PolygonStream):
        stream_line(obj["coordinates"], stream, False)

    @staticmethod
    def MultiLineString(obj: GeoJSON, stream: PolygonStream):
        coordinates = obj["coordinates"]
        for obj in coordinates:
            stream_line(obj, stream, False)

    @staticmethod
    def Polygon(obj: GeoJSON, stream: PolygonStream):
        stream_polygon(obj["coordinates"], stream)

    @staticmethod
    def MultiPolygon(obj: GeoJSON, stream: PolygonStream):
        coordinates = obj["coordinates"]
        for obj in coordinates:
            stream_polygon(obj, stream)

    @staticmethod
    def GeometryCollection(obj: GeoJSON, stream: PolygonStream):
        geometries = obj["geometries"]
        for obj in geometries:
            stream_geometry(obj, stream)


def stream_line(coordinates: list[T], stream: PolygonStream, closed: bool):
    stream.line_start()
    coordinates = coordinates[:-1] if closed else coordinates
    for coordinate in coordinates:
        argpass(stream.point)(
            get(coordinate, 0), get(coordinate, 1), get(coordinate, 2)
        )
    stream.line_end()


def stream_polygon(coordinates: list[T], stream: PolygonStream):
    stream.polygon_start()
    for coordinate in coordinates:
        stream_line(coordinate, stream, True)
    stream.polygon_end()


def geo_stream(obj: GeoJSON, stream: PolygonStream):
    """
    Streams the specified GeoJSON object to the specified projection stream.
    While both features and geometry objects are supported as input, the stream
    interface only describes the geometry, and thus additional feature
    properties are not visible to streams.

    Parameters
    ----------
    obj : GeoJSON
        GeoJSON object
    stream : PolygonStream
        Stream object
    """
    if obj and hasattr(StreamObjectType, obj["type"]):
        getattr(StreamObjectType, obj["type"])(obj, stream)
    else:
        stream_geometry(obj, stream)
