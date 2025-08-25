import detroit as d3

def test_contains_1():
    assert d3.geo_contains({"type": "Sphere"}, [0, 0]) is True

def test_contains_2():
    assert d3.geo_contains({"type": "Point", "coordinates": [0, 0]}, [0, 0]) is True
    assert d3.geo_contains({"type": "Point", "coordinates": [1, 2]}, [1, 2]) is True
    assert d3.geo_contains({"type": "Point", "coordinates": [0, 0]}, [0, 1]) is False
    assert d3.geo_contains({"type": "Point", "coordinates": [1, 1]}, [1, 0]) is False

def test_contains_3():
    assert d3.geo_contains({"type": "MultiPoint", "coordinates": [[0, 0], [1,2]]}, [0, 0]) is True
    assert d3.geo_contains({"type": "MultiPoint", "coordinates": [[0, 0], [1,2]]}, [1, 2]) is True
    assert d3.geo_contains({"type": "MultiPoint", "coordinates": [[0, 0], [1,2]]}, [1, 3]) is False

def test_contains_4():
    assert d3.geo_contains({"type": "LineString", "coordinates": [[0, 0], [1,2]]}, [0, 0]) is True
    assert d3.geo_contains({"type": "LineString", "coordinates": [[0, 0], [1,2]]}, [1, 2]) is True
    assert d3.geo_contains({"type": "LineString", "coordinates": [[0, 0], [1,2]]}, d3.geo_interpolate([0, 0], [1,2])(0.3)) is True
    assert d3.geo_contains({"type": "LineString", "coordinates": [[0, 0], [1,2]]}, d3.geo_interpolate([0, 0], [1,2])(1.3)) is False
    assert d3.geo_contains({"type": "LineString", "coordinates": [[0, 0], [1,2]]}, d3.geo_interpolate([0, 0], [1,2])(-0.3)) is False

def test_contains_5():
    points = [[0, 0], [1,2], [3, 4], [5, 6]]
    feature = {"type": "LineString", "coordinates": points}
    for point in points:
        assert d3.geo_contains(feature, point) is True

def test_contains_6():
    epsilon = 1e-6
    line = [[0, 0], [0, 10], [10, 10], [10, 0]]
    points = [[0, 5], [epsilon * 1, 5], [0, epsilon], [epsilon * 1, epsilon]]
    for point in points:
        assert(d3.geo_contains({"type":"LineString", "coordinates": line}, point))

def test_contains_7():
    epsilon = 1e-6
    line = [[0, 0], [0, 10], [10, 10], [10, 0]]
    points = [[epsilon * 10, 5], [epsilon * 10, epsilon]]
    for point in points:
        assert not(d3.geo_contains({"type":"LineString", "coordinates": line}, point))

def test_contains_8():
    assert d3.geo_contains({"type": "MultiLineString", "coordinates": [[[0, 0], [1,2]], [[2, 3], [4,5]]]}, [2, 3]) is True
    assert d3.geo_contains({"type": "MultiLineString", "coordinates": [[[0, 0], [1,2]], [[2, 3], [4,5]]]}, [5, 6]) is False

def test_contains_9():
    polygon = d3.geo_circle().set_radius(60)()
    assert d3.geo_contains(polygon, [1, 1]) is True
    assert d3.geo_contains(polygon, [-180, 0]) is False

def test_contains_10():
    outer = d3.geo_circle().set_radius(60)()["coordinates"][0]
    inner = d3.geo_circle().set_radius(3)()["coordinates"][0]
    polygon = {"type":"Polygon", "coordinates": [outer, inner]}
    assert d3.geo_contains(polygon, [1, 1]) is False
    assert d3.geo_contains(polygon, [5, 0]) is True
    assert d3.geo_contains(polygon, [65, 0]) is False

def test_contains_11():
    p1 = d3.geo_circle().set_radius(6)()["coordinates"]
    p2 = d3.geo_circle().set_radius(6).set_center([90,0])()["coordinates"]
    polygon = {"type":"MultiPolygon", "coordinates": [p1, p2]}
    assert d3.geo_contains(polygon, [1, 0]) is True
    assert d3.geo_contains(polygon, [90, 1]) is True
    assert d3.geo_contains(polygon, [90, 45]) is False

def test_contains_12():
    collection = {
        "type": "GeometryCollection", "geometries": [
            {"type": "GeometryCollection", "geometries": [{"type": "LineString", "coordinates": [[-45, 0], [0, 0]]}]},
            {"type": "LineString", "coordinates": [[0, 0], [45, 0]]}
        ]
    }
    assert d3.geo_contains(collection, [-45, 0]) is True
    assert d3.geo_contains(collection, [45, 0]) is True
    assert d3.geo_contains(collection, [12, 25]) is False

def test_contains_13():
    feature = {
        "type": "Feature", "geometry": {
            "type": "LineString", "coordinates": [[0, 0], [45, 0]]
        }
    }
    assert d3.geo_contains(feature, [45, 0]) is True
    assert d3.geo_contains(feature, [12, 25]) is False

def test_contains_14():
    feature1 = {
        "type": "Feature", "geometry": {
            "type": "LineString", "coordinates": [[0, 0], [45, 0]]
        }
    }
    feature2 = {
        "type": "Feature", "geometry": {
            "type": "LineString", "coordinates": [[-45, 0], [0, 0]]
        }
    }
    feature_collection = {
        "type": "FeatureCollection",
        "features": [ feature1, feature2 ]
    }
    assert d3.geo_contains(feature_collection, [45, 0]) is True
    assert d3.geo_contains(feature_collection, [-45, 0]) is True
    assert d3.geo_contains(feature_collection, [12, 25]) is False

def test_contains_15():
    assert d3.geo_contains(None, [0, 0]) is False
