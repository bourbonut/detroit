import detroit as d3

def test_round_1():
    i = d3.interpolate_round(10, 42)
    assert i(0.0) == 10
    assert i(0.1) == 13
    assert i(0.2) == 16
    assert i(0.3) == 20
    assert i(0.4) == 23
    assert i(0.5) == 26
    assert i(0.6) == 29
    assert i(0.7) == 32
    assert i(0.8) == 36
    assert i(0.9) == 39
    assert i(1.0) == 42

def test_round_2():
    i = d3.interpolate_round(2.6, 3.6)
    assert i(0.6) == 3

def test_round_3():
    a = 2e+42
    b = 335
    assert d3.interpolate_round(a, b)(1) == b
    assert d3.interpolate_round(a, b)(0) == a
