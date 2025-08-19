import detroit as d3

def test_measure_1():
    d3.geo_path().measure({
        "type": "Point",
        "coordinates": [0, 0]
    }) == 0

def test_measure_2():
    d3.geo_path().measure({
        "type": "MultiPoint",
        "coordinates": [[0, 0], [0, 1], [1, 1], [1, 0]]
    }) == 0

def test_measure_3():
    d3.geo_path().measure({
        "type": "LineString",
        "coordinates": [[0, 0], [0, 1], [1, 1], [1, 0]]
    }) == 3

def test_measure_4():
    d3.geo_path().measure({
        "type": "MultiLineString",
        "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0]]]
    }) == 3

def test_measure_5():
    d3.geo_path().measure({
        "type": "Polygon",
        "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]
    }) == 4

def test_measure_6():
    d3.geo_path().measure({
        "type": "Polygon",
        "coordinates": [[[-1, -1], [-1, 2], [2, 2], [2, -1], [-1, -1]], [[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
    }) == 16

def test_measure_7():
    d3.geo_path().measure({
        "type": "MultiPolygon",
        "coordinates": [[[[-1, -1], [-1, 2], [2, 2], [2, -1], [-1, -1]]], [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]]
    }) == 16
