import detroit as d3

from .generic import in_out, out


def in_delta(actual, expected):
    return expected - 1e-6 < actual and actual < expected + 1e-6


def test_quad_1():
    assert d3.ease_quad == d3.ease_quad_in_out


def test_quad_2():
    assert d3.ease_quad_in(0.0) == 0.00
    assert in_delta(d3.ease_quad_in(0.1), 0.01)
    assert in_delta(d3.ease_quad_in(0.2), 0.04)
    assert in_delta(d3.ease_quad_in(0.3), 0.09)
    assert in_delta(d3.ease_quad_in(0.4), 0.16)
    assert in_delta(d3.ease_quad_in(0.5), 0.25)
    assert in_delta(d3.ease_quad_in(0.6), 0.36)
    assert in_delta(d3.ease_quad_in(0.7), 0.49)
    assert in_delta(d3.ease_quad_in(0.8), 0.64)
    assert in_delta(d3.ease_quad_in(0.9), 0.81)
    assert d3.ease_quad_in(1.0) == 1.00


def test_quad_3():
    assert d3.ease_quad_in(0.9) == d3.ease_quad_in(0.9)


def test_quad_4():
    quad_out = out(d3.ease_quad_in)
    assert in_delta(d3.ease_quad_out(0.0), quad_out(0.0))
    assert in_delta(d3.ease_quad_out(0.1), quad_out(0.1))
    assert in_delta(d3.ease_quad_out(0.2), quad_out(0.2))
    assert in_delta(d3.ease_quad_out(0.3), quad_out(0.3))
    assert in_delta(d3.ease_quad_out(0.4), quad_out(0.4))
    assert in_delta(d3.ease_quad_out(0.5), quad_out(0.5))
    assert in_delta(d3.ease_quad_out(0.6), quad_out(0.6))
    assert in_delta(d3.ease_quad_out(0.7), quad_out(0.7))
    assert in_delta(d3.ease_quad_out(0.8), quad_out(0.8))
    assert in_delta(d3.ease_quad_out(0.9), quad_out(0.9))
    assert in_delta(d3.ease_quad_out(1.0), quad_out(1.0))


def test_quad_5():
    assert d3.ease_quad_out(0.9) == d3.ease_quad_out(0.9)


def test_quad_6():
    quad_in_out = in_out(d3.ease_quad_in)
    assert in_delta(d3.ease_quad_in_out(0.0), quad_in_out(0.0))
    assert in_delta(d3.ease_quad_in_out(0.1), quad_in_out(0.1))
    assert in_delta(d3.ease_quad_in_out(0.2), quad_in_out(0.2))
    assert in_delta(d3.ease_quad_in_out(0.3), quad_in_out(0.3))
    assert in_delta(d3.ease_quad_in_out(0.4), quad_in_out(0.4))
    assert in_delta(d3.ease_quad_in_out(0.5), quad_in_out(0.5))
    assert in_delta(d3.ease_quad_in_out(0.6), quad_in_out(0.6))
    assert in_delta(d3.ease_quad_in_out(0.7), quad_in_out(0.7))
    assert in_delta(d3.ease_quad_in_out(0.8), quad_in_out(0.8))
    assert in_delta(d3.ease_quad_in_out(0.9), quad_in_out(0.9))
    assert in_delta(d3.ease_quad_in_out(1.0), quad_in_out(1.0))


def test_quad_7():
    assert d3.ease_quad_in_out(0.9) == d3.ease_quad_in_out(0.9)
