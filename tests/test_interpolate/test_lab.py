import detroit as d3
import math


def test_lab_1():
    assert d3.interpolate_lab("steelblue", "brown")(0) == str(d3.rgb("steelblue"))
    assert d3.interpolate_lab("steelblue", d3.hsl("brown"))(1) == str(d3.rgb("brown"))
    assert d3.interpolate_lab("steelblue", d3.rgb("brown"))(1) == str(d3.rgb("brown"))


def test_lab_2():
    assert d3.interpolate_lab("steelblue", "#f00")(0.2) == "rgb(134, 120, 146)"
    assert (
        d3.interpolate_lab("rgba(70, 130, 180, 1)", "rgba(255, 0, 0, 0.2)")(0.2)
        == "rgba(134, 120, 146, 0.84)"
    )


def test_lab_3():
    assert d3.interpolate_lab(d3.lab(math.nan, 20, 40), d3.lab(60, 80, 100))(
        0.5
    ) == str(d3.lab(60, 50, 70))
    assert d3.interpolate_lab(d3.lab(20, math.nan, 40), d3.lab(60, 80, 100))(
        0.5
    ) == str(d3.lab(40, 80, 70))
    assert d3.interpolate_lab(d3.lab(20, 40, math.nan), d3.lab(60, 80, 100))(
        0.5
    ) == str(d3.lab(40, 60, 100))


def test_lab_4():
    assert d3.interpolate_lab(d3.lab(60, 80, 100), d3.lab(math.nan, 20, 40))(
        0.5
    ) == str(d3.lab(60, 50, 70))
    assert d3.interpolate_lab(d3.lab(60, 80, 100), d3.lab(20, math.nan, 40))(
        0.5
    ) == str(d3.lab(40, 80, 70))
    assert d3.interpolate_lab(d3.lab(60, 80, 100), d3.lab(20, 40, math.nan))(
        0.5
    ) == str(d3.lab(40, 60, 100))
