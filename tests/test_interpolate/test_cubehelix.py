import detroit as d3
import math


def test_cubehelix_1():
    assert d3.interpolate_cubehelix("steelblue", "brown")(0) == str(d3.rgb("steelblue"))
    assert d3.interpolate_cubehelix("steelblue", d3.hcl("brown"))(1) == str(
        d3.rgb("brown")
    )
    assert d3.interpolate_cubehelix("steelblue", d3.rgb("brown"))(1) == str(
        d3.rgb("brown")
    )


def test_cubehelix_2():
    assert d3.interpolate_cubehelix("steelblue", "#f00")(0.2) == "rgb(88, 100, 218)"
    assert (
        d3.interpolate_cubehelix("rgba(70, 130, 180, 1)", "rgba(255, 0, 0, 0.2)")(0.2)
        == "rgba(88, 100, 218, 0.84)"
    )


def test_cubehelix_3():
    assert (
        d3.interpolate_cubehelix.set_gamma(3)("steelblue", "#f00")(0.2)
        == "rgb(96, 107, 228)"
    )


def test_cubehelix_4():
    i0 = d3.interpolate_cubehelix.set_gamma(1)("purple", "orange")
    i1 = d3.interpolate_cubehelix("purple", "orange")
    assert i1(0.0) == i0(0.0)
    assert i1(0.2) == i0(0.2)
    assert i1(0.4) == i0(0.4)
    assert i1(0.6) == i0(0.6)
    assert i1(0.8) == i0(0.8)
    assert i1(1.0) == i0(1.0)


def test_cubehelix_5():
    i = d3.interpolate_cubehelix("purple", "orange")
    assert i(0.0) == "rgb(128, 0, 128)"
    assert i(0.2) == "rgb(208, 1, 127)"
    assert i(0.4) == "rgb(255, 17, 93)"
    assert i(0.6) == "rgb(255, 52, 43)"
    assert i(0.8) == "rgb(255, 105, 5)"
    assert i(1.0) == "rgb(255, 165, 0)"


def test_cubehelix_6():
    assert (
        d3.interpolate_cubehelix("#f60", d3.cubehelix(math.nan, math.nan, 0))(0.5)
        == "rgb(162, 41, 0)"
    )
    assert (
        d3.interpolate_cubehelix("#6f0", d3.cubehelix(math.nan, math.nan, 0))(0.5)
        == "rgb(3, 173, 0)"
    )


def test_cubehelix_7():
    assert (
        d3.interpolate_cubehelix(d3.cubehelix(math.nan, math.nan, 0), "#f60")(0.5)
        == "rgb(162, 41, 0)"
    )
    assert (
        d3.interpolate_cubehelix(d3.cubehelix(math.nan, math.nan, 0), "#6f0")(0.5)
        == "rgb(3, 173, 0)"
    )


def test_cubehelix_8():
    assert (
        d3.interpolate_cubehelix("#ccc", d3.cubehelix(math.nan, math.nan, 0))(0.5)
        == "rgb(102, 102, 102)"
    )
    assert (
        d3.interpolate_cubehelix("#f00", d3.cubehelix(math.nan, math.nan, 0))(0.5)
        == "rgb(147, 0, 0)"
    )


def test_cubehelix_9():
    assert (
        d3.interpolate_cubehelix(d3.cubehelix(math.nan, math.nan, 0), "#ccc")(0.5)
        == "rgb(102, 102, 102)"
    )
    assert (
        d3.interpolate_cubehelix(d3.cubehelix(math.nan, math.nan, 0), "#f00")(0.5)
        == "rgb(147, 0, 0)"
    )
