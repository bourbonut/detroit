import detroit as d3

from .generic import in_out, out


def in_delta(actual, expected):
    return expected - 1e-6 < actual and actual < expected + 1e-6


def test_circle_1():
    assert d3.ease_circle == d3.ease_circle_in_out


def test_circle_2():
    assert d3.ease_circle_in(0.0) == 0.000000
    assert in_delta(d3.ease_circle_in(0.1), 0.005013)
    assert in_delta(d3.ease_circle_in(0.2), 0.020204)
    assert in_delta(d3.ease_circle_in(0.3), 0.046061)
    assert in_delta(d3.ease_circle_in(0.4), 0.083485)
    assert in_delta(d3.ease_circle_in(0.5), 0.133975)
    assert in_delta(d3.ease_circle_in(0.6), 0.200000)
    assert in_delta(d3.ease_circle_in(0.7), 0.285857)
    assert in_delta(d3.ease_circle_in(0.8), 0.400000)
    assert in_delta(d3.ease_circle_in(0.9), 0.564110)
    assert d3.ease_circle_in(1.0) == 1.000000


def test_circle_3():
    assert d3.ease_circle_in(0.9) == d3.ease_circle_in(0.9)


def test_circle_4():
    circle_out = out(d3.ease_circle_in)
    assert d3.ease_circle_out(0.0) == circle_out(0.0)
    assert in_delta(d3.ease_circle_out(0.1), circle_out(0.1))
    assert in_delta(d3.ease_circle_out(0.2), circle_out(0.2))
    assert in_delta(d3.ease_circle_out(0.3), circle_out(0.3))
    assert in_delta(d3.ease_circle_out(0.4), circle_out(0.4))
    assert in_delta(d3.ease_circle_out(0.5), circle_out(0.5))
    assert in_delta(d3.ease_circle_out(0.6), circle_out(0.6))
    assert in_delta(d3.ease_circle_out(0.7), circle_out(0.7))
    assert in_delta(d3.ease_circle_out(0.8), circle_out(0.8))
    assert in_delta(d3.ease_circle_out(0.9), circle_out(0.9))
    assert d3.ease_circle_out(1.0) == circle_out(1.0)


def test_circle_5():
    assert d3.ease_circle_out(0.9) == d3.ease_circle_out(0.9)


def test_circle_6():
    circle_in_out = in_out(d3.ease_circle_in)
    assert d3.ease_circle_in_out(0.0) == circle_in_out(0.0)
    assert in_delta(d3.ease_circle_in_out(0.1), circle_in_out(0.1))
    assert in_delta(d3.ease_circle_in_out(0.2), circle_in_out(0.2))
    assert in_delta(d3.ease_circle_in_out(0.3), circle_in_out(0.3))
    assert in_delta(d3.ease_circle_in_out(0.4), circle_in_out(0.4))
    assert in_delta(d3.ease_circle_in_out(0.5), circle_in_out(0.5))
    assert in_delta(d3.ease_circle_in_out(0.6), circle_in_out(0.6))
    assert in_delta(d3.ease_circle_in_out(0.7), circle_in_out(0.7))
    assert in_delta(d3.ease_circle_in_out(0.8), circle_in_out(0.8))
    assert in_delta(d3.ease_circle_in_out(0.9), circle_in_out(0.9))
    assert d3.ease_circle_in_out(1.0) == circle_in_out(1.0)


def test_circle_7():
    assert d3.ease_circle_in_out(0.9) == d3.ease_circle_in_out(0.9)
