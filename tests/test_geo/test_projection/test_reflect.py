import detroit as d3

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

def in_delta_number(actual, expected, delta=1e-6):
    return actual >= expected - delta and actual <= expected + delta


def test_reflect_1():
    projection = d3.geo_gnomonic().scale(1).translate([0, 0])
    assert projection.get_reflect_x() is False
    assert projection.get_reflect_y() is False
    assert projection_equal(projection, [0, 0], [0, 0])
    assert projection_equal(projection, [10, 0], [0.17632698070846498, 0])
    assert projection_equal(projection, [0, 10], [0, -0.17632698070846498])

def test_reflect_2():
    projection = d3.geo_gnomonic().scale(1).translate([0, 0]).set_reflect_x(True)
    assert projection.get_reflect_x() is True
    assert projection_equal(projection, [0, 0], [0, 0])
    assert projection_equal(projection, [10, 0], [-0.17632698070846498, 0])
    assert projection_equal(projection, [0, 10], [0, -0.17632698070846498])
    projection.set_reflect_x(False).set_reflect_y(True)
    assert projection.get_reflect_x() is False
    assert projection.get_reflect_y() is True
    assert projection_equal(projection, [0, 0], [0, 0])
    assert projection_equal(projection, [10, 0], [0.17632698070846498, 0])
    assert projection_equal(projection, [0, 10], [0, 0.17632698070846498])

def test_reflect_3():
    projection = d3.geo_mercator().scale(1).translate([10, 20]).set_reflect_x(True).set_angle(45)
    assert projection.get_reflect_x() is True
    assert in_delta_number(projection.get_angle(), 45)
    assert projection_equal(projection, [0, 0], [10, 20])
    assert projection_equal(projection, [10, 0], [9.87658658, 20.12341341])
    assert projection_equal(projection, [0, 10], [9.87595521, 19.87595521])
