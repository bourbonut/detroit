import json
from math import ceil, isnan
from pathlib import Path

import detroit as d3


def frange(start, stop, step):
    return [start + i * step for i in range(max(0, ceil((stop - start) / step)))]


def in_delta(actual, expected, delta=1e-6):
    if isinstance(expected, list):
        n = len(expected)
        if len(actual) != n:
            return False
        for i in range(n):
            if not in_delta(actual[i], expected[i], delta):
                return False
        return True
    else:
        return actual >= expected - delta and actual <= expected + delta


def test_centroid_1():
    assert in_delta(
        d3.geo_centroid({"type": "Point", "coordinates": [0, 0]}), [0, 0], 1e-6
    )
    assert in_delta(
        d3.geo_centroid({"type": "Point", "coordinates": [1, 1]}), [1, 1], 1e-6
    )
    assert in_delta(
        d3.geo_centroid({"type": "Point", "coordinates": [2, 3]}), [2, 3], 1e-6
    )
    assert in_delta(
        d3.geo_centroid({"type": "Point", "coordinates": [-4, -5]}), [-4, -5], 1e-6
    )


def test_centroid_2():
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "GeometryCollection",
                "geometries": [
                    {"type": "Point", "coordinates": [0, 0]},
                    {"type": "Point", "coordinates": [1, 2]},
                ],
            }
        ),
        [0.499847, 1.000038],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid({"type": "MultiPoint", "coordinates": [[0, 0], [1, 2]]}),
        [0.499847, 1.000038],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid({"type": "MultiPoint", "coordinates": [[179, 0], [-179, 0]]}),
        [180, 0],
        1e-6,
    )


def test_centroid_3():
    assert all(
        map(
            isnan,
            d3.geo_centroid({"type": "MultiPoint", "coordinates": [[0, 0], [180, 0]]}),
        )
    )
    assert all(
        map(
            isnan,
            d3.geo_centroid(
                {
                    "type": "MultiPoint",
                    "coordinates": [[0, 0], [90, 0], [180, 0], [-90, 0]],
                }
            ),
        )
    )
    assert all(
        map(
            isnan,
            d3.geo_centroid(
                {
                    "type": "MultiPoint",
                    "coordinates": [[0, 0], [0, 90], [180, 0], [0, -90]],
                }
            ),
        )
    )


def test_centroid_4():
    assert all(map(isnan, d3.geo_centroid({"type": "MultiPoint", "coordinates": []})))


def test_centroid_5():
    assert in_delta(
        d3.geo_centroid({"type": "LineString", "coordinates": [[0, 0], [1, 0]]}),
        [0.5, 0],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid({"type": "LineString", "coordinates": [[0, 0], [0, 90]]}),
        [0, 45],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid(
            {"type": "LineString", "coordinates": [[0, 0], [0, 45], [0, 90]]}
        ),
        [0, 45],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid({"type": "LineString", "coordinates": [[-1, -1], [1, 1]]}),
        [0, 0],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid({"type": "LineString", "coordinates": [[-60, -1], [60, 1]]}),
        [0, 0],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid({"type": "LineString", "coordinates": [[179, -1], [-179, 1]]}),
        [180, 0],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid(
            {"type": "LineString", "coordinates": [[-179, 0], [0, 0], [179, 0]]}
        ),
        [0, 0],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid(
            {"type": "LineString", "coordinates": [[-180, -90], [0, 0], [0, 90]]}
        ),
        [0, 0],
        1e-6,
    )


def test_centroid_6():
    assert all(
        map(
            isnan,
            d3.geo_centroid({"type": "LineString", "coordinates": [[180, 0], [0, 0]]}),
        )
    )
    assert all(
        map(
            isnan,
            d3.geo_centroid(
                {"type": "MultiLineString", "coordinates": [[[0, -90], [0, 90]]]}
            ),
        )
    )


def test_centroid_7():
    assert in_delta(
        d3.geo_centroid({"type": "MultiLineString", "coordinates": [[[0, 0], [0, 2]]]}),
        [0, 1],
        1e-6,
    )


