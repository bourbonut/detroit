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


def test_stereographic_1():
    stereographic = d3.geo_stereographic().translate([0, 0]).scale(1)
    assert projection_equal(stereographic, [0, 0], [0, 0])
    assert projection_equal(stereographic, [-90, 0], [-1, 0])
    assert projection_equal(stereographic, [90, 0], [1, 0])
    assert projection_equal(stereographic, [0, -90], [0, 1])
    assert projection_equal(stereographic, [0, 90], [0, -1])
