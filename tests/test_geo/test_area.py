from itertools import starmap
from math import ceil, pi, sqrt

import detroit as d3

SQRT2 = sqrt(2)


def frange(start, stop, step):
    return [start + i * step for i in range(max(0, ceil((stop - start) / step)))]


def in_delta(actual, expected, delta=1e-6):
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


def stripes(a, b):
    def change(i, d):
        stripe = [[x, d] for x in frange(-180, 180, 0.1)]
        stripe.append(stripe[0])
        return stripe[::-1] if i else stripe

    return {"type": "Polygon", "coordinates": list(starmap(change, enumerate([a, b])))}


def test_area_1():
    assert d3.geo_area({"type": "Point", "coordinates": [0, 0]}) == 0


def test_area_2():
    assert d3.geo_area({"type": "MultiPoint", "coordinates": [[0, 1], [2, 3]]}) == 0


def test_area_3():
    assert d3.geo_area({"type": "LineString", "coordinates": [[0, 1], [2, 3]]}) == 0


def test_area_4():
    assert (
        d3.geo_area(
            {
                "type": "MultiLineString",
                "coordinates": [[[0, 1], [2, 3]], [[4, 5], [6, 7]]],
            }
        )
        == 0
    )


def test_area_5():
    assert in_delta(
        d3.geo_area(
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-64.66070178517852, 18.33986913231323],
                        [-64.66079715091509, 18.33994007490749],
                        [-64.66074946804680, 18.33994007490749],
                        [-64.66070178517852, 18.33986913231323],
                    ]
                ],
            }
        ),
        4.890516e-13,
        1e-13,
    )


def test_area_6():
    assert (
        d3.geo_area(
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [96.79142432523281, 5.262704519048153],
                        [96.81065389253769, 5.272455576551362],
                        [96.82988345984256, 5.272455576551362],
                        [96.81065389253769, 5.272455576551362],
                        [96.79142432523281, 5.262704519048153],
                    ]
                ],
            }
        )
        == 0
    )


def test_area_7():
    assert in_delta(
        d3.geo_area(
            {"type": "Polygon", "coordinates": [[[0, 0], [0, 90], [90, 0], [0, 0]]]}
        ),
        pi / 2,
        1e-6,
    )


def test_area_8():
    assert in_delta(
        d3.geo_area(
            {
                "type": "Polygon",
                "coordinates": [[[0, 0], [0, 90], [90, 0], [0, -90], [0, 0]]],
            }
        ),
        pi,
        1e-6,
    )


def test_area_9():
    assert in_delta(
        d3.geo_area(
            {
                "type": "Polygon",
                "coordinates": [[[0, 0], [-90, 0], [180, 0], [90, 0], [0, 0]]],
            }
        ),
        2 * pi,
        1e-6,
    )


def test_area_10():
    assert in_delta(
        d3.geo_area(
            {
                "type": "Polygon",
                "coordinates": [[[0, 0], [90, 0], [180, 0], [-90, 0], [0, 0]]],
            }
        ),
        2 * pi,
        1e-6,
    )


def test_area_11():
    assert in_delta(
        d3.geo_area(
            {
                "type": "Polygon",
                "coordinates": [[[0, 0], [0, 90], [180, 0], [0, -90], [0, 0]]],
            }
        ),
        2 * pi,
        1e-6,
    )


def test_area_12():
    assert in_delta(
        d3.geo_area(
            {
                "type": "Polygon",
                "coordinates": [[[0, 0], [0, -90], [180, 0], [0, 90], [0, 0]]],
            }
        ),
        2 * pi,
        1e-6,
    )


def test_area_13():
    assert in_delta(
        d3.geo_area(d3.geo_graticule().set_extent([[-180, -90], [180, 90]]).outline()),
        4 * pi,
        1e-5,
    )


def test_area_14():
    assert in_delta(
        d3.geo_area(d3.geo_graticule().set_extent([[-180, 0], [180, 90]]).outline()),
        2 * pi,
        1e-5,
    )


def test_area_15():
    assert in_delta(
        d3.geo_area(d3.geo_graticule().set_extent([[0, 0], [90, 90]]).outline()),
        pi / 2,
        1e-5,
    )


def test_area_16():
    assert in_delta(d3.geo_area(d3.geo_circle().set_radius(90)()), 2 * pi, 1e-5)


def test_area_17():
    assert in_delta(
        d3.geo_area(d3.geo_circle().set_radius(60).set_precision(0.1)()), pi, 1e-5
    )


