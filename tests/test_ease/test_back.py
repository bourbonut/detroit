import detroit as d3

from .generic import in_out, out


def in_delta(actual, expected):
    return expected - 1e-6 < actual and actual < expected + 1e-6


def test_back_1():
    assert d3.ease_back == d3.ease_back_in_out


def test_back_2():
    assert abs(d3.ease_back_in(0.0)) == 0.000000
    assert in_delta(d3.ease_back_in(0.1), -0.014314)
    assert in_delta(d3.ease_back_in(0.2), -0.046451)
    assert in_delta(d3.ease_back_in(0.3), -0.080200)
    assert in_delta(d3.ease_back_in(0.4), -0.099352)
    assert in_delta(d3.ease_back_in(0.5), -0.087698)
    assert in_delta(d3.ease_back_in(0.6), -0.029028)
    assert in_delta(d3.ease_back_in(0.7), +0.092868)
    assert in_delta(d3.ease_back_in(0.8), +0.294198)
    assert in_delta(d3.ease_back_in(0.9), +0.591172)
    assert d3.ease_back_in(1.0) == +1.000000


def test_back_3():
    assert d3.ease_back_in(0.9) == d3.ease_back_in(0.9)


def test_back_4():
    back_out = out(d3.ease_back_in)
    assert d3.ease_back_out(0.0) == back_out(0.0)
    assert in_delta(d3.ease_back_out(0.1), back_out(0.1))
    assert in_delta(d3.ease_back_out(0.2), back_out(0.2))
    assert in_delta(d3.ease_back_out(0.3), back_out(0.3))
    assert in_delta(d3.ease_back_out(0.4), back_out(0.4))
    assert in_delta(d3.ease_back_out(0.5), back_out(0.5))
    assert in_delta(d3.ease_back_out(0.6), back_out(0.6))
    assert in_delta(d3.ease_back_out(0.7), back_out(0.7))
    assert in_delta(d3.ease_back_out(0.8), back_out(0.8))
    assert in_delta(d3.ease_back_out(0.9), back_out(0.9))
    assert d3.ease_back_out(1.0) == back_out(1.0)


def test_back_5():
    assert d3.ease_back_out(0.9) == d3.ease_back_out(0.9)


def test_back_6():
    back_in_out = in_out(d3.ease_back_in)
    assert d3.ease_back_in_out(0.0) == back_in_out(0.0)
    assert in_delta(d3.ease_back_in_out(0.1), back_in_out(0.1))
    assert in_delta(d3.ease_back_in_out(0.2), back_in_out(0.2))
    assert in_delta(d3.ease_back_in_out(0.3), back_in_out(0.3))
    assert in_delta(d3.ease_back_in_out(0.4), back_in_out(0.4))
    assert in_delta(d3.ease_back_in_out(0.5), back_in_out(0.5))
    assert in_delta(d3.ease_back_in_out(0.6), back_in_out(0.6))
    assert in_delta(d3.ease_back_in_out(0.7), back_in_out(0.7))
    assert in_delta(d3.ease_back_in_out(0.8), back_in_out(0.8))
    assert in_delta(d3.ease_back_in_out(0.9), back_in_out(0.9))
    assert d3.ease_back_in_out(1.0) == back_in_out(1.0)


def test_back_7():
    assert d3.ease_back_in_out(0.9) == d3.ease_back_in_out(0.9)
