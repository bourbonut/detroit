import detroit as d3
import math
import pytest


def test_tick_increment_none():
    with pytest.raises(ValueError):
        assert math.isnan(d3.tick_increment(math.nan, 1, 1))
    with pytest.raises(ValueError):
        assert math.isnan(d3.tick_increment(0, math.nan, 1))
    with pytest.raises(ZeroDivisionError):
        assert math.isnan(d3.tick_increment(0, 1, math.nan))
    with pytest.raises(ValueError):
        assert math.isnan(d3.tick_increment(math.nan, math.nan, 1))
    with pytest.raises(ZeroDivisionError):
        assert math.isnan(d3.tick_increment(0, math.nan, math.nan))
    with pytest.raises(ZeroDivisionError):
        assert math.isnan(d3.tick_increment(math.nan, 1, math.nan))
    with pytest.raises(ZeroDivisionError):
        assert math.isnan(d3.tick_increment(math.nan, math.nan, math.nan))
    with pytest.raises(ZeroDivisionError):
        assert math.isnan(d3.tick_increment(1, 1, -1))
    with pytest.raises(ZeroDivisionError):
        assert math.isnan(d3.tick_increment(1, 1, 0))
    with pytest.raises(ZeroDivisionError):
        assert math.isnan(d3.tick_increment(1, 1, math.nan))


def test_tick_increment_infinity():
    with pytest.raises(ValueError):
        assert d3.tick_increment(1, 1, 1) == -math.inf
    with pytest.raises(ValueError):
        assert d3.tick_increment(1, 1, 10) == -math.inf
    with pytest.raises(ZeroDivisionError):
        assert d3.tick_increment(0, 1, -1) == math.inf
    with pytest.raises(ZeroDivisionError):
        assert d3.tick_increment(0, 1, 0) == math.inf
    with pytest.raises(ValueError):
        assert d3.tick_increment(0, 1, math.inf) == -math.inf


def test_tick_increment():
    assert d3.tick_increment(0, 1, 10) == -10
    assert d3.tick_increment(0, 1, 9) == -10
    assert d3.tick_increment(0, 1, 8) == -10
    assert d3.tick_increment(0, 1, 7) == -5
    assert d3.tick_increment(0, 1, 6) == -5
    assert d3.tick_increment(0, 1, 5) == -5
    assert d3.tick_increment(0, 1, 4) == -5
    assert d3.tick_increment(0, 1, 3) == -2
    assert d3.tick_increment(0, 1, 2) == -2
    assert d3.tick_increment(0, 1, 1) == 1
    assert d3.tick_increment(0, 10, 10) == 1
    assert d3.tick_increment(0, 10, 9) == 1
    assert d3.tick_increment(0, 10, 8) == 1
    assert d3.tick_increment(0, 10, 7) == 2
    assert d3.tick_increment(0, 10, 6) == 2
    assert d3.tick_increment(0, 10, 5) == 2
    assert d3.tick_increment(0, 10, 4) == 2
    assert d3.tick_increment(0, 10, 3) == 5
    assert d3.tick_increment(0, 10, 2) == 5
    assert d3.tick_increment(0, 10, 1) == 10
    assert d3.tick_increment(-10, 10, 10) == 2
    assert d3.tick_increment(-10, 10, 9) == 2
    assert d3.tick_increment(-10, 10, 8) == 2
    assert d3.tick_increment(-10, 10, 7) == 2
    assert d3.tick_increment(-10, 10, 6) == 5
    assert d3.tick_increment(-10, 10, 5) == 5
    assert d3.tick_increment(-10, 10, 4) == 5
    assert d3.tick_increment(-10, 10, 3) == 5
    assert d3.tick_increment(-10, 10, 2) == 10
    assert d3.tick_increment(-10, 10, 1) == 20
