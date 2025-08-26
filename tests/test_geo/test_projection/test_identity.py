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


def test_identity_1():
    identity = d3.geo_identity().translate([0, 0]).scale(1)
    assert projection_equal(identity, [0, 0], [0, 0])
    assert projection_equal(identity, [-180, 0], [-180, 0])
    assert projection_equal(identity, [180, 0], [180, 0])
    assert projection_equal(identity, [30, 30], [30, 30])


def test_identity_2():
    identity = d3.geo_identity().translate([100, 10]).scale(2)
    assert projection_equal(identity, [0, 0], [100, 10])
    assert projection_equal(identity, [-180, 0], [-260, 10])
    assert projection_equal(identity, [180, 0], [460, 10])
    assert projection_equal(identity, [30, 30], [160, 70])


def test_identity_3():
    identity = (
        d3.geo_identity()
        .translate([100, 10])
        .scale(2)
        .set_reflect_x(False)
        .set_reflect_y(False)
    )
    assert projection_equal(identity, [3, 7], [106, 24])
    assert projection_equal(identity.set_reflect_x(True), [3, 7], [94, 24])
    assert projection_equal(identity.set_reflect_y(True), [3, 7], [94, -4])
    assert projection_equal(identity.set_reflect_x(False), [3, 7], [106, -4])
    assert projection_equal(identity.set_reflect_y(False), [3, 7], [106, 24])


def test_identity_4():
    identity = d3.geo_identity().translate([0, 0]).scale(1)
    path = d3.geo_path().set_projection(identity)
    assert (
        path({"type": "LineString", "coordinates": [[0, 0], [10, 10]]}) == "M0,0L10,10"
    )
    identity.translate([30, 90]).scale(2).set_reflect_y(True)
    assert (
        path({"type": "LineString", "coordinates": [[0, 0], [10, 10]]})
        == "M30,90L50,70"
    )


def test_identity_5():
    identity = d3.geo_identity().translate([0, 0]).scale(1)
    path = d3.geo_path().set_projection(identity)
    identity.set_clip_extent([[5, 5], [40, 80]])
    assert (
        path({"type": "LineString", "coordinates": [[0, 0], [10, 10]]}) == "M5,5L10,10"
    )
    identity.translate([30, 90]).scale(2).set_reflect_y(True).set_clip_extent(
        [[35, 76], [45, 86]]
    )
    assert (
        path({"type": "LineString", "coordinates": [[0, 0], [10, 10]]})
        == "M35,85L44,76"
    )
