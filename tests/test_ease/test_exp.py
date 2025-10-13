import detroit as d3

from .generic import in_out, out


def in_delta(actual, expected):
    return expected - 1e-6 < actual and actual < expected + 1e-6


def test_exp_1():
    assert d3.ease_exp == d3.ease_exp_in_out


def test_exp_2():
    assert d3.ease_exp_in(0.0) == 0.000000
    assert in_delta(d3.ease_exp_in(0.1), 0.000978)
    assert in_delta(d3.ease_exp_in(0.2), 0.002933)
    assert in_delta(d3.ease_exp_in(0.3), 0.006843)
    assert in_delta(d3.ease_exp_in(0.4), 0.014663)
    assert in_delta(d3.ease_exp_in(0.5), 0.030303)
    assert in_delta(d3.ease_exp_in(0.6), 0.061584)
    assert in_delta(d3.ease_exp_in(0.7), 0.124145)
    assert in_delta(d3.ease_exp_in(0.8), 0.249267)
    assert in_delta(d3.ease_exp_in(0.9), 0.499511)
    assert d3.ease_exp_in(1.0) == 1.000000


def test_exp_3():
    assert d3.ease_exp_in(0.9) == d3.ease_exp_in(0.9)


def test_exp_4():
    exp_out = out(d3.ease_exp_in)
    assert in_delta(d3.ease_exp_out(0.0), exp_out(0.0))
    assert in_delta(d3.ease_exp_out(0.1), exp_out(0.1))
    assert in_delta(d3.ease_exp_out(0.2), exp_out(0.2))
    assert in_delta(d3.ease_exp_out(0.3), exp_out(0.3))
    assert in_delta(d3.ease_exp_out(0.4), exp_out(0.4))
    assert in_delta(d3.ease_exp_out(0.5), exp_out(0.5))
    assert in_delta(d3.ease_exp_out(0.6), exp_out(0.6))
    assert in_delta(d3.ease_exp_out(0.7), exp_out(0.7))
    assert in_delta(d3.ease_exp_out(0.8), exp_out(0.8))
    assert in_delta(d3.ease_exp_out(0.9), exp_out(0.9))
    assert in_delta(d3.ease_exp_out(1.0), exp_out(1.0))


def test_exp_5():
    assert d3.ease_exp_out(0.9) == d3.ease_exp_out(0.9)


def test_exp_6():
    exp_in_out = in_out(d3.ease_exp_in)
    assert d3.ease_exp_in_out(0.0) == exp_in_out(0.0)
    assert in_delta(d3.ease_exp_in_out(0.1), exp_in_out(0.1))
    assert in_delta(d3.ease_exp_in_out(0.2), exp_in_out(0.2))
    assert in_delta(d3.ease_exp_in_out(0.3), exp_in_out(0.3))
    assert in_delta(d3.ease_exp_in_out(0.4), exp_in_out(0.4))
    assert in_delta(d3.ease_exp_in_out(0.5), exp_in_out(0.5))
    assert in_delta(d3.ease_exp_in_out(0.6), exp_in_out(0.6))
    assert in_delta(d3.ease_exp_in_out(0.7), exp_in_out(0.7))
    assert in_delta(d3.ease_exp_in_out(0.8), exp_in_out(0.8))
    assert in_delta(d3.ease_exp_in_out(0.9), exp_in_out(0.9))
    assert d3.ease_exp_in_out(1.0) == exp_in_out(1.0)


def test_exp_7():
    assert d3.ease_exp_in_out(0.9) == d3.ease_exp_in_out(0.9)
