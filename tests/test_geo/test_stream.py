import detroit as d3


class DefaultPoint:
    def point(self):
        return


class DefaultSphere:
    def sphere(self):
        return


def test_stream_1():
    d3.geo_stream({"type": "Unknown"}, DefaultPoint())
    d3.geo_stream({"type": "Feature", "geometry": {"type": "Unknown"}}, DefaultPoint())
    d3.geo_stream(
        {
            "type": "FeatureCollection",
            "features": [{"type": "Feature", "geometry": {"type": "Unknown"}}],
        },
        DefaultPoint(),
    )
    d3.geo_stream(
        {"type": "GeometryCollection", "geometries": [{"type": "Unknown"}]},
        DefaultPoint(),
    )


def test_stream_2():
    d3.geo_stream(None, {})
    d3.geo_stream({"type": "Feature", "geometry": None}, DefaultPoint())
    d3.geo_stream(
        {
            "type": "FeatureCollection",
            "features": [{"type": "Feature", "geometry": None}],
        },
        DefaultPoint(),
    )
    d3.geo_stream({"type": "GeometryCollection", "geometries": [None]}, DefaultPoint())


def test_stream_3():
    assert (
        d3.geo_stream({"type": "Point", "coordinates": [1, 2]}, DefaultPoint()) is None
    )


def test_stream_4():
    d3.geo_stream({"type": "MultiPoint", "coordinates": []}, DefaultPoint())
    d3.geo_stream({"type": "MultiLineString", "coordinates": []}, DefaultPoint())
    d3.geo_stream({"type": "MultiPolygon", "coordinates": []}, DefaultPoint())


def test_stream_5():
    calls = [0]

    class Sphere:
        def sphere(self):
            calls[0] += 1
            return

    d3.geo_stream({"type": "Sphere"}, Sphere())
    assert calls[0] == 1


def test_stream_6():
    calls = [0]
    coordinates = [0]

    class Point:
        def point(self, x, y, z):
            coordinates[0] += 1
            assert x == coordinates[0]
            coordinates[0] += 1
            assert y == coordinates[0]
            coordinates[0] += 1
            assert z == coordinates[0]
            calls[0] += 1
            return

    d3.geo_stream({"type": "Point", "coordinates": [1, 2, 3]}, Point())
    assert calls[0] == 1


def test_stream_7():
    calls = [0]
    coordinates = [0]

    class Point:
        def point(self, x, y, z):
            coordinates[0] += 1
            assert x == coordinates[0]
            coordinates[0] += 1
            assert y == coordinates[0]
            coordinates[0] += 1
            assert z == coordinates[0]
            calls[0] += 1
            assert calls[0] <= 2
            return

    d3.geo_stream(
        {"type": "MultiPoint", "coordinates": [[1, 2, 3], [4, 5, 6]]}, Point()
    )
    assert calls[0] == 2


def test_stream_8():
    calls = [0]
    coordinates = [0]

    class Obj:
        def line_start(self):
            calls[0] += 1
            assert calls[0] == 1

        def point(self, x, y, z):
            coordinates[0] += 1
            assert x == coordinates[0]
            coordinates[0] += 1
            assert y == coordinates[0]
            coordinates[0] += 1
            assert z == coordinates[0]
            calls[0] += 1
            assert 2 <= calls[0] <= 3
            return

        def line_end(self):
            calls[0] += 1
            assert calls[0] == 4

    d3.geo_stream({"type": "LineString", "coordinates": [[1, 2, 3], [4, 5, 6]]}, Obj())
    assert calls[0] == 4


def test_stream_9():
    calls = [0]
    coordinates = [0]

    class Obj:
        def line_start(self):
            calls[0] += 1
            assert calls[0] == 1 or calls[0] == 5

        def point(self, x, y, z):
            coordinates[0] += 1
            assert x == coordinates[0]
            coordinates[0] += 1
            assert y == coordinates[0]
            coordinates[0] += 1
            assert z == coordinates[0]
            calls[0] += 1
            assert 2 <= calls[0] <= 3 or 6 <= calls[0] <= 7
            return

        def line_end(self):
            calls[0] += 1
            assert calls[0] == 4 or calls[0] == 8

    d3.geo_stream(
        {
            "type": "MultiLineString",
            "coordinates": [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]],
        },
        Obj(),
    )
    assert calls[0] == 8


