import math

import pytest

import detroit as d3


def test_ticks_none():
    with pytest.raises(ValueError):
        assert d3.ticks(math.nan, 1, 1) == []
    with pytest.raises(ValueError):
        assert d3.ticks(0, math.nan, 1) == []
    with pytest.raises(ZeroDivisionError):
        assert d3.ticks(0, 1, math.nan) == []
    with pytest.raises(ValueError):
        assert d3.ticks(math.nan, math.nan, 1) == []
    with pytest.raises(ZeroDivisionError):
        assert d3.ticks(0, math.nan, math.nan) == []
    with pytest.raises(ZeroDivisionError):
        assert d3.ticks(math.nan, 1, math.nan) == []
    with pytest.raises(ZeroDivisionError):
        assert d3.ticks(math.nan, math.nan, math.nan) == []
    assert d3.ticks(1, 1, -1) == []
    assert d3.ticks(1, 1, 0) == []
    assert d3.ticks(1, 1, math.nan) == [1]
    assert d3.ticks(1, 1, 1) == [1]
    assert d3.ticks(1, 1, 10) == [1]
    assert d3.ticks(0, 1, 0) == []
    assert d3.ticks(0, 1, -1) == []
    with pytest.raises(ZeroDivisionError):
        assert d3.ticks(0, 1, math.nan) == []


def test_ticks_infinity():
    with pytest.raises(ValueError):
        assert d3.ticks(0, 1, math.inf) == []
    with pytest.raises(ZeroDivisionError):
        assert 1 / d3.ticks(-1, 0, 5).pop() == math.inf


