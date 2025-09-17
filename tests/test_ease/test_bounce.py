import detroit as d3
from .generic import out, in_out

def in_delta(actual, expected):
    return expected - 1e-6 < actual and actual < expected + 1e-6

def test_bounce_1():
    assert d3.ease_bounce == d3.ease_bounce_out

def test_bounce_2():
    assert d3.ease_bounce_in(0.0) == 0.000000
    assert in_delta(d3.ease_bounce_in(0.1), 0.011875)
    assert in_delta(d3.ease_bounce_in(0.2), 0.060000)
    assert in_delta(d3.ease_bounce_in(0.3), 0.069375)
    assert in_delta(d3.ease_bounce_in(0.4), 0.227500)
    assert in_delta(d3.ease_bounce_in(0.5), 0.234375)
    assert in_delta(d3.ease_bounce_in(0.6), 0.090000)
    assert in_delta(d3.ease_bounce_in(0.7), 0.319375)
    assert in_delta(d3.ease_bounce_in(0.8), 0.697500)
    assert in_delta(d3.ease_bounce_in(0.9), 0.924375)
    assert d3.ease_bounce_in(1.0) == 1.000000

def test_bounce_3():
    assert d3.ease_bounce_in(.9) == d3.ease_bounce_in(0.9)

def test_bounce_4():
    bounce_out = out(d3.ease_bounce_in)
    assert d3.ease_bounce_out(0.0) == bounce_out(0.0)
    assert in_delta(d3.ease_bounce_out(0.1), bounce_out(0.1))
    assert in_delta(d3.ease_bounce_out(0.2), bounce_out(0.2))
    assert in_delta(d3.ease_bounce_out(0.3), bounce_out(0.3))
    assert in_delta(d3.ease_bounce_out(0.4), bounce_out(0.4))
    assert in_delta(d3.ease_bounce_out(0.5), bounce_out(0.5))
    assert in_delta(d3.ease_bounce_out(0.6), bounce_out(0.6))
    assert in_delta(d3.ease_bounce_out(0.7), bounce_out(0.7))
    assert in_delta(d3.ease_bounce_out(0.8), bounce_out(0.8))
    assert in_delta(d3.ease_bounce_out(0.9), bounce_out(0.9))
    assert d3.ease_bounce_out(1.0) == bounce_out(1.0)

def test_bounce_5():
    assert d3.ease_bounce_out(.9) == d3.ease_bounce_out(0.9)

def test_bounce_6():
    bounce_in_out = in_out(d3.ease_bounce_in)
    assert d3.ease_bounce_in_out(0.0) == bounce_in_out(0.0)
    assert in_delta(d3.ease_bounce_in_out(0.1), bounce_in_out(0.1))
    assert in_delta(d3.ease_bounce_in_out(0.2), bounce_in_out(0.2))
    assert in_delta(d3.ease_bounce_in_out(0.3), bounce_in_out(0.3))
    assert in_delta(d3.ease_bounce_in_out(0.4), bounce_in_out(0.4))
    assert in_delta(d3.ease_bounce_in_out(0.5), bounce_in_out(0.5))
    assert in_delta(d3.ease_bounce_in_out(0.6), bounce_in_out(0.6))
    assert in_delta(d3.ease_bounce_in_out(0.7), bounce_in_out(0.7))
    assert in_delta(d3.ease_bounce_in_out(0.8), bounce_in_out(0.8))
    assert in_delta(d3.ease_bounce_in_out(0.9), bounce_in_out(0.9))
    assert d3.ease_bounce_in_out(1.0) == bounce_in_out(1.0)

def test_bounce_7():
    assert d3.ease_bounce_in_out(.9) == d3.ease_bounce_in_out(0.9)
