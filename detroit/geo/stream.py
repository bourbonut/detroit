from ..array import argpass

def get(values, index):
    return values[index] if index < len(values) else None

def stream_geometry(geometry, stream):
    if geometry and hasattr(StreamGeometryType, geometry["type"]):
        getattr(StreamGeometryType, geometry["type"])(geometry, stream)
        

class StreamObjectType:

    @staticmethod
    def Feature(obj, stream):
        stream_geometry(obj["geometry"], stream)

    @staticmethod
    def FeatureCollection(obj, stream):
        features = obj["features"]
        for feature in features:
            stream_geometry(feature["geometry"], stream)

class StreamGeometryType:
    
    @staticmethod
    def Sphere(obj, stream):
        stream.sphere()

    @staticmethod
    def Point(obj, stream):
        obj = obj["coordinates"]
        argpass(stream.point)(get(obj, 0), get(obj, 1), get(obj, 2))

    @staticmethod
    def MultiPoint(obj, stream):
        coordinates = obj["coordinates"]
        for obj in coordinates:
            argpass(stream.point)(get(obj, 0), get(obj, 1), get(obj, 2))

    @staticmethod
    def LineString(obj, stream):
        stream_line(obj["coordinates"], stream, 0)

    @staticmethod
    def MultiLineString(obj, stream):
        coordinates = obj["coordinates"]
        for obj in coordinates:
            stream_line(obj, stream, 0)

    @staticmethod
    def Polygon(obj, stream):
        stream_polygon(obj["coordinates"], stream)

    @staticmethod
    def MultiPolygon(obj, stream):
        coordinates = obj["coordinates"]
        for obj in coordinates:
            stream_polygon(obj, stream)

    @staticmethod
    def GeometryCollection(obj, stream):
        geometries = obj["geometries"]
        for obj in geometries:
            stream_geometry(obj, stream)

def stream_line(coordinates, stream, closed):
    stream.line_start()
    coordinates = coordinates[:-1] if closed else coordinates
    for coordinate in coordinates:
        stream.point(coordinate[0], coordinate[1], coordinate[2])
    stream.line_end()

def stream_polygon(coordinates, stream):
    stream.polygon_start()
    for coordinate in coordinates:
        stream_line(coordinate, stream, 1)
    stream.polygon_end()

def stream(obj, stream):
    if obj and hasattr(StreamObjectType, obj["type"]):
        getattr(StreamObjectType, obj["type"])(obj, stream)
    else:
        stream_geometry(obj, stream)
