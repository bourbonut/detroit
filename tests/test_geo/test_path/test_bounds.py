import detroit as d3
import pytest
from math import pi

@pytest.fixture
def equirectangular():
    return (
        d3.geo_equirectangular()
        .set_scale(900 / pi)
        .set_precision(0)
    )

def bounds(projection, obj):
    return (
        d3.geo_path()
        .projection(projection)
        .bounds(obj)
    )

def test_bounds_1(equirectangular):
    assert bounds(equirectangular, {
        "type": "Polygon",
        "coordinates": [[[100, 0], [100, 1], [101, 1], [101, 0], [100, 0]]]
    }) == [[980, 245], [985, 250]]

def test_bounds_2(equirectangular):
    assert bounds(equirectangular, {
        "type": "Polygon",
        "coordinates": [[[100, 0], [100, 1], [101, 1], [101, 0], [100, 0]], [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]]
    }) == [[980, 245], [985, 250]]

def test_bounds_3(equirectangular):
    assert bounds(equirectangular, {
        "type": "Sphere"
    }) == [[-420, -200], [1380, 700]]
