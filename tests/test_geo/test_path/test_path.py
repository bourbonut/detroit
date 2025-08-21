import detroit as d3
import pytest
from math import e, pi, nan

def sround(x):
    decimals = abs(x - round(x))
    rx = round(x)
    sign = -1 if x < 0 else 1
    return int(x + sign * decimals) if decimals == 0.5 else rx

class ContextTest:
    def __init__(self):
        self._buffer = []

    def arc(self, x, y, r, *args):
        self._buffer.append({"type": "arc", "x": sround(x), "y": sround(y), "r": r})

    def move_to(self, x, y, *args):
        self._buffer.append({"type": "move_to", "x": sround(x), "y": sround(y)})

    def line_to(self, x, y, *args):
        self._buffer.append({"type": "line_to", "x": sround(x), "y": sround(y)})

    def close_path(self):
        self._buffer.append({"type": "close_path"})

    def result(self):
        result = self._buffer
        self._buffer = []
        return result

@pytest.fixture
def equirectangular():
    return (
        d3.geo_equirectangular()
        .scale(900 / pi)
        .set_precision(0)
    )

def path(projection, obj):
    context = ContextTest()
    (
        d3.geo_path()
        .set_projection(projection)
        .set_context(context)(obj)
    )
    return context.result()

def test_path_1():
    path = d3.geo_path()
    assert path.get_projection() is None

def test_path_2():
    path = d3.geo_path()
    assert path.get_context() is None

@pytest.mark.skip
def test_path_3():
    projection = d3.geo_albers()
    path = d3.geo_path(projection)
    assert path.get_projection() == projection

@pytest.mark.skip
def test_path_4():
    context = ContextTest()
    projection = d3.geo_albers()
    path = d3.geo_path(projection, context)
    assert path.get_projection() == projection
    assert path.get_context() == context

def test_path_5(equirectangular):
    assert path(equirectangular, {
        "type": "Point",
        "coordinates": [-63, 18]
    }) == [
        {"type": "move_to", "x": 170, "y": 160},
        {"type": "arc", "x": 165, "y": 160, "r": 4.5}
    ]

def test_path_6(equirectangular):
    assert path(equirectangular, {
        "type": "MultiPoint",
        "coordinates": [[-63, 18], [-62, 18], [-62, 17]]
    }) == [
        {"type": "move_to", "x": 170, "y": 160}, {"type": "arc", "x": 165, "y": 160, "r": 4.5},
        {"type": "move_to", "x": 175, "y": 160}, {"type": "arc", "x": 170, "y": 160, "r": 4.5},
        {"type": "move_to", "x": 175, "y": 165}, {"type": "arc", "x": 170, "y": 165, "r": 4.5}
    ]

def test_path_7(equirectangular):
    assert path(equirectangular, {
        "type": "LineString",
        "coordinates": [[-63, 18], [-62, 18], [-62, 17]]
    }) == [
        {"type": "move_to", "x": 165, "y": 160},
        {"type": "line_to", "x": 170, "y": 160},
        {"type": "line_to", "x": 170, "y": 165}
    ]

def test_path_8(equirectangular):
    assert path(equirectangular, {
        "type": "Polygon",
        "coordinates": [[[-63, 18], [-62, 18], [-62, 17], [-63, 18]]]
    }) == [
        {"type": "move_to", "x": 165, "y": 160},
        {"type": "line_to", "x": 170, "y": 160},
        {"type": "line_to", "x": 170, "y": 165},
        {"type": "close_path"}
    ]

def test_path_9(equirectangular):
    assert path(equirectangular, {
        "type": "GeometryCollection",
        "geometries": [{
            "type": "Polygon",
            "coordinates": [[[-63, 18], [-62, 18], [-62, 17], [-63, 18]]]
        }]
    }) == [
        {"type": "move_to", "x": 165, "y": 160},
        {"type": "line_to", "x": 170, "y": 160},
        {"type": "line_to", "x": 170, "y": 165},
        {"type": "close_path"}
    ]

def test_path_10(equirectangular):
    assert path(equirectangular, {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[-63, 18], [-62, 18], [-62, 17], [-63, 18]]]
        }
    }) == [
        {"type": "move_to", "x": 165, "y": 160},
        {"type": "line_to", "x": 170, "y": 160},
        {"type": "line_to", "x": 170, "y": 165},
        {"type": "close_path"}
    ]

def test_path_11(equirectangular):
    assert path(equirectangular, {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
             "coordinates": [[[-63, 18], [-62, 18], [-62, 17], [-63, 18]]]
            }
        }]
    }) == [
        {"type": "move_to", "x": 165, "y": 160},
        {"type": "line_to", "x": 170, "y": 160},
        {"type": "line_to", "x": 170, "y": 165},
        {"type": "close_path"}
    ]

def test_path_12(equirectangular):
    assert path(equirectangular, {
        "type": "Point",
        "coordinates": [180 + 1e-6, 0]
    }) == [
        {"type": "move_to", "x": -415, "y": 250},
        {"type": "arc", "x": -420, "y": 250, "r": 4.5}
    ]

def test_path_13(equirectangular):
    assert path(equirectangular, {
        "type": "Polygon",
        "coordinates": [[
            [-0.06904102953339501, 0.346043661846373],
            [-6.725674252975136e-15, 0.3981303360336475],
            [-6.742247658534323e-15, -0.08812465346531581],
         [-0.17301258217724075, -0.12278150669440671],
            [-0.06904102953339501, 0.346043661846373]
        ]]
    }) == [
        {"type": "move_to", "x": 480, "y": 248},
        {"type": "line_to", "x": 480, "y": 248},
        {"type": "line_to", "x": 480, "y": 250},
        {"type": "line_to", "x": 479, "y": 251},
        {"type": "close_path"}
    ]