def test_centroid_8():
    assert in_delta(
        d3.geo_centroid({"type": "LineString", "coordinates": [[1, 1], [1, 1]]}),
        [1, 1],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "GeometryCollection",
                "geometries": [
                    {"type": "Point", "coordinates": [0, 0]},
                    {"type": "LineString", "coordinates": [[1, 2], [1, 2]]},
                ],
            }
        ),
        [0.666534, 1.333408],
        1e-6,
    )


def test_centroid_9():
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "Polygon",
                "coordinates": [[[1, 1], [2, 1], [3, 1], [2, 1], [1, 1]]],
            }
        ),
        [2, 1.000076],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "GeometryCollection",
                "geometries": [
                    {"type": "Point", "coordinates": [0, 0]},
                    {
                        "type": "Polygon",
                        "coordinates": [[[1, 2], [1, 2], [1, 2], [1, 2]]],
                    },
                ],
            }
        ),
        [0.799907, 1.600077],
        1e-6,
    )


def test_centroid_10():
    assert in_delta(
        d3.geo_centroid(
            {"type": "Polygon", "coordinates": [[[1, 1], [1, 1], [1, 1], [1, 1]]]}
        ),
        [1, 1],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "GeometryCollection",
                "geometries": [
                    {"type": "Point", "coordinates": [0, 0]},
                    {
                        "type": "Polygon",
                        "coordinates": [[[1, 2], [1, 2], [1, 2], [1, 2]]],
                    },
                ],
            }
        ),
        [0.799907, 1.600077],
        1e-6,
    )


def test_centroid_11():
    assert all(
        map(
            isnan,
            d3.geo_centroid(
                {
                    "type": "LineString",
                    "coordinates": [[0, 0], [120, 0], [-120, 0], [0, 0]],
                }
            ),
        )
    )


def test_centroid_12():
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "Polygon",
                "coordinates": [[[0, -90], [0, 0], [0, 90], [1, 0], [0, -90]]],
            }
        ),
        [0.5, 0],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "Polygon",
                "coordinates": [[[x, -60] for x in frange(-180, 180 + 1 / 2, 1)]],
            }
        )[1],
        -90,
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "Polygon",
                "coordinates": [[[0, -10], [0, 10], [10, 10], [10, -10], [0, -10]]],
            }
        ),
        [5, 0],
        1e-6,
    )


def test_centroid_13():
    circle = d3.geo_circle()
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "MultiPolygon",
                "coordinates": [
                    circle.set_radius(45).set_center([90, 0])()["coordinates"],
                    circle.set_radius(60).set_center([-90, 0])()["coordinates"],
                ],
            }
        ),
        [-90, 0],
        1e-6,
    )


def test_centroid_14():
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "Polygon",
                "coordinates": [[[0, -90], [0, 0], [0, 90], [1, 0], [0, -90]]],
            }
        ),
        [0.5, 0],
        1e-6,
    )


def test_centroid_15():
    assert in_delta(
        d3.geo_centroid(d3.geo_circle().set_radius(5).set_center([30, 45])()),
        [30, 45],
        1e-6,
    )


def test_centroid_16():
    assert in_delta(
        d3.geo_centroid(d3.geo_circle().set_radius(135).set_center([30, 45])()),
        [30, 45],
        1e-6,
    )


def test_centroid_17():
    assert (
        d3.geo_centroid(
            {
                "type": "Polygon",
                "coordinates": [[[x, -60] for x in frange(-180, 180 + 1 / 2, 1)]],
            }
        )[1]
        == -90
    )


def test_centroid_18():
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "Polygon",
                "coordinates": [[[0, -10], [0, 10], [10, 10], [10, -10], [0, -10]]],
            }
        ),
        [5, 0],
        1e-6,
    )


def test_centroid_19():
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "Polygon",
                "coordinates": [
                    [[0, -10], [0, 10], [0, 10], [10, 10], [10, -10], [0, -10]]
                ],
            }
        ),
        [5, 0],
        1e-6,
    )


def test_centroid_20():
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "Polygon",
                "coordinates": [
                    [[-180, 0], [-180, 10], [-179, 10], [-179, 0], [-180, 0]]
                ],
            }
        ),
        [-179.5, 4.987448],
        1e-6,
    )


