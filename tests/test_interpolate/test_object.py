import math

import detroit as d3


def test_object_1():
    assert d3.interpolate_object({"a": 2, "b": 12}, {"a": 4, "b": 24})(0.5) == {
        "a": 3,
        "b": 18,
    }


# @pytest.mark.skip
def test_object_2():
    assert d3.interpolate_object({"background": "red"}, {"background": "green"})(
        0.5
    ) == {"background": "rgb(128, 64, 0)"}
    assert d3.interpolate_object({"fill": "red"}, {"fill": "green"})(0.5) == {
        "fill": "rgb(128, 64, 0)"
    }
    assert d3.interpolate_object({"stroke": "red"}, {"stroke": "green"})(0.5) == {
        "stroke": "rgb(128, 64, 0)"
    }
    assert d3.interpolate_object({"color": "red"}, {"color": "green"})(0.5) == {
        "color": "rgb(128, 64, 0)"
    }


def test_object_3():
    assert d3.interpolate_object({"foo": [2, 12]}, {"foo": [4, 24]})(0.5) == {
        "foo": [3, 18]
    }
    assert d3.interpolate_object({"foo": {"bar": [2, 12]}}, {"foo": {"bar": [4, 24]}})(
        0.5
    ) == {"foo": {"bar": [3, 18]}}


def test_object_4():
    assert d3.interpolate_object({"foo": 2, "bar": 12}, {"foo": 4})(0.5) == {"foo": 3}


def test_object_5():
    assert d3.interpolate_object({"foo": 2}, {"foo": 4, "bar": 12})(0.5) == {
        "foo": 3,
        "bar": 12,
    }


def test_object_6():
    assert d3.interpolate_object(math.nan, {"foo": 2})(0.5) == {"foo": 2}
    assert d3.interpolate_object({"foo": 2}, None)(0.5) == {}
    assert d3.interpolate_object(None, {"foo": 2})(0.5) == {"foo": 2}
    assert d3.interpolate_object({"foo": 2}, None)(0.5) == {}
    assert d3.interpolate_object(None, {"foo": 2})(0.5) == {"foo": 2}
    assert d3.interpolate_object(None, math.nan)(0.5) == {}
