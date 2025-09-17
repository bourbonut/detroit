import detroit as d3
from .generic import out, in_out

def in_delta(actual, expected):
    return expected - 1e-6 < actual and actual < expected + 1e-6

def test_poly_1():
    assert d3.ease_poly == d3.ease_poly_in_out

def test_poly_2():
    assert d3.ease_poly_in(0.0) == 0.000
    assert in_delta(d3.ease_poly_in(0.1), 0.001)
    assert in_delta(d3.ease_poly_in(0.2), 0.008)
    assert in_delta(d3.ease_poly_in(0.3), 0.027)
    assert in_delta(d3.ease_poly_in(0.4), 0.064)
    assert in_delta(d3.ease_poly_in(0.5), 0.125)
    assert in_delta(d3.ease_poly_in(0.6), 0.216)
    assert in_delta(d3.ease_poly_in(0.7), 0.343)
    assert in_delta(d3.ease_poly_in(0.8), 0.512)
    assert in_delta(d3.ease_poly_in(0.9), 0.729)
    assert d3.ease_poly_in(1.0) == 1.000

def test_poly_3():
    assert d3.ease_poly_in(.9) == d3.ease_poly_in(0.9)

def test_poly_4():
    assert d3.ease_poly_in(0.1) == d3.ease_poly_in.exponent(3)(0.1)
    assert d3.ease_poly_in(0.2) == d3.ease_poly_in.exponent(3)(0.2)
    assert d3.ease_poly_in(0.3) == d3.ease_poly_in.exponent(3)(0.3)

def test_poly_5():
    assert d3.ease_poly_in.exponent(1.3)(.9) == d3.ease_poly_in.exponent(1.3)(0.9)

def test_poly_6():
    assert d3.ease_poly_in.exponent(2.5)(0.0) == 0.000000
    assert in_delta(d3.ease_poly_in.exponent(2.5)(0.1), 0.003162)
    assert in_delta(d3.ease_poly_in.exponent(2.5)(0.2), 0.017889)
    assert in_delta(d3.ease_poly_in.exponent(2.5)(0.3), 0.049295)
    assert in_delta(d3.ease_poly_in.exponent(2.5)(0.4), 0.101193)
    assert in_delta(d3.ease_poly_in.exponent(2.5)(0.5), 0.176777)
    assert in_delta(d3.ease_poly_in.exponent(2.5)(0.6), 0.278855)
    assert in_delta(d3.ease_poly_in.exponent(2.5)(0.7), 0.409963)
    assert in_delta(d3.ease_poly_in.exponent(2.5)(0.8), 0.572433)
    assert in_delta(d3.ease_poly_in.exponent(2.5)(0.9), 0.768433)
    assert d3.ease_poly_in.exponent(2.5)(1.0) == 1.000000

def test_poly_7():
    assert d3.ease_poly_out.exponent(1.3)(.9) == d3.ease_poly_out.exponent(1.3)(0.9)

def test_poly_8():
    assert d3.ease_poly_out(0.1) == d3.ease_poly_out.exponent(3)(0.1)
    assert d3.ease_poly_out(0.2) == d3.ease_poly_out.exponent(3)(0.2)
    assert d3.ease_poly_out(0.3) == d3.ease_poly_out.exponent(3)(0.3)

def test_poly_9():
    assert d3.ease_poly_out(0.1) == d3.ease_poly_out.exponent(3)(0.1)
    assert d3.ease_poly_out(0.2) == d3.ease_poly_out.exponent(3)(0.2)
    assert d3.ease_poly_out(0.3) == d3.ease_poly_out.exponent(3)(0.3)

def test_poly_10():
    assert d3.ease_poly_out(0.1) == d3.ease_poly_out.exponent(3)(0.1)
    assert d3.ease_poly_out(0.2) == d3.ease_poly_out.exponent(3)(0.2)
    assert d3.ease_poly_out(0.3) == d3.ease_poly_out.exponent(3)(0.3)

def test_poly_11():
    poly_out = out(d3.ease_poly_in.exponent(2.5))
    assert d3.ease_poly_out.exponent(2.5)(0.0) == poly_out(0.0)
    assert in_delta(d3.ease_poly_out.exponent(2.5)(0.1), poly_out(0.1))
    assert in_delta(d3.ease_poly_out.exponent(2.5)(0.2), poly_out(0.2))
    assert in_delta(d3.ease_poly_out.exponent(2.5)(0.3), poly_out(0.3))
    assert in_delta(d3.ease_poly_out.exponent(2.5)(0.4), poly_out(0.4))
    assert in_delta(d3.ease_poly_out.exponent(2.5)(0.5), poly_out(0.5))
    assert in_delta(d3.ease_poly_out.exponent(2.5)(0.6), poly_out(0.6))
    assert in_delta(d3.ease_poly_out.exponent(2.5)(0.7), poly_out(0.7))
    assert in_delta(d3.ease_poly_out.exponent(2.5)(0.8), poly_out(0.8))
    assert in_delta(d3.ease_poly_out.exponent(2.5)(0.9), poly_out(0.9))
    assert d3.ease_poly_out.exponent(2.5)(1.0) == poly_out(1.0)

def test_poly_12():
    assert d3.ease_poly_in_out.exponent(1.3)(.9) == d3.ease_poly_in_out.exponent(1.3)(0.9)

def test_poly_13():
    assert d3.ease_poly_in_out(0.1) == d3.ease_poly_in_out.exponent(3)(0.1)
    assert d3.ease_poly_in_out(0.2) == d3.ease_poly_in_out.exponent(3)(0.2)
    assert d3.ease_poly_in_out(0.3) == d3.ease_poly_in_out.exponent(3)(0.3)

def test_poly_14():
    poly_in_out = in_out(d3.ease_poly_in.exponent(2.5))
    assert in_delta(d3.ease_poly_in_out.exponent(2.5)(0.0), poly_in_out(0.0))
    assert in_delta(d3.ease_poly_in_out.exponent(2.5)(0.1), poly_in_out(0.1))
    assert in_delta(d3.ease_poly_in_out.exponent(2.5)(0.2), poly_in_out(0.2))
    assert in_delta(d3.ease_poly_in_out.exponent(2.5)(0.3), poly_in_out(0.3))
    assert in_delta(d3.ease_poly_in_out.exponent(2.5)(0.4), poly_in_out(0.4))
    assert in_delta(d3.ease_poly_in_out.exponent(2.5)(0.5), poly_in_out(0.5))
    assert in_delta(d3.ease_poly_in_out.exponent(2.5)(0.6), poly_in_out(0.6))
    assert in_delta(d3.ease_poly_in_out.exponent(2.5)(0.7), poly_in_out(0.7))
    assert in_delta(d3.ease_poly_in_out.exponent(2.5)(0.8), poly_in_out(0.8))
    assert in_delta(d3.ease_poly_in_out.exponent(2.5)(0.9), poly_in_out(0.9))
    assert in_delta(d3.ease_poly_in_out.exponent(2.5)(1.0), poly_in_out(1.0))
