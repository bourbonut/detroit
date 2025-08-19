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

def area(projection, obj):
    return (
        d3.geo_path()
        .set_projection(projection)
        .area(obj)
    )

def test_area_1(equirectangular):
    assert area(equirectangular, {
        "type": "Polygon",
        "coordinates": [[[100, 0], [100, 1], [101, 1], [101, 0], [100, 0]]]
    }) == 25

def test_area_2(equirectangular):
    assert area(equirectangular, {
        "type": "Polygon",
        "coordinates": [[[100, 0], [100, 1], [101, 1], [101, 0], [100, 0]], [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]]
    }) == 16

def test_area_3(equirectangular):
    assert area(equirectangular, {
        "type": "Sphere",
    }) == 1620000
