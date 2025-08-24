import detroit as d3

def projection_equal(projection, location, point, delta=None):
    print(projection(location), point)
    print(projection.invert(point), delta)
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

def test_albert_usa_1():
    albers_usa = d3.geo_albers_usa()
    assert projection_equal(albers_usa, [-122.4194, 37.7749], [107.4, 214.1], 0.1) # San Francisco, CA
    assert projection_equal(albers_usa, [ -74.0059, 40.7128], [794.6, 176.5], 0.1) # New York, NY
    assert projection_equal(albers_usa, [ -95.9928, 36.1540], [488.8, 298.0], 0.1) # Tulsa, OK
    assert projection_equal(albers_usa, [-149.9003, 61.2181], [171.2, 446.9], 0.1) # Anchorage, AK
    assert projection_equal(albers_usa, [-157.8583, 21.3069], [298.5, 451.0], 0.1) # Honolulu, HI
    assert albers_usa([2.3522, 48.8566]) is None # Paris, France
