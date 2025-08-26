import detroit as d3
from math import isnan

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

def test_bounds_1():
    assert d3.geo_bounds({
        "type": "Feature",
        "geometry": {
            "type": "MultiPoint",
            "coordinates": [[-123, 39], [-122, 38]]
        }
    }) == [[-123, 38], [-122, 39]]

def test_bounds_2():
    assert d3.geo_bounds({
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [-123, 39]
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [-122, 38]
                }
            }
        ]
    }) == [[-123, 38], [-122, 39]]

def test_bounds_3():
    assert d3.geo_bounds({
        "type": "GeometryCollection",
        "geometries": [
            {
                "type": "Point",
                "coordinates": [-123, 39]
            },
            {
                "type": "Point",
                "coordinates": [-122, 38]
            }
        ]
    }) == [[-123, 38], [-122, 39]]

def test_bounds_4():
    assert d3.geo_bounds({
        "type": "LineString",
        "coordinates": [[-123, 39], [-122, 38]]
    }) == [[-123, 38], [-122, 39]]

def test_bounds_5():
    assert d3.geo_bounds({
        "type": "LineString",
        "coordinates": [[-30, -20], [130, 40]]
    }) == d3.geo_bounds({
        "type": "LineString",
        "coordinates": [[-30, -20], [130, 40]][::-1]
    })

def test_bounds_6():
    assert d3.geo_bounds({
        "type": "LineString",
        "coordinates": [[-123, 39], [-122, 38], [-122, 38]]
    }) == [[-123, 38], [-122, 39]]

def test_bounds_7():
    assert d3.geo_bounds({
        "type": "LineString",
        "coordinates": [[0, 0], [0, 1], [0, 60]]
    }) == [[0, 0], [0, 60]]

def test_bounds_8():
    assert d3.geo_bounds({
        "type": "LineString",
        "coordinates": [[0, 0], [1, 0], [60, 0]]
    }) == [[0, 0], [60, 0]]

def test_bounds_9():
    assert in_delta(d3.geo_bounds({
        "type": "LineString",
        "coordinates": [[-45, 60], [45, 60]]
    }), [[-45, 60], [45, 67.792345]], 1e-6)

def test_bounds_10():
    assert in_delta(d3.geo_bounds({
        "type": "LineString",
        "coordinates": [[-45, -60], [45, -60]]
    }), [[-45, -67.792345], [45, -60]], 1e-6)

def test_bounds_11():
    assert d3.geo_bounds({
        "type": "MultiLineString",
        "coordinates": [[[-123, 39], [-122, 38]]]
    }) == [[-123, 38], [-122, 39]]

def test_bounds_12():
    assert d3.geo_bounds({
        "type": "MultiPoint",
        "coordinates": [[-123, 39], [-122, 38]]
    }) == [[-123, 38], [-122, 39]]

def test_bounds_13():
    assert d3.geo_bounds({
        "type": "MultiPoint",
        "coordinates": [[-179, 39], [179, 38]]
    }) == [[179, 38], [-179, 39]]

def test_bounds_14():
    assert d3.geo_bounds({
        "type": "MultiPoint",
        "coordinates": [[-179, 39], [179, 38], [-1, 0], [1, 0]]
    }) == [[-1, 0], [-179, 39]]

def test_bounds_15():
    assert d3.geo_bounds({
        "type": "MultiPoint",
        "coordinates": [[-1, 0], [1, 0], [-179, 39], [179, 38]]
    }) == [[-1, 0], [-179, 39]]

def test_bounds_16():
    assert d3.geo_bounds({
        "type": "MultiPoint",
        "coordinates": [[-1, 0], [-179, 39], [1, 0], [179, 38]]
    }) == [[-1, 0], [-179, 39]]

def test_bounds_17():
    assert d3.geo_bounds({
        "type": "MultiPoint",
        "coordinates": [[178, 38], [179, 39], [-179, 37]]
    }) == [[178, 37], [-179, 39]]

def test_bounds_18():
    assert d3.geo_bounds({
        "type": "MultiPoint",
        "coordinates": [[-179, 39], [-179, 38], [178, 39], [-178, 38]]
    }) == [[178, 38], [-178, 39]]

