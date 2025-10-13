import detroit as d3

from .generic import in_out, out


def in_delta(actual, expected):
    return expected - 1e-6 < actual and actual < expected + 1e-6


def test_sin_1():
    assert d3.ease_sin == d3.ease_sin_in_out


def test_sin_2():
    assert d3.ease_sin_in(0.0) == 0.000000
    assert in_delta(d3.ease_sin_in(0.1), 0.012312)
    assert in_delta(d3.ease_sin_in(0.2), 0.048943)
    assert in_delta(d3.ease_sin_in(0.3), 0.108993)
    assert in_delta(d3.ease_sin_in(0.4), 0.190983)
    assert in_delta(d3.ease_sin_in(0.5), 0.292893)
    assert in_delta(d3.ease_sin_in(0.6), 0.412215)
    assert in_delta(d3.ease_sin_in(0.7), 0.546010)
    assert in_delta(d3.ease_sin_in(0.8), 0.690983)
    assert in_delta(d3.ease_sin_in(0.9), 0.843566)
    assert d3.ease_sin_in(1.0) == 1.000000


def test_sin_3():
    assert d3.ease_sin_in(0.9) == d3.ease_sin_in(0.9)


def test_sin_4():
    sin_out = out(d3.ease_sin_in)
    assert in_delta(d3.ease_sin_out(0.0), sin_out(0.0))
    assert in_delta(d3.ease_sin_out(0.1), sin_out(0.1))
    assert in_delta(d3.ease_sin_out(0.2), sin_out(0.2))
    assert in_delta(d3.ease_sin_out(0.3), sin_out(0.3))
    assert in_delta(d3.ease_sin_out(0.4), sin_out(0.4))
    assert in_delta(d3.ease_sin_out(0.5), sin_out(0.5))
    assert in_delta(d3.ease_sin_out(0.6), sin_out(0.6))
    assert in_delta(d3.ease_sin_out(0.7), sin_out(0.7))
    assert in_delta(d3.ease_sin_out(0.8), sin_out(0.8))
    assert in_delta(d3.ease_sin_out(0.9), sin_out(0.9))
    assert in_delta(d3.ease_sin_out(1.0), sin_out(1.0))


def test_sin_5():
    assert d3.ease_sin_out(0.9) == d3.ease_sin_out(0.9)


def test_sin_6():
    sin_in_out = in_out(d3.ease_sin_in)
    assert in_delta(d3.ease_sin_in_out(0.0), sin_in_out(0.0))
    assert in_delta(d3.ease_sin_in_out(0.1), sin_in_out(0.1))
    assert in_delta(d3.ease_sin_in_out(0.2), sin_in_out(0.2))
    assert in_delta(d3.ease_sin_in_out(0.3), sin_in_out(0.3))
    assert in_delta(d3.ease_sin_in_out(0.4), sin_in_out(0.4))
    assert in_delta(d3.ease_sin_in_out(0.5), sin_in_out(0.5))
    assert in_delta(d3.ease_sin_in_out(0.6), sin_in_out(0.6))
    assert in_delta(d3.ease_sin_in_out(0.7), sin_in_out(0.7))
    assert in_delta(d3.ease_sin_in_out(0.8), sin_in_out(0.8))
    assert in_delta(d3.ease_sin_in_out(0.9), sin_in_out(0.9))
    assert in_delta(d3.ease_sin_in_out(1.0), sin_in_out(1.0))


def test_sin_7():
    assert d3.ease_sin_in_out(0.9) == d3.ease_sin_in_out(0.9)
