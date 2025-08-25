import detroit as d3
import pytest

def projection_equal(projection, location, point, delta=None):
    return planar_equal(projection(location), point, delta or 1e-6) and spherical_equal(
        projection.invert(point), location, delta or 1e-3
    )

def planar_equal(actual, expected, delta):
    return (
        isinstance(actual, list)
        and len(actual) == 2
        and in_delta(actual[0], expected[0], delta)
        and in_delta(actual[0], expected[0], delta)
    )

def spherical_equal(actual, expected, delta):
    return (
        isinstance(actual, list)
        and len(actual) == 2
        and longitude_equal(actual[0], expected[0], delta)
        and in_delta(actual[1], expected[1], delta)
    )


def longitude_equal(actual, expected, delta):
    actual = abs(actual - expected) % 360
    return actual <= delta or actual >= 360 - delta


def in_delta(actual, expected, delta):
    return abs(actual - expected) <= delta

def conic_conformal_1():
	 return d3.geo_conic_conformal().parallels([20, 30])
def conic_conformal_2():
	 return d3.geo_conic_conformal().parallels([30, 30])
def conic_conformal_3():
	 return d3.geo_conic_conformal().parallels([-35, -50])
def conic_conformal_4():
	 return d3.geo_conic_conformal().parallels([40, 60]).rotate([-120,0])
def conic_equal_area_1():
	 return d3.geo_conic_equal_area().parallels([20, 30])
def conic_equal_area_2():
	 return d3.geo_conic_equal_area().parallels([-30, 30])
def conic_equal_area_3():
	 return d3.geo_conic_equal_area().parallels([-35, -50])
def conic_equal_area_4():
	 return d3.geo_conic_equal_area().parallels([40, 60]).rotate([-120,0])
def conic_equidistant_1():
	 return d3.geo_conic_equidistant().parallels([20, 30])
def conic_equidistant_2():
	 return d3.geo_conic_equidistant().parallels([30, 30])
def conic_equidistant_3():
	 return d3.geo_conic_equidistant().parallels([-35, -50])
def conic_equidistant_4():
	 return d3.geo_conic_equidistant().parallels([40, 60]).rotate([-120,0])

projections = [
    d3.geo_albers,
    d3.geo_azimuthal_equal_area,
    d3.geo_azimuthal_equidistant,
    d3.geo_conic_conformal,
    d3.geo_conic_equal_area,
    d3.geo_conic_equidistant,
    d3.geo_equal_earth,
    d3.geo_equirectangular,
    d3.geo_gnomonic,
    d3.geo_mercator,
    d3.geo_orthographic,
    d3.geo_stereographic,
    d3.geo_transverse_mercator,
    conic_conformal_1,
    conic_conformal_2,
    conic_conformal_3,
    conic_conformal_4,
    conic_equal_area_1,
    conic_equal_area_2,
    conic_equal_area_3,
    conic_equal_area_4,
    conic_equidistant_1,
    conic_equidistant_2,
    conic_equidistant_3,
    conic_equidistant_4,
]

@pytest.mark.parametrize("factory", projections)
def test_invert(factory):
    projection = factory()
    for point in [[0, 0], [30.3, 24.1], [-10, 42], [-2, -5]]:
        assert projection_equal(projection, point, projection(point))

def test_invert_albers_usa():
    projection = d3.geo_albers_usa()
    for point in [[-122.4194, 37.7749], [-74.0059, 40.7128], [-149.9003, 61.2181], [-157.8583, 21.3069]]:
        assert projection_equal(projection, point, projection(point))
