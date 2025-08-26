import detroit as d3
import pytest
from math import pi, isnan

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

@pytest.fixture
def equirectangular():
    return (
        d3.geo_equirectangular()
        .scale(900 / pi)
        .set_precision(0)
    )

def centroid(projection, obj):
    return (
        d3.geo_path()
        .set_projection(projection)
        .centroid(obj)
    )

def test_centroid_1(equirectangular):
    assert centroid(equirectangular, {"type": "Point", "coordinates": [0, 0]}) == [480, 250]

def test_centroid_2(equirectangular):
    assert all(map(isnan, centroid(equirectangular, {"type": "MultiPoint", "coordinates": []})))

def test_centroid_3(equirectangular):
    assert centroid(equirectangular, {"type": "MultiPoint", "coordinates": [[0, 0]]}) == [480, 250]

def test_centroid_4(equirectangular):
    assert centroid(equirectangular, {"type": "MultiPoint", "coordinates": [[-122, 37], [-74, 40]]}) == [-10, 57.5]

def test_centroid_5(equirectangular):
    assert all(map(isnan, centroid(equirectangular, {"type": "LineString", "coordinates": []})))

def test_centroid_6(equirectangular):
    assert centroid(equirectangular, {"type": "LineString", "coordinates": [[100, 0], [0, 0]]}) == [730, 250]
    assert centroid(equirectangular, {"type": "LineString", "coordinates": [[0, 0], [100, 0], [101, 0]]}) == [732.5, 250]

def test_centroid_7(equirectangular):
    assert centroid(equirectangular, {"type": "LineString", "coordinates": [[-122, 37], [-122, 37]]}) == [-130, 65]
    assert centroid(equirectangular, {"type": "LineString", "coordinates": [[-74, 40], [-74, 40]]}) == [110, 50]

def test_centroid_8(equirectangular):
    assert centroid(equirectangular, {"type": "LineString", "coordinates": [[-122, 37], [-74, 40], [-74, 40]]}) == [-10, 57.5]

def test_centroid_9(equirectangular):
    assert in_delta(centroid(equirectangular, {"type": "LineString", "coordinates": [[-122, 37], [-74, 40], [-100, 0]]}), [17.389135, 103.563545], 1e-6)

def test_centroid_10(equirectangular):
    assert centroid(equirectangular, {"type": "MultiLineString", "coordinates": [[[100, 0], [0, 0]], [[-10, 0], [0, 0]]]}) == [705, 250]

def test_centroid_11(equirectangular):
    assert centroid(equirectangular, {"type": "Polygon", "coordinates": [[[100, 0], [100, 1], [101, 1], [101, 0], [100, 0]]]}) == [982.5, 247.5]

def test_centroid_12(equirectangular):
    assert centroid(equirectangular, {"type": "Polygon", "coordinates": [[[1, 0], [2, 0], [3, 0], [1, 0]]]}) == [490, 250]

def test_centroid_13(equirectangular):
    assert centroid(equirectangular, {"type": "Polygon", "coordinates": [
        [[100,     0], [100,     1], [101,     1], [101,     0], [100, 0]],
        [[100.1, 0], [100.2, 0], [100.3, 0], [100.1, 0]
    ]]}) == [982.5, 247.5]

def test_centroid_14(equirectangular):
    assert in_delta(centroid(equirectangular, {
        "type": "Polygon",
        "coordinates": [
            [[-2, -2], [2, -2], [2, 2], [-2, 2], [-2, -2]][::-1],
            [[ 0, -1], [1, -1], [1, 1], [ 0, 1], [ 0, -1]]
        ]
    }), [479.642857, 250], 1e-6)

def test_centroid_15(equirectangular):
    assert all(map(isnan, centroid(equirectangular, {"type": "MultiPolygon", "coordinates": []})))

def test_centroid_16(equirectangular):
    assert centroid(equirectangular, {"type": "MultiPolygon", "coordinates": [[[[100, 0], [100, 1], [101, 1], [101, 0], [100, 0]]]]}) == [982.5, 247.5]

def test_centroid_17(equirectangular):
    assert centroid(equirectangular, {"type": "MultiPolygon", "coordinates": [
        [[[100, 0], [100, 1], [101, 1], [101, 0], [100, 0]]],
        [[[0, 0], [1, 0], [1, -1], [0, -1], [0, 0]]]
    ]}) == [732.5, 250]

def test_centroid_18(equirectangular):
    assert centroid(equirectangular, {"type": "MultiPolygon", "coordinates": [
        [[[100, 0], [100, 1], [101, 1], [101, 0], [100, 0]]],
        [[[0, 0], [1, 0], [2, 0], [0, 0]]]
    ]}) == [982.5, 247.5]

def test_centroid_19(equirectangular):
    assert centroid(equirectangular, {"type": "GeometryCollection", "geometries": [{"type": "Point", "coordinates": [0, 0]}]}) == [480, 250]

def test_centroid_20(equirectangular):
    assert centroid(equirectangular, {"type": "GeometryCollection", "geometries": [
        {"type": "LineString", "coordinates": [[179, 0], [180, 0]]},
        {"type": "Point", "coordinates": [0, 0]}
    ]}) == [1377.5, 250]

def test_centroid_21(equirectangular):
    assert centroid(equirectangular, {"type": "GeometryCollection", "geometries": [
        {"type": "Polygon", "coordinates": [[[-180, 0], [-180, 1], [-179, 1], [-179, 0], [-180, 0]]]},
        {"type": "LineString", "coordinates": [[179, 0], [180, 0]]},
        {"type": "Point", "coordinates": [0, 0]}
    ]}) == [-417.5, 247.5]

def test_centroid_22(equirectangular):
    assert centroid(equirectangular, {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [0, 0]}}]}) == [480, 250]

def test_centroid_23(equirectangular):
    assert centroid(equirectangular, {"type": "FeatureCollection", "features": [
        {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[179, 0], [180, 0]]}},
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [0, 0]}}
    ]}) == [1377.5, 250]

def test_centroid_24(equirectangular):
    assert centroid(equirectangular, {"type": "FeatureCollection", "features": [
        {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-180, 0], [-180, 1], [-179, 1], [-179, 0], [-180, 0]]]}},
        {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[179, 0], [180, 0]]}},
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [0, 0]}}
    ]}) == [-417.5, 247.5]

def test_centroid_25(equirectangular):
    assert centroid(equirectangular, {"type": "Sphere"}) == [480, 250]