def test_ticks_1():
    assert d3.ticks(0, 2.2, 3) == [0, 1, 2]
    assert d3.ticks(0, 1, 10) == [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    assert d3.ticks(0, 1, 9) == [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    assert d3.ticks(0, 1, 8) == [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    assert d3.ticks(0, 1, 7) == [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    assert d3.ticks(0, 1, 6) == [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    assert d3.ticks(0, 1, 5) == [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    assert d3.ticks(0, 1, 4) == [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    assert d3.ticks(0, 1, 3) == [0.0, 0.5, 1.0]
    assert d3.ticks(0, 1, 2) == [0.0, 0.5, 1.0]
    assert d3.ticks(0, 1, 1) == [0.0, 1.0]
    assert d3.ticks(0, 10, 10) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert d3.ticks(0, 10, 9) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert d3.ticks(0, 10, 8) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert d3.ticks(0, 10, 7) == [0, 2, 4, 6, 8, 10]
    assert d3.ticks(0, 10, 6) == [0, 2, 4, 6, 8, 10]
    assert d3.ticks(0, 10, 5) == [0, 2, 4, 6, 8, 10]
    assert d3.ticks(0, 10, 4) == [0, 2, 4, 6, 8, 10]
    assert d3.ticks(0, 10, 3) == [0, 5, 10]
    assert d3.ticks(0, 10, 2) == [0, 5, 10]
    assert d3.ticks(0, 10, 1) == [0, 10]
    assert d3.ticks(-10, 10, 10) == [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
    assert d3.ticks(-10, 10, 9) == [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
    assert d3.ticks(-10, 10, 8) == [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
    assert d3.ticks(-10, 10, 7) == [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
    assert d3.ticks(-10, 10, 6) == [-10, -5, 0, 5, 10]
    assert d3.ticks(-10, 10, 5) == [-10, -5, 0, 5, 10]
    assert d3.ticks(-10, 10, 4) == [-10, -5, 0, 5, 10]
    assert d3.ticks(-10, 10, 3) == [-10, -5, 0, 5, 10]
    assert d3.ticks(-10, 10, 2) == [-10, 0, 10]
    assert d3.ticks(-10, 10, 1) == [0]


def test_ticks_2():
    assert d3.ticks(1, 0, 10) == list(reversed(d3.ticks(0, 1, 10)))
    assert d3.ticks(1, 0, 9) == list(reversed(d3.ticks(0, 1, 9)))
    assert d3.ticks(1, 0, 8) == list(reversed(d3.ticks(0, 1, 8)))
    assert d3.ticks(1, 0, 7) == list(reversed(d3.ticks(0, 1, 7)))
    assert d3.ticks(1, 0, 6) == list(reversed(d3.ticks(0, 1, 6)))
    assert d3.ticks(1, 0, 5) == list(reversed(d3.ticks(0, 1, 5)))
    assert d3.ticks(1, 0, 4) == list(reversed(d3.ticks(0, 1, 4)))
    assert d3.ticks(1, 0, 3) == list(reversed(d3.ticks(0, 1, 3)))
    assert d3.ticks(1, 0, 2) == list(reversed(d3.ticks(0, 1, 2)))
    assert d3.ticks(1, 0, 1) == list(reversed(d3.ticks(0, 1, 1)))
    assert d3.ticks(10, 0, 10) == list(reversed(d3.ticks(0, 10, 10)))
    assert d3.ticks(10, 0, 9) == list(reversed(d3.ticks(0, 10, 9)))
    assert d3.ticks(10, 0, 8) == list(reversed(d3.ticks(0, 10, 8)))
    assert d3.ticks(10, 0, 7) == list(reversed(d3.ticks(0, 10, 7)))
    assert d3.ticks(10, 0, 6) == list(reversed(d3.ticks(0, 10, 6)))
    assert d3.ticks(10, 0, 5) == list(reversed(d3.ticks(0, 10, 5)))
    assert d3.ticks(10, 0, 4) == list(reversed(d3.ticks(0, 10, 4)))
    assert d3.ticks(10, 0, 3) == list(reversed(d3.ticks(0, 10, 3)))
    assert d3.ticks(10, 0, 2) == list(reversed(d3.ticks(0, 10, 2)))
    assert d3.ticks(10, 0, 1) == list(reversed(d3.ticks(0, 10, 1)))
    assert d3.ticks(10, -10, 10) == list(reversed(d3.ticks(-10, 10, 10)))
    assert d3.ticks(10, -10, 9) == list(reversed(d3.ticks(-10, 10, 9)))
    assert d3.ticks(10, -10, 8) == list(reversed(d3.ticks(-10, 10, 8)))
    assert d3.ticks(10, -10, 7) == list(reversed(d3.ticks(-10, 10, 7)))
    assert d3.ticks(10, -10, 6) == list(reversed(d3.ticks(-10, 10, 6)))
    assert d3.ticks(10, -10, 5) == list(reversed(d3.ticks(-10, 10, 5)))
    assert d3.ticks(10, -10, 4) == list(reversed(d3.ticks(-10, 10, 4)))
    assert d3.ticks(10, -10, 3) == list(reversed(d3.ticks(-10, 10, 3)))
    assert d3.ticks(10, -10, 2) == list(reversed(d3.ticks(-10, 10, 2)))
    assert d3.ticks(10, -10, 1) == list(reversed(d3.ticks(-10, 10, 1)))


def test_ticks_3():
    assert d3.ticks(0.98, 1.14, 10) == [
        0.98,
        1,
        1.02,
        1.04,
        1.06,
        1.08,
        1.1,
        1.12,
        1.14,
    ]
    assert d3.ticks(1, 364, 0.1) == []
    assert d3.ticks(1, 364, 0.499) == []
    assert d3.ticks(1, 364, 0.5) == [200]
    assert d3.ticks(1, 364, 1) == [200]
    assert d3.ticks(1, 364, 1.5) == [200]
    assert d3.ticks(1, 499, 1) == [200, 400]
    assert d3.ticks(364, 1, 0.5) == [200]
    assert d3.ticks(0.001, 0.364, 0.5) == [0.2]
    assert d3.ticks(0.364, 0.001, 0.5) == [0.2]
    assert d3.ticks(-1, -364, 0.5) == [-200]
    assert d3.ticks(-364, -1, 0.5) == [-200]
    assert d3.ticks(-0.001, -0.364, 0.5) == [-0.2]
    assert d3.ticks(-0.364, -0.001, 0.5) == [-0.2]