def test_stream_16():
    calls = [0]
    coordinates = [0]

    class Obj:
        def polygon_start(self):
            calls[0] += 1
            assert calls[0] == 1

        def line_start(self):
            calls[0] += 1
            assert calls[0] == 2 or calls[0] == 6

        def point(self, x, y, z):
            coordinates[0] += 1
            assert x == coordinates[0]
            coordinates[0] += 1
            assert y == coordinates[0]
            coordinates[0] += 1
            assert z == coordinates[0]
            calls[0] += 1
            assert 3 <= calls[0] <= 4 or 7 <= calls[0] <= 8
            return

        def line_end(self):
            calls[0] += 1
            assert calls[0] == 5 or calls[0] == 9

        def polygon_end(self):
            calls[0] += 1
            assert calls[0] == 10

    d3.geo_stream(
        {
            "type": "Polygon",
            "coordinates": [
                [[1, 2, 3], [4, 5, 6], [1, 2, 3]],
                [[7, 8, 9], [10, 11, 12], [7, 8, 9]],
            ],
        },
        Obj(),
    )
    assert calls[0] == 10


def test_stream_17():
    calls = [0]
    coordinates = [0]

    class Obj:
        def polygon_start(self):
            calls[0] += 1
            assert calls[0] == 1 or calls[0] == 7

        def line_start(self):
            calls[0] += 1
            assert calls[0] == 2 or calls[0] == 8

        def point(self, x, y, z):
            coordinates[0] += 1
            assert x == coordinates[0]
            coordinates[0] += 1
            assert y == coordinates[0]
            coordinates[0] += 1
            assert z == coordinates[0]
            calls[0] += 1
            assert 3 <= calls[0] <= 4 or 9 <= calls[0] <= 10
            return

        def line_end(self):
            calls[0] += 1
            assert calls[0] == 5 or calls[0] == 11

        def polygon_end(self):
            calls[0] += 1
            assert calls[0] == 6 or calls[0] == 12

    d3.geo_stream(
        {
            "type": "MultiPolygon",
            "coordinates": [
                [[[1, 2, 3], [4, 5, 6], [1, 2, 3]]],
                [[[7, 8, 9], [10, 11, 12], [7, 8, 9]]],
            ],
        },
        Obj(),
    )
    assert calls[0] == 12


def test_stream_18():
    calls = [0]
    coordinates = [0]

    class Point:
        def point(self, x, y, z):
            coordinates[0] += 1
            assert x == coordinates[0]
            coordinates[0] += 1
            assert y == coordinates[0]
            coordinates[0] += 1
            assert z == coordinates[0]
            calls[0] += 1
            return

    d3.geo_stream(
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 2, 3]}},
        Point(),
    )
    assert calls[0] == 1


def test_stream_19():
    calls = [0]
    coordinates = [0]

    class Point:
        def point(self, x, y, z):
            coordinates[0] += 1
            assert x == coordinates[0]
            coordinates[0] += 1
            assert y == coordinates[0]
            coordinates[0] += 1
            assert z == coordinates[0]
            calls[0] += 1
            return

    d3.geo_stream(
        {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [1, 2, 3]},
                }
            ],
        },
        Point(),
    )
    assert calls[0] == 1


def test_stream_20():
    calls = [0]
    coordinates = [0]

    class Point:
        def point(self, x, y, z):
            coordinates[0] += 1
            assert x == coordinates[0]
            coordinates[0] += 1
            assert y == coordinates[0]
            coordinates[0] += 1
            assert z == coordinates[0]
            calls[0] += 1
            return

    d3.geo_stream(
        {
            "type": "GeometryCollection",
            "geometries": [{"type": "Point", "coordinates": [1, 2, 3]}],
        },
        Point(),
    )
    assert calls[0] == 1
