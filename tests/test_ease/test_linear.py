import detroit as d3

def in_delta(actual, expected):
    return expected - 1e-6 < actual and actual < expected + 1e-6

def test_linear_1():
    assert d3.ease_linear(0.0) == 0.0
    assert in_delta(d3.ease_linear(0.1), 0.1)
    assert in_delta(d3.ease_linear(0.2), 0.2)
    assert in_delta(d3.ease_linear(0.3), 0.3)
    assert in_delta(d3.ease_linear(0.4), 0.4)
    assert in_delta(d3.ease_linear(0.5), 0.5)
    assert in_delta(d3.ease_linear(0.6), 0.6)
    assert in_delta(d3.ease_linear(0.7), 0.7)
    assert in_delta(d3.ease_linear(0.8), 0.8)
    assert in_delta(d3.ease_linear(0.9), 0.9)
    assert d3.ease_linear(1.0) == 1.0

def test_linear_2():
    assert d3.ease_linear(.9) == d3.ease_linear(0.9)