def test_bounds_19():
    assert in_delta(d3.geo_bounds({
        "type": "MultiPolygon",
        "coordinates": [
            [[[-123, 39], [-122, 39], [-122, 38], [-123, 39]],
            [[10, 20], [20, 20], [20, 10], [10, 10], [10, 20]]]
        ]
    }), [[-123, 10], [20, 39.001067]], 1e-6)

def test_bounds_20():
    assert d3.geo_bounds({
        "type": "Point",
        "coordinates": [-123, 39]
    }) == [[-123, 39], [-123, 39]]

def test_bounds_21():
    assert in_delta(d3.geo_bounds({
        "type": "Polygon",
        "coordinates": [[[-123, 39], [-122, 39], [-122, 38], [-123, 39]]]
    }), [[-123, 38], [-122, 39.001067]], 1e-6)

def test_bounds_22():
    assert d3.geo_bounds({
        "type": "Polygon",
        "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]]
    }) == [[-180, -90], [180, 90]]

def test_bounds_23():
    assert in_delta(d3.geo_bounds({
        "type": "Polygon",
        "coordinates": [[[-170, 80], [0, 80], [170, 80], [170, -80], [0, -80], [-170, -80], [-170, 80]]]
    }), [[-170, -89.119552], [170, 89.119552]], 1e-6)

def test_bounds_24():
    assert in_delta(d3.geo_bounds({
        "type": "Polygon",
        "coordinates": [[[10, 80], [170, 80], [-170, 80], [-10, 80], [10, 80]]]
    }), [[-180, -90], [180, 88.246216]], 1e-6)

def test_bounds_25():
    assert in_delta(d3.geo_bounds({
        "type": "Polygon",
        "coordinates": [[[10, 80], [170, 80], [-170, 80], [-10, 80], [-10, 0], [-10, -80], [-170, -80], [170, -80], [10, -80], [10, 0], [10, 80]]]
    }), [[10, -88.246216], [-10, 88.246216]], 1e-6)

def test_bounds_26():
    assert d3.geo_bounds({
        "type": "Polygon",
        "coordinates": [[[-60, -80], [60, -80], [180, -80], [-60, -80]]]
    }) == [[-180, -90], [180, -80]]

def test_bounds_27():
    assert in_delta(d3.geo_bounds({
        "type": "Polygon",
        "coordinates": [
            [[-60, -80], [60, -80], [180, -80], [-60, -80]],
            [[-60, -89], [180, -89], [60, -89], [-60, -89]]
        ]
    }), [[-180, -89.499961], [180, -80]], 1e-6)

def test_bounds_28():
    assert d3.geo_bounds({
        "type": "Sphere"
    }) == [[-180, -90], [180, 90]]

def test_bounds_29():
    assert d3.geo_bounds({
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "GeometryCollection",
                    "geometries": [
                        {
                            "type": "Point",
                            "coordinates": [-120,47]
                        },
                        {
                            "type": "Point",
                            "coordinates": [-119,46]
                        }
                    ]
                }
            }
        ]
    }) == [[-120,46], [-119,47]]

def test_bounds_30():
    b = d3.geo_bounds({"type": "Feature", "geometry": None})
    assert isnan(b[0][0])
    assert isnan(b[0][1])
    assert isnan(b[1][0])
    assert isnan(b[1][1])

def test_bounds_31():
    b = d3.geo_bounds({"type": "MultiPoint", "coordinates": []})
    assert isnan(b[0][0])
    assert isnan(b[0][1])
    assert isnan(b[1][0])
    assert isnan(b[1][1])

def test_bounds_32():
    b = d3.geo_bounds({"type": "MultiLineString", "coordinates": []})
    assert isnan(b[0][0])
    assert isnan(b[0][1])
    assert isnan(b[1][0])
    assert isnan(b[1][1])

def test_bounds_33():
    b = d3.geo_bounds({"type": "MultiPolygon", "coordinates": []})
    assert isnan(b[0][0])
    assert isnan(b[0][1])
    assert isnan(b[1][0])
    assert isnan(b[1][1])
