import detroit as d3

from .generic import in_out, out


def in_delta(actual, expected):
    return expected - 1e-6 < actual and actual < expected + 1e-6


def test_cubic_1():
    assert d3.ease_cubic == d3.ease_cubic_in_out


def test_cubic_2():
    assert d3.ease_cubic_in(0.0) == 0.000
    assert in_delta(d3.ease_cubic_in(0.1), 0.001)
    assert in_delta(d3.ease_cubic_in(0.2), 0.008)
    assert in_delta(d3.ease_cubic_in(0.3), 0.027)
    assert in_delta(d3.ease_cubic_in(0.4), 0.064)
    assert in_delta(d3.ease_cubic_in(0.5), 0.125)
    assert in_delta(d3.ease_cubic_in(0.6), 0.216)
    assert in_delta(d3.ease_cubic_in(0.7), 0.343)
    assert in_delta(d3.ease_cubic_in(0.8), 0.512)
    assert in_delta(d3.ease_cubic_in(0.9), 0.729)
    assert d3.ease_cubic_in(1.0) == 1.000


def test_cubic_3():
    assert d3.ease_cubic_in(0.9) == d3.ease_cubic_in(0.9)


def test_cubic_4():
    cubic_out = out(d3.ease_cubic_in)
    assert d3.ease_cubic_out(0.0) == cubic_out(0.0)
    assert in_delta(d3.ease_cubic_out(0.1), cubic_out(0.1))
    assert in_delta(d3.ease_cubic_out(0.2), cubic_out(0.2))
    assert in_delta(d3.ease_cubic_out(0.3), cubic_out(0.3))
    assert in_delta(d3.ease_cubic_out(0.4), cubic_out(0.4))
    assert in_delta(d3.ease_cubic_out(0.5), cubic_out(0.5))
    assert in_delta(d3.ease_cubic_out(0.6), cubic_out(0.6))
    assert in_delta(d3.ease_cubic_out(0.7), cubic_out(0.7))
    assert in_delta(d3.ease_cubic_out(0.8), cubic_out(0.8))
    assert in_delta(d3.ease_cubic_out(0.9), cubic_out(0.9))
    assert d3.ease_cubic_out(1.0) == cubic_out(1.0)


def test_cubic_5():
    assert d3.ease_cubic_out(0.9) == d3.ease_cubic_out(0.9)


def test_cubic_6():
    cubic_in_out = in_out(d3.ease_cubic_in)
    assert d3.ease_cubic_in_out(0.0) == cubic_in_out(0.0)
    assert in_delta(d3.ease_cubic_in_out(0.1), cubic_in_out(0.1))
    assert in_delta(d3.ease_cubic_in_out(0.2), cubic_in_out(0.2))
    assert in_delta(d3.ease_cubic_in_out(0.3), cubic_in_out(0.3))
    assert in_delta(d3.ease_cubic_in_out(0.4), cubic_in_out(0.4))
    assert in_delta(d3.ease_cubic_in_out(0.5), cubic_in_out(0.5))
    assert in_delta(d3.ease_cubic_in_out(0.6), cubic_in_out(0.6))
    assert in_delta(d3.ease_cubic_in_out(0.7), cubic_in_out(0.7))
    assert in_delta(d3.ease_cubic_in_out(0.8), cubic_in_out(0.8))
    assert in_delta(d3.ease_cubic_in_out(0.9), cubic_in_out(0.9))
    assert d3.ease_cubic_in_out(1.0) == cubic_in_out(1.0)


def test_cubic_7():
    assert d3.ease_cubic_in_out(0.9) == d3.ease_cubic_in_out(0.9)