def test_path_14(equirectangular):
    assert path(None, {
        "type": "Polygon",
        "coordinates": [[[-63, 18], [-62, 18], [-62, 17], [-63, 18]]]
    }) == [
        {"type": "move_to", "x": -63, "y": 18},
        {"type": "line_to", "x": -62, "y": 18},
        {"type": "line_to", "x": -62, "y": 17},
        {"type": "close_path"}
    ]

def test_path_15():
    path = d3.geo_path()
    assert path(None) is None

def test_path_16():
    path = d3.geo_path()
    assert path({"type": "Unknown"}) is None
    assert path({"type": "__proto__"}) is None

def test_path_17(equirectangular):
    context = ContextTest()
    path = d3.geo_path().set_projection(equirectangular).set_context(context)
    path({
        "type": "LineString",
        "coordinates": [[-63, 18], [-62, 18], [-62, 17]]
    })
    assert context.result(), [
        {"type": "move_to", "x": 165, "y": 160},
        {"type": "line_to", "x": 170, "y": 160},
        {"type": "line_to", "x": 170, "y": 165}
    ]
    path({
        "type": "Point",
        "coordinates": [-63, 18]
    })
    assert context.result(), [
        {"type": "move_to", "x": 170, "y": 160},
        {"type": "arc", "x": 165, "y": 160, "r": 4.5}
    ]

def test_path_18():
    path = d3.geo_path()
    assert path.get_digits() == 3

def test_path_19():
    path = d3.geo_path()
    assert path.set_digits(4) == path
    assert path.get_digits() == 4
    assert path.set_digits(0).get_digits() == 0
    assert d3.geo_path().get_digits() == 3

def test_path_20():
    path = d3.geo_path()
    assert path.set_digits(None).get_digits() is None

def test_path_21():
    path = d3.geo_path()
    assert path.set_digits(3.5).get_digits() == 3
    assert path.set_digits(3.9).get_digits() == 3
    assert path.set_digits("3").get_digits() == 3
    assert path.set_digits(" 3").get_digits() == 3
    assert path.set_digits("").get_digits() == 0

def test_path_22():
    path = d3.geo_path()
    with pytest.raises(ValueError):
        path.set_digits(nan)
    with pytest.raises(ValueError):
        path.set_digits(-1)
    with pytest.raises(ValueError):
        path.set_digits(-0.1)

def test_path_23():
    line = {"type": "LineString", "coordinates": [[pi, e], [e, pi]]}
    assert d3.geo_path().set_digits(0)(line) == "M3,3L3,3"
    assert d3.geo_path().set_digits(1)(line) == "M3.1,2.7L2.7,3.1"
    assert d3.geo_path().set_digits(2)(line) == "M3.14,2.72L2.72,3.14"
    assert d3.geo_path().set_digits(3)(line) == "M3.142,2.718L2.718,3.142"
    assert d3.geo_path().set_digits(4)(line) == "M3.1416,2.7183L2.7183,3.1416"
    assert d3.geo_path().set_digits(5)(line) == "M3.14159,2.71828L2.71828,3.14159"
    assert d3.geo_path().set_digits(6)(line) == "M3.141593,2.718282L2.718282,3.141593"
    assert d3.geo_path().set_digits(40)(line) == "M3.141592653589793,2.718281828459045L2.718281828459045,3.141592653589793"
    assert d3.geo_path().set_digits(None)(line) == "M3.141592653589793,2.718281828459045L2.718281828459045,3.141592653589793"

def test_path_24():
    p1 = d3.geo_path().set_digits(1)
    p2 = d3.geo_path().set_digits(2)
    point = {"type": "Point", "coordinates": [pi, e]}
    assert p1.set_point_radius(1)(point) == "M3.1,2.7m0,1a1,1 0 1,1 0,-2a1,1 0 1,1 0,2z"
    assert p1(point) == "M3.1,2.7m0,1a1,1 0 1,1 0,-2a1,1 0 1,1 0,2z"
    assert p1.set_point_radius(2)(point) == "M3.1,2.7m0,2a2,2 0 1,1 0,-4a2,2 0 1,1 0,4z"
    assert p1(point) == "M3.1,2.7m0,2a2,2 0 1,1 0,-4a2,2 0 1,1 0,4z"
    assert p2.set_point_radius(1)(point) == "M3.14,2.72m0,1a1,1 0 1,1 0,-2a1,1 0 1,1 0,2z"
    assert p2(point) == "M3.14,2.72m0,1a1,1 0 1,1 0,-2a1,1 0 1,1 0,2z"
    assert p1(point) == "M3.1,2.7m0,2a2,2 0 1,1 0,-4a2,2 0 1,1 0,4z"
    assert p2.set_point_radius(2)(point) == "M3.14,2.72m0,2a2,2 0 1,1 0,-4a2,2 0 1,1 0,4z"
    assert p2(point) == "M3.14,2.72m0,2a2,2 0 1,1 0,-4a2,2 0 1,1 0,4z"
    assert p1(point) == "M3.1,2.7m0,2a2,2 0 1,1 0,-4a2,2 0 1,1 0,4z"
