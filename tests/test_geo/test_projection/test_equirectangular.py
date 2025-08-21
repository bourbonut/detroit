import detroit as d3
from math import pi


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


def test_equirectangular_1():
    equirectangular = d3.geo_equirectangular().translate([0, 0]).scale(1)
    assert projection_equal(equirectangular, [0, 0], [0, 0])
    assert projection_equal(equirectangular, [-180, 0], [-pi, 0])
    assert projection_equal(equirectangular, [180, 0], [pi, 0])
    assert projection_equal(equirectangular, [0, 30], [0, -pi / 6])
    assert projection_equal(equirectangular, [0, -30], [0, pi / 6])
    assert projection_equal(equirectangular, [30, 30], [pi / 6, -pi / 6])
    assert projection_equal(equirectangular, [30, -30], [pi / 6, pi / 6])
    assert projection_equal(equirectangular, [-30, 30], [-pi / 6, -pi / 6])
    assert projection_equal(equirectangular, [-30, -30], [-pi / 6, pi / 6])


def test_equirectangular_2():
    equirectangular = (
        d3.geo_equirectangular().rotate([30, 0]).translate([0, 0]).scale(1)
    )
    assert projection_equal(equirectangular, [0, 0], [pi / 6, 0])
    assert projection_equal(equirectangular, [-180, 0], [-5 / 6 * pi, 0])
    assert projection_equal(equirectangular, [180, 0], [-5 / 6 * pi, 0])
    assert projection_equal(equirectangular, [0, 30], [pi / 6, -pi / 6])
    assert projection_equal(equirectangular, [0, -30], [pi / 6, pi / 6])
    assert projection_equal(equirectangular, [30, 30], [pi / 3, -pi / 6])
    assert projection_equal(equirectangular, [30, -30], [pi / 3, pi / 6])
    assert projection_equal(equirectangular, [-30, 30], [0, -pi / 6])
    assert projection_equal(equirectangular, [-30, -30], [0, pi / 6])


def test_equirectangular_3():
    equirectangular = (
        d3.geo_equirectangular().rotate([30, 30]).translate([0, 0]).scale(1)
    )
    assert projection_equal(
        equirectangular, [0, 0], [0.5880026035475674, -0.44783239692893245]
    )
    assert projection_equal(
        equirectangular, [-180, 0], [-2.5535900500422257, 0.44783239692893245]
    )
    assert projection_equal(
        equirectangular, [180, 0], [-2.5535900500422257, 0.44783239692893245]
    )
    assert projection_equal(
        equirectangular, [0, 30], [0.8256075561643480, -0.9407711951705208]
    )
    assert projection_equal(
        equirectangular, [0, -30], [0.4486429615608479, 0.05804529130778048]
    )
    assert projection_equal(
        equirectangular, [30, 30], [1.4056476493802694, -0.7069517278872177]
    )
    assert projection_equal(
        equirectangular, [30, -30], [0.8760580505981933, 0.21823451436745955]
    )
    assert projection_equal(
        equirectangular, [-30, 30], [0.0000000000000000, -1.0471975511965976]
    )
    assert projection_equal(
        equirectangular, [-30, -30], [0.0000000000000000, 0.00000000000000000]
    )


def test_equirectangular_4():
    equirectangular = (
        d3.geo_equirectangular().rotate([0, 0, 30]).translate([0, 0]).scale(1)
    )
    assert projection_equal(equirectangular, [0, 0], [0, 0])
    assert projection_equal(equirectangular, [-180, 0], [-pi, 0])
    assert projection_equal(equirectangular, [180, 0], [pi, 0])
    assert projection_equal(
        equirectangular, [0, 30], [-0.2810349015028135, -0.44783239692893245]
    )
    assert projection_equal(
        equirectangular, [0, -30], [0.2810349015028135, 0.44783239692893245]
    )
    assert projection_equal(
        equirectangular, [30, 30], [0.1651486774146268, -0.7069517278872176]
    )
    assert projection_equal(
        equirectangular, [30, -30], [0.6947382761967031, 0.21823451436745964]
    )
    assert projection_equal(
        equirectangular, [-30, 30], [-0.6947382761967031, -0.21823451436745964]
    )
    assert projection_equal(
        equirectangular, [-30, -30], [-0.1651486774146268, 0.7069517278872176]
    )


def test_equirectangular_5():
    equirectangular = (
        d3.geo_equirectangular().rotate([30, 30, 30]).translate([0, 0]).scale(1)
    )
    assert projection_equal(
        equirectangular, [0, 0], [0.2810349015028135, -0.6751315329370317]
    )
    assert projection_equal(
        equirectangular, [-180, 0], [-2.860557752086980, 0.6751315329370317]
    )
    assert projection_equal(
        equirectangular, [180, 0], [-2.860557752086980, 0.6751315329370317]
    )
    assert projection_equal(
        equirectangular, [0, 30], [-0.0724760059270816, -1.1586567708659772]
    )
    assert projection_equal(
        equirectangular, [0, -30], [0.4221351552567053, -0.16704161863132252]
    )
    assert projection_equal(
        equirectangular, [30, 30], [1.2033744221750944, -1.2153751251046732]
    )
    assert projection_equal(
        equirectangular, [30, -30], [0.8811235701944905, -0.18861638617540410]
    )
    assert projection_equal(
        equirectangular, [-30, 30], [-0.7137243789447654, -0.84806207898148100]
    )
    assert projection_equal(equirectangular, [-30, -30], [0, 0])
