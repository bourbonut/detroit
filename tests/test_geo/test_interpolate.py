import detroit as d3


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


def test_interpolate_1():
    assert d3.geo_interpolate([140.63289, -29.95101], [140.63289, -29.95101])(0.5) == [
        140.63289,
        -29.95101,
    ]


def test_interpolate_2():
    assert in_delta(d3.geo_interpolate([10, 0], [20, 0])(0.5), [15, 0], 1e-6)


def test_interpolate_3():
    assert in_delta(d3.geo_interpolate([10, -20], [10, 40])(0.5), [10, 10], 1e-6)
