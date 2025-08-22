import detroit as d3
import json
from math import isnan, pi
from pytopojson.feature import Feature
from pathlib import Path
import pytest

def in_delta(actual, expected, delta=1e6):
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

@pytest.fixture(scope="session")
def us():
    filepath = Path(__file__).resolve().parents[1] / "data" / "us-10m.json"
    with open(filepath) as file:
        us_topo = json.load(file)
    return Feature()(us_topo, us_topo["objects"]["land"])

@pytest.fixture(scope="session")
def world():
    filepath = Path(__file__).resolve().parents[1] / "data" / "world-50m.json"
    with open(filepath) as file:
        world_topo = json.load(file)
    return Feature()(world_topo, world_topo["objects"]["land"])

def test_fit_1():
    projection = d3.geo_equirectangular()
    projection.fit_extent([[50, 50], [950, 950]], {"type": "Sphere"})
    assert in_delta(projection.get_scale(), 900 / (2 * pi), 1e-6)
    assert in_delta(projection.get_translation(), [500, 500], 1e-6)

def test_fit_2(world):
    projection = d3.geo_equirectangular()
    projection.fit_extent([[50, 50], [950, 950]], world)
    assert in_delta(projection.get_scale(), 143.239449, 1e-6)
    assert in_delta(projection.get_translation(), [500, 492.000762], 1e-6)

@pytest.mark.skip
def test_fit_3(world):
    projection = d3.geo_azimuthal_equal_area()
    projection.fit_extent([[50, 50], [950, 950]], world)
    assert in_delta(projection.get_scale(), 228.357229, 1e-6)
    assert in_delta(projection.get_translation(), [496.353618, 479.684353], 1e-6)

@pytest.mark.skip
def test_fit_4(world):
    projection = d3.geo_azimuthal_equidistant()
    projection.fit_extent([[50, 50], [950, 950]], world)
    assert in_delta(projection.get_scale(), 153.559317, 1e-6)
    assert in_delta(projection.get_translation(), [485.272493, 452.093375], 1e-6)

@pytest.mark.skip
def test_fit_5(world):
    projection = d3.geo_conic_conformal().clip_angle(30).parallels([30, 60]).rotate([0, -45])
    projection.fit_extent([[50, 50], [950, 950]], world)
    assert in_delta(projection.get_scale(), 625.567161, 1e-6)
    assert in_delta(projection.get_translation(), [444.206209, 409.910893], 1e-6)

@pytest.mark.skip
def test_fit_6(world):
    projection = d3.geo_conic_equal_area()
    projection.fit_extent([[50, 50], [950, 950]], world)
    assert in_delta(projection.get_scale(), 145.862346, 1e-6)
    assert in_delta(projection.get_translation(), [500, 498.0114265], 1e-6)

@pytest.mark.skip
def test_fit_7(world):
    projection = d3.geo_conic_equidistant()
    projection.fit_extent([[50, 50], [950, 950]], world)
    assert in_delta(projection.get_scale(), 123.085587, 1e-6)
    assert in_delta(projection.get_translation(), [500, 498.598401], 1e-6)

def test_fit_8(world):
    projection = d3.geo_equirectangular()
    projection.fit_size([900, 900], world)
    assert in_delta(projection.get_scale(), 143.239449, 1e-6)
    assert in_delta(projection.get_translation(), [450, 442.000762], 1e-6)

@pytest.mark.skip
def test_fit_9(world):
    projection = d3.geo_gnomonic().clip_angle(45)
    projection.fit_extent([[50, 50], [950, 950]], world)
    assert in_delta(projection.get_scale(), 450.348233, 1e-6)
    assert in_delta(projection.get_translation(), [500.115138, 556.551304], 1e-6)

@pytest.mark.skip
def test_fit_10(world):
    projection = d3.geo_mercator()
    projection.fit_extent([[50, 50], [950, 950]], world)
    assert in_delta(projection.get_scale(), 143.239449, 1e-6)
    assert in_delta(projection.get_translation(), [500, 481.549457], 1e-6)

@pytest.mark.skip
def test_fit_11(world):
    projection = d3.geo_orthographic()
    projection.fit_extent([[50, 50], [950, 950]], world)
    assert in_delta(projection.get_scale(), 451.406773, 1e-6)
    assert in_delta(projection.get_translation(), [503.769179, 498.593227], 1e-6)

@pytest.mark.skip
def test_fit_12(world):
    projection = d3.geo_orthographic()
    projection.fit_size([900, 900], world)
    assert in_delta(projection.get_scale(), 451.406773, 1e-6)
    assert in_delta(projection.get_translation(), [453.769179, 448.593227], 1e-6)

@pytest.mark.skip
def test_fit_13(world):
    projection = d3.geo_stereographic()
    projection.fit_extent([[50, 50], [950, 950]], world)
    assert in_delta(projection.get_scale(), 162.934379, 1e-6)
    assert in_delta(projection.get_translation(), [478.546293, 432.922534], 1e-6)

@pytest.mark.skip
def test_fit_14(world):
    projection = d3.geo_transverse_mercator()
    projection.fit_extent([[50, 50], [950, 950]], world)
    assert in_delta(projection.get_scale(), 143.239449, 1e-6)
    assert in_delta(projection.get_translation(), [473.829551, 500], 1e-6)

