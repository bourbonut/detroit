import detroit as d3
from detroit.interpolate.piecewise import piecewise


def test_piecewise_1():
    i = piecewise(d3.interpolate, [0, 2, 10])
    assert i(-1) == -4
    assert i(0) == 0
    assert i(0.19) == 0.76
    assert i(0.21) == 0.84
    assert i(0.5) == 2
    assert i(0.75) == 6
    assert i(1) == 10


def test_piecewise_2():
    i = piecewise([0, 2, 10])
    assert i(-1) == -4
    assert i(0) == 0
    assert i(0.19) == 0.76
    assert i(0.21) == 0.84
    assert i(0.5) == 2
    assert i(0.75) == 6
    assert i(1) == 10


def test_piecewise_3():
    i = piecewise(["a0", "a2", "a10"])
    assert i(-1) == "a-4"
    assert i(0) == "a0"
    assert i(0.19) == "a0.76"
    assert i(0.21) == "a0.84"
    assert i(0.5) == "a2"
    assert i(0.75) == "a6"
    assert i(1) == "a10"
