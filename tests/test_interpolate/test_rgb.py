import math

import detroit as d3


def test_rgb_1():
    assert d3.interpolate_rgb("steelblue", "brown")(0) == str(d3.rgb("steelblue"))
    assert d3.interpolate_rgb("steelblue", d3.hsl("brown"))(1) == str(d3.rgb("brown"))
    assert d3.interpolate_rgb("steelblue", d3.rgb("brown"))(1) == str(d3.rgb("brown"))


def test_rgb_2():
    assert d3.interpolate_rgb("steelblue", "#f00")(0.2) == "rgb(107, 104, 144)"
    assert (
        d3.interpolate_rgb("rgba(70, 130, 180, 1)", "rgba(255, 0, 0, 0.2)")(0.2)
        == "rgba(107, 104, 144, 0.84)"
    )


def test_rgb_3():
    assert d3.interpolate_rgb(d3.rgb(math.nan, 20, 40), d3.rgb(60, 80, 100))(
        0.5
    ) == str(d3.rgb(60, 50, 70))
    assert d3.interpolate_rgb(d3.rgb(20, math.nan, 40), d3.rgb(60, 80, 100))(
        0.5
    ) == str(d3.rgb(40, 80, 70))
    assert d3.interpolate_rgb(d3.rgb(20, 40, math.nan), d3.rgb(60, 80, 100))(
        0.5
    ) == str(d3.rgb(40, 60, 100))


def test_rgb_4():
    assert d3.interpolate_rgb(d3.rgb(60, 80, 100), d3.rgb(math.nan, 20, 40))(
        0.5
    ) == str(d3.rgb(60, 50, 70))
    assert d3.interpolate_rgb(d3.rgb(60, 80, 100), d3.rgb(20, math.nan, 40))(
        0.5
    ) == str(d3.rgb(40, 80, 70))
    assert d3.interpolate_rgb(d3.rgb(60, 80, 100), d3.rgb(20, 40, math.nan))(
        0.5
    ) == str(d3.rgb(40, 60, 100))


def test_rgb_5():
    assert (
        d3.interpolate_rgb.set_gamma(3)("steelblue", "#f00")(0.2)
        == "rgb(153, 121, 167)"
    )


def test_rgb_6():
    assert (
        d3.interpolate_rgb.set_gamma(3)("transparent", "#f00")(0.2)
        == "rgba(255, 0, 0, 0.2)"
    )


def test_rgb_7():
    i0 = d3.interpolate_rgb.set_gamma(1)("purple", "orange")
    i1 = d3.interpolate_rgb("purple", "orange")
    assert i1(0.0) == i0(0.0)
    assert i1(0.2) == i0(0.2)
    assert i1(0.4) == i0(0.4)
    assert i1(0.6) == i0(0.6)
    assert i1(0.8) == i0(0.8)
    assert i1(1.0) == i0(1.0)