def test_centroid_21():
    circle = d3.geo_circle().set_center([0, 45])
    coordinates = circle.set_radius(60)()["coordinates"]
    coordinates.append(circle.set_radius(45)()["coordinates"][0][::-1])
    assert in_delta(
        d3.geo_centroid({"type": "Polygon", "coordinates": coordinates}), [0, 45], 1e-6
    )


def test_centroid_22():
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "Polygon",
                "coordinates": [[[0, -10], [0, 10], [10, 10], [10, -10], [0, -10]]],
            }
        ),
        [5, 0],
        1e-6,
    )


def test_centroid_23():
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "Polygon",
                "coordinates": [
                    [[-180, 0], [-180, 10], [-179, 10], [-179, 0], [-180, 0]]
                ],
            }
        ),
        [-179.5, 4.987448],
        1e-6,
    )


def test_centroid_24():
    circle = d3.geo_circle().set_center([0, 45])
    coordinates = circle.set_radius(60)()["coordinates"]
    coordinates.append(circle.set_radius(45)()["coordinates"][0][::-1])
    assert in_delta(
        d3.geo_centroid({"type": "Polygon", "coordinates": coordinates}), [0, 45], 1e-6
    )


def test_centroid_25():
    assert all(map(isnan, d3.geo_centroid({"type": "Sphere"})))


def test_centroid_26():
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": [[1, 1], [1, 1]]},
            }
        ),
        [1, 1],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid(
            {"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 1]}}
        ),
        [1, 1],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[0, -90], [0, 0], [0, 90], [1, 0], [0, -90]]],
                },
            }
        ),
        [0.5, 0],
        1e-6,
    )


def test_centroid_27():
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [[179, 0], [180, 0]],
                        },
                    },
                    {
                        "type": "Feature",
                        "geometry": {"type": "Point", "coordinates": [0, 0]},
                    },
                ],
            }
        ),
        [179.5, 0],
        1e-6,
    )


def test_centroid_28():
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "GeometryCollection",
                "geometries": [
                    {"type": "LineString", "coordinates": [[179, 0], [180, 0]]},
                    {"type": "Point", "coordinates": [0, 0]},
                ],
            }
        ),
        [179.5, 0],
        1e-6,
    )


def test_centroid_29():
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "GeometryCollection",
                "geometries": [
                    {
                        "type": "Polygon",
                        "coordinates": [
                            [[-180, 0], [-180, 1], [-179, 1], [-179, 0], [-180, 0]]
                        ],
                    },
                    {"type": "LineString", "coordinates": [[179, 0], [180, 0]]},
                    {"type": "Point", "coordinates": [0, 0]},
                ],
            }
        ),
        [-179.5, 0.500006],
        1e-6,
    )
    assert in_delta(
        d3.geo_centroid(
            {
                "type": "GeometryCollection",
                "geometries": [
                    {"type": "Point", "coordinates": [0, 0]},
                    {"type": "LineString", "coordinates": [[179, 0], [180, 0]]},
                    {
                        "type": "Polygon",
                        "coordinates": [
                            [[-180, 0], [-180, 1], [-179, 1], [-179, 0], [-180, 0]]
                        ],
                    },
                ],
            }
        ),
        [-179.5, 0.500006],
        1e-6,
    )


def test_centroid_30():
    assert d3.geo_centroid(
        {
            "type": "GeometryCollection",
            "geometries": [
                {"type": "Sphere"},
                {"type": "Point", "coordinates": [0, 0]},
            ],
        }
    ) == [0, 0]
    assert d3.geo_centroid(
        {
            "type": "GeometryCollection",
            "geometries": [
                {"type": "Point", "coordinates": [0, 0]},
                {"type": "Sphere"},
            ],
        }
    ) == [0, 0]


def test_centroid_31():
    filepath = Path(__file__).resolve().parent / "data" / "ny.json"
    with open(filepath) as file:
        ny = json.load(file)
    assert in_delta(d3.geo_centroid(ny), [-73.93079, 40.69447], 1e-5)