def test_area_18():
    assert in_delta(
        d3.geo_area(
            d3.geo_circle().set_radius(60).set_precision(0.1).set_center([0, 90])()
        ),
        pi,
        1e-5,
    )


def test_area_19():
    assert in_delta(
        d3.geo_area(d3.geo_circle().set_radius(45).set_precision(0.1)()),
        pi * (2 - SQRT2),
        1e-5,
    )


def test_area_20():
    assert in_delta(
        d3.geo_area(
            d3.geo_circle().set_radius(45).set_precision(0.1).set_center([0, 90])()
        ),
        pi * (2 - SQRT2),
        1e-5,
    )


def test_area_21():
    assert in_delta(
        d3.geo_area(
            d3.geo_circle().set_radius(45).set_precision(0.1).set_center([0, -90])()
        ),
        pi * (2 - SQRT2),
        1e-5,
    )


def test_area_22():
    assert in_delta(
        d3.geo_area(d3.geo_circle().set_radius(135).set_precision(0.1)()),
        pi * (2 + SQRT2),
        1e-5,
    )


def test_area_23():
    assert in_delta(
        d3.geo_area(
            d3.geo_circle().set_radius(135).set_precision(0.1).set_center([0, 90])()
        ),
        pi * (2 + SQRT2),
        1e-5,
    )


def test_area_24():
    assert in_delta(
        d3.geo_area(
            d3.geo_circle().set_radius(135).set_precision(0.1).set_center([0, -90])()
        ),
        pi * (2 + SQRT2),
        1e-5,
    )


def test_area_25():
    assert in_delta(
        d3.geo_area(d3.geo_circle().set_radius(1e-6).set_precision(0.1)()), 0, 1e-6
    )


def test_area_26():
    assert in_delta(
        d3.geo_area(d3.geo_circle().set_radius(180 - 1e-6).set_precision(0.1)()),
        4 * pi,
        1e-6,
    )


def test_area_27():
    circle = d3.geo_circle().set_precision(0.1)
    assert in_delta(
        d3.geo_area(
            {
                "type": "Polygon",
                "coordinates": [
                    circle.set_radius(60)()["coordinates"][0],
                    circle.set_radius(45)()["coordinates"][0][::-1],
                ],
            }
        ),
        pi * (SQRT2 - 1),
        1e-5,
    )


def test_area_28():
    circle = d3.geo_circle().set_precision(0.1).set_radius(45)
    assert in_delta(
        d3.geo_area(
            {
                "type": "Polygon",
                "coordinates": [
                    circle.set_center([0, 0])()["coordinates"][0][::-1],
                    circle.set_center([0, 90])()["coordinates"][0][::-1],
                ],
            }
        ),
        pi * 2 * SQRT2,
        1e-5,
    )


def test_area_29():
    circle = d3.geo_circle().set_precision(0.1).set_radius(45)
    assert in_delta(
        d3.geo_area(
            {
                "type": "Polygon",
                "coordinates": [
                    circle.set_center([0, 90])()["coordinates"][0][::-1],
                    circle.set_center([0, 0])()["coordinates"][0][::-1],
                ],
            }
        ),
        pi * 2 * SQRT2,
        1e-5,
    )


def test_area_30():
    assert in_delta(d3.geo_area(stripes(45, -45)), pi * 2 * SQRT2, 1e-5)


def test_area_31():
    assert in_delta(d3.geo_area(stripes(-45, 45)), pi * 2 * (2 - SQRT2), 1e-5)


def test_area_32():
    assert in_delta(d3.geo_area(stripes(45, 30)), pi * (SQRT2 - 1), 1e-5)


def test_area_33():
    assert (
        d3.geo_area(
            {
                "type": "MultiPolygon",
                "coordinates": [
                    [[[0, 0], [-90, 0], [180, 0], [90, 0], [0, 0]]],
                    [[[0, 0], [90, 0], [180, 0], [-90, 0], [0, 0]]],
                ],
            }
        )
        == 4 * pi
    )


def test_area_34():
    assert d3.geo_area({"type": "Sphere"}) == 4 * pi


def test_area_35():
    assert (
        d3.geo_area({"type": "GeometryCollection", "geometries": [{"type": "Sphere"}]})
        == 4 * pi
    )


def test_area_36():
    assert (
        d3.geo_area(
            {
                "type": "FeatureCollection",
                "features": [{"type": "Feature", "geometry": {"type": "Sphere"}}],
            }
        )
        == 4 * pi
    )


def test_area_37():
    assert d3.geo_area({"type": "Feature", "geometry": {"type": "Sphere"}}) == 4 * pi