@pytest.mark.skip
def test_fit_15(world):
    projection = d3.geo_albers_usa()
    projection.fit_extent([[50, 50], [950, 950]], us)
    assert in_delta(projection.get_scale(), 1152.889035, 1e-6)
    assert in_delta(projection.get_translation(), [533.52541, 496.232028], 1e-6)

def test_fit_16():
    projection = d3.geo_equirectangular()
    projection.fit_extent([[50, 50], [950, 950]], {"type": "Feature", "geometry": None})
    s = projection.get_scale()
    t = projection.get_translation()
    assert not s
    assert isnan(t[0])
    assert isnan(t[1])

def test_fit_17():
    projection = d3.geo_equirectangular()
    projection.fit_extent([[50, 50], [950, 950]], {"type": "MultiPoint", "coordinates": []})
    s = projection.get_scale()
    t = projection.get_translation()
    assert not s
    assert isnan(t[0])
    assert isnan(t[1])

def test_fit_18():
    projection = d3.geo_equirectangular()
    projection.fit_extent([[50, 50], [950, 950]], {"type": "MultiLineString", "coordinates": []})
    s = projection.get_scale()
    t = projection.get_translation()
    assert not s
    assert isnan(t[0])
    assert isnan(t[1])

def test_fit_19():
    projection = d3.geo_equirectangular()
    projection.fit_extent([[50, 50], [950, 950]], {"type": "MultiPolygon", "coordinates": []})
    s = projection.get_scale()
    t = projection.get_translation()
    assert not s
    assert isnan(t[0])
    assert isnan(t[1])

@pytest.mark.skip
def test_fit_20(world):
    projection = d3.geo_conic_equidistant()
    projection.fit_extent([[50, 50], [950, 950]], world)
    assert in_delta(projection.get_scale(), 128.903525, 1e-6)
    assert in_delta(projection.get_translation(), [500, 450.414357], 1e-6)

def test_fit_21(world):
    p1 = d3.geo_equirectangular().fit_size([1000, 1000], world)
    s1 = p1.get_scale()
    t1 = p1.get_translation()
    c1 = p1.get_clip_extent()
    p2 = d3.geo_equirectangular().set_clip_extent([[100, 200], [700, 600]]).fit_size([1000, 1000], world)
    s2 = p2.get_scale()
    t2 = p2.get_translation()
    c2 = p2.get_clip_extent()
    assert in_delta(s1, s2, 1e-6)
    assert in_delta(t1, t2, 1e-6)
    assert c1 is None
    assert c2 == [[100, 200], [700, 600]]

@pytest.mark.skip
def test_fit_22(world):
    projection = d3.geo_transverse_mercator().fit_extent([[50, 50], [950, 950]], world).scale(500)
    assert projection.get_scale() == 500
    assert in_delta(projection.get_translation(), [473.829551, 500], 1e-6)

@pytest.mark.skip
def test_fit_23(world):
    box = {"type": "Polygon", "coordinates": [[[-135, 45], [-45, 45], [-45, -45], [-135, -45], [-135, 45]]]}
    p1 = d3.geo_mercator().precision(0.1).fit_size([1000, 1000], box)
    p2 = d3.geo_mercator().precision(0).fit_size([1000, 1000], box)
    t1 = p1.get_translation()
    t2 = p2.get_translation()
    assert p1.precision() == 0.1
    assert p2.precision() == 0
    assert in_delta(p1.get_scale(), 436.218018, 1e-6)
    assert in_delta(p2.get_scale(), 567.296328, 1e-6)
    assert in_delta(t1[0], 1185.209661, 1e-6)
    assert in_delta(t2[0], 1391.106989, 1e-6)
    assert in_delta(t1[1], 500, 1e-6)
    assert in_delta(t1[1], t2[1], 1e-6)

def test_fit_24(world):
    projection = d3.geo_equirectangular()
    projection.fit_width(900, world)
    assert in_delta(projection.get_scale(), 143.239449, 1e-6)
    assert in_delta(projection.get_translation(), [450, 208.999023], 1e-6)

@pytest.mark.skip
def test_fit_25(world):
    projection = d3.geo_transverse_mercator()
    projection.fit_width(900, world)
    assert in_delta(projection.get_scale(), 166.239257, 1e-6)
    assert in_delta(projection.get_translation(), [419.627390, 522.256029], 1e-6)

@pytest.mark.skip
def test_fit_26(us):
    projection = d3.geo_albers_usa()
    projection.fit_width(900, us)
    assert in_delta(projection.get_scale(), 1152.889035, 1e-6)
    assert in_delta(projection.get_translation(), [483.52541, 257.736905], 1e-6)

def test_fit_27(world):
    projection = d3.geo_equirectangular()
    projection.fit_height(900, world)
    assert in_delta(projection.get_scale(), 297.042711, 1e-6)
    assert in_delta(projection.get_translation(), [933.187199, 433.411585], 1e-6)

@pytest.mark.skip
def test_fit_28(world):
    projection = d3.geo_transverse_mercator()
    projection.fit_height(900, world)
    assert in_delta(projection.get_scale(), 143.239449, 1e-6)
    assert in_delta(projection.get_translation(), [361.570408, 450], 1e-6)

@pytest.mark.skip
def test_fit_29(us):
    projection = d3.geo_albers_usa()
    projection.fit_height(900, us)
    assert in_delta(projection.get_scale(), 1983.902059, 1e-6)
    assert in_delta(projection.get_translation(), [832.054974, 443.516038], 1e-6)
