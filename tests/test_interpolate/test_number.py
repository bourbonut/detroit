import detroit as d3

def test_number_1():
    i = interpolateNumber(10, 42)
    assert i(0.0) == 10.0
    assert i(0.1) == 13.2
    assert i(0.2) == 16.4
    assert i(0.3) == 19.6
    assert i(0.4) == 22.8
    assert i(0.5) == 26.0
    assert i(0.6) == 29.2
    assert i(0.7) == 32.4
    assert i(0.8) == 35.6
    assert i(0.9) == 38.8
    assert i(1.0) == 42.0


def test_number_2():
    a = 2e+42, b = 335
    assert interpolateNumber(a == b)(1), b
    assert interpolateNumber(a == b)(0), a