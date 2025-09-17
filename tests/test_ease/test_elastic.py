import detroit as d3
from .generic import out, in_out

def in_delta(actual, expected):
    return expected - 1e-6 < actual and actual < expected + 1e-6

def test_elastic_1():
    assert d3.ease_elastic == d3.ease_elastic_out

def test_elastic_2():
    assert abs(d3.ease_elastic_in(0.0)) == 0.000000
    assert in_delta(d3.ease_elastic_in(0.1),    0.000978)
    assert in_delta(d3.ease_elastic_in(0.2), -0.001466)
    assert in_delta(d3.ease_elastic_in(0.3), -0.003421)
    assert in_delta(d3.ease_elastic_in(0.4),    0.014663)
    assert in_delta(d3.ease_elastic_in(0.5), -0.015152)
    assert in_delta(d3.ease_elastic_in(0.6), -0.030792)
    assert in_delta(d3.ease_elastic_in(0.7),    0.124145)
    assert in_delta(d3.ease_elastic_in(0.8), -0.124633)
    assert in_delta(d3.ease_elastic_in(0.9), -0.249756)
    assert d3.ease_elastic_in(1.0) ==    1.000000

def test_elastic_3():
    assert d3.ease_elastic_in(.9) == d3.ease_elastic_in(0.9)

def test_elastic_4():
    assert d3.ease_elastic_in(0.1) == d3.ease_elastic_in.amplitude(1).period(0.3)(0.1)
    assert d3.ease_elastic_in(0.2) == d3.ease_elastic_in.amplitude(1).period(0.3)(0.2)
    assert d3.ease_elastic_in(0.3) == d3.ease_elastic_in.amplitude(1).period(0.3)(0.3)

def test_elastic_5():
    assert d3.ease_elastic_in.amplitude(-1.0)(0.1) == d3.ease_elastic_in(0.1)
    assert d3.ease_elastic_in.amplitude(+0.4)(0.2) == d3.ease_elastic_in(0.2)
    assert d3.ease_elastic_in.amplitude(+0.8)(0.3) == d3.ease_elastic_in(0.3)

def test_elastic_6():
    assert d3.ease_elastic_in.amplitude(1.3).period(0.2)(.9) == d3.ease_elastic_in.amplitude(1.3).period(0.2)(.9)

def test_elastic_7():
    assert d3.ease_elastic_in.amplitude(1.3)(0.0) ==    0.000000
    assert in_delta(d3.ease_elastic_in.amplitude(1.3)(0.1),    0.000978)
    assert in_delta(d3.ease_elastic_in.amplitude(1.3)(0.2), -0.003576)
    assert in_delta(d3.ease_elastic_in.amplitude(1.3)(0.3),    0.001501)
    assert in_delta(d3.ease_elastic_in.amplitude(1.3)(0.4),    0.014663)
    assert in_delta(d3.ease_elastic_in.amplitude(1.3)(0.5), -0.036951)
    assert in_delta(d3.ease_elastic_in.amplitude(1.3)(0.6),    0.013510)
    assert in_delta(d3.ease_elastic_in.amplitude(1.3)(0.7),    0.124145)
    assert in_delta(d3.ease_elastic_in.amplitude(1.3)(0.8), -0.303950)
    assert in_delta(d3.ease_elastic_in.amplitude(1.3)(0.9),    0.109580)
    assert d3.ease_elastic_in.amplitude(1.3)(1.0) ==    1.000000

def test_elastic_8():
    assert d3.ease_elastic_in.amplitude(1.5).period(1)(0.0) ==    0.000000
    assert in_delta(d3.ease_elastic_in.amplitude(1.5).period(1)(0.1),    0.000148)
    assert in_delta(d3.ease_elastic_in.amplitude(1.5).period(1)(0.2), -0.002212)
    assert in_delta(d3.ease_elastic_in.amplitude(1.5).period(1)(0.3), -0.009390)
    assert in_delta(d3.ease_elastic_in.amplitude(1.5).period(1)(0.4), -0.021498)
    assert in_delta(d3.ease_elastic_in.amplitude(1.5).period(1)(0.5), -0.030303)
    assert in_delta(d3.ease_elastic_in.amplitude(1.5).period(1)(0.6), -0.009352)
    assert in_delta(d3.ease_elastic_in.amplitude(1.5).period(1)(0.7),    0.093642)
    assert in_delta(d3.ease_elastic_in.amplitude(1.5).period(1)(0.8),    0.342077)
    assert in_delta(d3.ease_elastic_in.amplitude(1.5).period(1)(0.9),    0.732374)
    assert d3.ease_elastic_in.amplitude(1.5).period(1)(1.0) ==    1.000000

def test_elastic_9():
    elastic_out = out(d3.ease_elastic_in)
    assert d3.ease_elastic_out(0.0) == elastic_out(0.0)
    assert in_delta(d3.ease_elastic_out(0.1), elastic_out(0.1))
    assert in_delta(d3.ease_elastic_out(0.2), elastic_out(0.2))
    assert in_delta(d3.ease_elastic_out(0.3), elastic_out(0.3))
    assert in_delta(d3.ease_elastic_out(0.4), elastic_out(0.4))
    assert in_delta(d3.ease_elastic_out(0.5), elastic_out(0.5))
    assert in_delta(d3.ease_elastic_out(0.6), elastic_out(0.6))
    assert in_delta(d3.ease_elastic_out(0.7), elastic_out(0.7))
    assert in_delta(d3.ease_elastic_out(0.8), elastic_out(0.8))
    assert in_delta(d3.ease_elastic_out(0.9), elastic_out(0.9))
    assert d3.ease_elastic_out(1.0) == elastic_out(1.0)

def test_elastic_10():
    assert d3.ease_elastic_out.amplitude(1.3).period(0.2)(.9) == d3.ease_elastic_out.amplitude(1.3).period(0.2)(.9)

def test_elastic_11():
    elastic_in_out = in_out(d3.ease_elastic_in)
    assert d3.ease_elastic_in_out(0.0) == elastic_in_out(0.0)
    assert in_delta(d3.ease_elastic_in_out(0.1), elastic_in_out(0.1))
    assert in_delta(d3.ease_elastic_in_out(0.2), elastic_in_out(0.2))
    assert in_delta(d3.ease_elastic_in_out(0.3), elastic_in_out(0.3))
    assert in_delta(d3.ease_elastic_in_out(0.4), elastic_in_out(0.4))
    assert in_delta(d3.ease_elastic_in_out(0.5), elastic_in_out(0.5))
    assert in_delta(d3.ease_elastic_in_out(0.6), elastic_in_out(0.6))
    assert in_delta(d3.ease_elastic_in_out(0.7), elastic_in_out(0.7))
    assert in_delta(d3.ease_elastic_in_out(0.8), elastic_in_out(0.8))
    assert in_delta(d3.ease_elastic_in_out(0.9), elastic_in_out(0.9))
    assert d3.ease_elastic_in_out(1.0) == elastic_in_out(1.0)

def test_elastic_12():
    assert d3.ease_elastic_in_out.amplitude(1.3).period(0.2)(.9) == d3.ease_elastic_in_out.amplitude(1.3).period(0.2)(.9)
