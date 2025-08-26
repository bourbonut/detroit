import detroit as d3
from math import pi

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

def test_length_1():
  assert in_delta(d3.geo_length({"type": "Point", "coordinates": [0, 0]}), 0, 1e-6)

def test_length_2():
  assert in_delta(d3.geo_length({"type": "MultiPoint", "coordinates": [[0, 1], [2, 3]]}), 0, 1e-6)

def test_length_3():
  assert in_delta(d3.geo_length({"type": "LineString", "coordinates": [[-45, 0], [45, 0]]}), pi / 2, 1e-6)
  assert in_delta(d3.geo_length({"type": "LineString", "coordinates": [[-45, 0], [-30, 0], [-15, 0], [0, 0]]}), pi / 4, 1e-6)

def test_length_4():
  assert in_delta(d3.geo_length({"type": "MultiLineString", "coordinates": [[[-45, 0], [-30, 0]], [[-15, 0], [0, 0]]]}), pi / 6, 1e-6)

def test_length_5():
  assert in_delta(d3.geo_length({"type": "Polygon", "coordinates": [[[0, 0], [3, 0], [3, 3], [0, 3], [0, 0]]]}), 0.157008, 1e-6)

def test_length_6():
  assert in_delta(d3.geo_length({"type": "Polygon", "coordinates": [[[0, 0], [3, 0], [3, 3], [0, 3], [0, 0]], [[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]]]}), 0.209354, 1e-6)

def test_length_7():
  assert in_delta(d3.geo_length({"type": "MultiPolygon", "coordinates": [[[[0, 0], [3, 0], [3, 3], [0, 3], [0, 0]]]]}), 0.157008, 1e-6)
  assert in_delta(d3.geo_length({"type": "MultiPolygon", "coordinates": [[[[0, 0], [3, 0], [3, 3], [0, 3], [0, 0]]], [[[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]]]]}), 0.209354, 1e-6)

def test_length_8():
  assert in_delta(d3.geo_length({
    "type": "FeatureCollection", "features": [
      {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-45, 0], [0, 0]]}},
      {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[0, 0], [45, 0]]}}
    ]
  }), pi / 2, 1e-6)

def test_length_9():
  assert in_delta(d3.geo_length({
    "type": "GeometryCollection", "geometries": [
      {"type": "GeometryCollection", "geometries": [{"type": "LineString", "coordinates": [[-45, 0], [0, 0]]}]},
      {"type": "LineString", "coordinates": [[0, 0], [45, 0]]}
    ]
  }), pi / 2, 1e-6)
