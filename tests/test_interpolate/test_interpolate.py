import detroit as d3
from datetime import datetime
import math
import pytest


def test_value_1():
    assert d3.interpolate("foo", "bar")(0.5) == "bar"


def test_value_2():
    assert d3.interpolate("1", "2")(0.5) == "1.5"
    assert d3.interpolate(" 1", " 2")(0.5) == " 1.5"


def test_value_3():
    assert d3.interpolate("red", "blue")(0.5) == "rgb(128, 0, 128)"
    assert d3.interpolate("#ff0000", "#0000ff")(0.5) == "rgb(128, 0, 128)"
    assert d3.interpolate("#f00", "#00f")(0.5) == "rgb(128, 0, 128)"
    assert d3.interpolate("rgb(255, 0, 0)", "rgb(0, 0, 255)")(0.5) == "rgb(128, 0, 128)"
    assert (
        d3.interpolate("rgba(255, 0, 0, 1.0)", "rgba(0, 0, 255, 1.0)")(0.5)
        == "rgb(128, 0, 128)"
    )
    assert (
        d3.interpolate("rgb(100%, 0%, 0%)", "rgb(0%, 0%, 100%)")(0.5)
        == "rgb(128, 0, 128)"
    )
    assert (
        d3.interpolate("rgba(100%, 0%, 0%, 1.0)", "rgba(0%, 0%, 100%, 1.0)")(0.5)
        == "rgb(128, 0, 128)"
    )
    assert (
        d3.interpolate("rgba(100%, 0%, 0%, 0.5)", "rgba(0%, 0%, 100%, 0.7)")(0.5)
        == "rgba(128, 0, 128, 0.6)"
    )


def test_value_4():
    assert d3.interpolate("red", d3.rgb("blue"))(0.5) == "rgb(128, 0, 128)"
    assert d3.interpolate("red", d3.hsl("blue"))(0.5) == "rgb(128, 0, 128)"


def test_value_5():
    assert d3.interpolate(["red"], ["blue"])(0.5) == ["rgb(128, 0, 128)"]


def test_value_6():
    assert d3.interpolate([1], [2])(0.5) == [1.5]


def test_value_7():
    assert d3.interpolate(1, 2)(0.5) == 1.5
    assert math.isnan(d3.interpolate(1, math.nan)(0.5))


def test_value_8():
    assert d3.interpolate({"color": "red"}, {"color": "blue"})(0.5) == {
        "color": "rgb(128, 0, 128)"
    }


def test_value_9():
    assert d3.interpolate(1, 2)(0.5) == 1.5
    assert d3.interpolate(1, "2")(0.5) == "1.5"


def test_value_10():
    i = d3.interpolate(datetime(2000, 1, 1), datetime(2000, 1, 2))
    d = i(0.5)
    assert isinstance(d, datetime)
    assert i(0.5) == datetime(2000, 1, 1, 12)


def test_value_11():
    assert d3.interpolate(0, None)(0.5) is None
    assert d3.interpolate(0, None)(0.5) is None
    assert d3.interpolate(0, True)(0.5) is True
    assert d3.interpolate(0, False)(0.5) is False


def test_value_12():
    assert d3.interpolate([0, 0], [-1, 1])(0.5) == [-0.5, 0.5]
    assert isinstance(d3.interpolate([0, 0], [-1, 1])(0.5), list)
    assert d3.interpolate([0, 0], [-1, 1])(0.5) == [-0.5, 0.5]
    assert isinstance(d3.interpolate([0, 0], [-1, 1])(0.5), list)
    assert d3.interpolate([0, 0], [-2, 2])(0.5) == [-1, 1]
    assert isinstance(d3.interpolate([0, 0], [-1, 1])(0.5), list)
    assert d3.interpolate([0, 0], [-2, 2])(0.5) == [-1, 1]
    assert isinstance(d3.interpolate([0, 0], [-1, 1])(0.5), list)
