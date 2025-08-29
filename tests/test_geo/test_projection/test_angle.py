from math import sqrt

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


def test_angle_1():
    projection = d3.geo_gnomonic().scale(1).translate([0, 0])
    assert projection.get_angle() == 0
    assert projection_equal(projection, [0, 0], [0, 0])
    assert projection_equal(projection, [10, 0], [0.17632698070846498, 0])
    assert projection_equal(projection, [-10, 0], [-0.17632698070846498, 0])
    assert projection_equal(projection, [0, 10], [0, -0.17632698070846498])
    assert projection_equal(projection, [0, -10], [0, 0.17632698070846498])
    assert projection_equal(
        projection, [10, 10], [0.17632698070846495, -0.17904710860483972]
    )
    assert projection_equal(
        projection, [10, -10], [0.17632698070846495, 0.17904710860483972]
    )
    assert projection_equal(
        projection, [-10, 10], [-0.17632698070846495, -0.17904710860483972]
    )
    assert projection_equal(
        projection, [-10, -10], [-0.17632698070846495, 0.17904710860483972]
    )


def test_angle_2():
    projection = d3.geo_gnomonic().scale(1).translate([0, 0]).set_angle(30)
    assert in_delta_number(projection.get_angle(), 30)
    assert projection_equal(projection, [0, 0], [0, 0])
    assert projection_equal(
        projection, [10, 0], [0.1527036446661393, -0.08816349035423247]
    )
    assert projection_equal(
        projection, [-10, 0], [-0.1527036446661393, 0.08816349035423247]
    )
    assert projection_equal(
        projection, [0, 10], [-0.08816349035423247, -0.1527036446661393]
    )
    assert projection_equal(
        projection, [0, -10], [0.08816349035423247, 0.1527036446661393]
    )
    assert projection_equal(
        projection, [10, 10], [0.06318009036371944, -0.24322283488017502]
    )
    assert projection_equal(
        projection, [10, -10], [0.24222719896855913, 0.0668958541717101]
    )
    assert projection_equal(
        projection, [-10, 10], [-0.24222719896855913, -0.0668958541717101]
    )
    assert projection_equal(
        projection, [-10, -10], [-0.06318009036371944, 0.24322283488017502]
    )


def test_angle_3():
    projection = d3.geo_gnomonic().scale(1).translate([0, 0]).set_angle(-30)
    assert in_delta_number(projection.get_angle(), -30)
    assert projection_equal(projection, [0, 0], [0, 0])
    assert projection_equal(
        projection, [10, 0], [0.1527036446661393, 0.08816349035423247]
    )
    assert projection_equal(
        projection, [-10, 0], [-0.1527036446661393, -0.08816349035423247]
    )
    assert projection_equal(
        projection, [0, 10], [0.08816349035423247, -0.1527036446661393]
    )
    assert projection_equal(
        projection, [0, -10], [-0.08816349035423247, 0.1527036446661393]
    )
    assert projection_equal(
        projection, [10, 10], [0.24222719896855913, -0.0668958541717101]
    )
    assert projection_equal(
        projection, [10, -10], [0.06318009036371944, 0.24322283488017502]
    )
    assert projection_equal(
        projection, [-10, 10], [-0.06318009036371944, -0.24322283488017502]
    )
    assert projection_equal(
        projection, [-10, -10], [-0.24222719896855913, 0.0668958541717101]
    )


def test_angle_4():
    projection = d3.geo_gnomonic().scale(1).translate([0, 0]).set_angle(360)
    assert projection.get_angle() == 360


def test_angle_5():
    projection = d3.geo_identity().set_angle(-45)
    SQRT2_2 = sqrt(2) / 2
    assert in_delta_number(projection.get_angle(), -45)
    assert projection_equal(projection, [0, 0], [0, 0])
    assert projection_equal(projection, [1, 0], [SQRT2_2, SQRT2_2])
    assert projection_equal(projection, [-1, 0], [-SQRT2_2, -SQRT2_2])
    assert projection_equal(projection, [0, 1], [-SQRT2_2, SQRT2_2])
