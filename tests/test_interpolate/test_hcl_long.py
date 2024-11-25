import math

import detroit as d3


def test_hcl_long_1():
    assert d3.interpolate_hcl_long("steelblue", "brown")(0) == str(d3.rgb("steelblue"))
    assert d3.interpolate_hcl_long("steelblue", d3.hcl("brown"))(1) == str(
        d3.rgb("brown")
    )
    assert d3.interpolate_hcl_long("steelblue", d3.rgb("brown"))(1) == str(
        d3.rgb("brown")
    )


def test_hcl_long_2():
    assert d3.interpolate_hcl_long("steelblue", "#f00")(0.2) == "rgb(0, 144, 169)"
    assert (
        d3.interpolate_hcl_long("rgba(70, 130, 180, 1)", "rgba(255, 0, 0, 0.2)")(0.2)
        == "rgba(0, 144, 169, 0.84)"
    )


def test_hcl_long_3():
    i = d3.interpolate_hcl_long(d3.hcl(10, 50, 50), d3.hcl(350, 50, 50))
    assert i(0.0) == "rgb(194, 78, 107)"
    assert i(0.2) == "rgb(151, 111, 28)"
    assert i(0.4) == "rgb(35, 136, 68)"
    assert i(0.6) == "rgb(0, 138, 165)"
    assert i(0.8) == "rgb(91, 116, 203)"
    assert i(1.0) == "rgb(189, 79, 136)"


def test_hcl_long_4():
    assert (
        d3.interpolate_hcl_long("#f60", d3.hcl(math.nan, math.nan, 0))(0.5)
        == "rgb(155, 0, 0)"
    )
    assert (
        d3.interpolate_hcl_long("#6f0", d3.hcl(math.nan, math.nan, 0))(0.5)
        == "rgb(0, 129, 0)"
    )


def test_hcl_long_5():
    assert (
        d3.interpolate_hcl_long(d3.hcl(math.nan, math.nan, 0), "#f60")(0.5)
        == "rgb(155, 0, 0)"
    )
    assert (
        d3.interpolate_hcl_long(d3.hcl(math.nan, math.nan, 0), "#6f0")(0.5)
        == "rgb(0, 129, 0)"
    )


def test_hcl_long_6():
    assert (
        d3.interpolate_hcl_long("#ccc", d3.hcl(math.nan, math.nan, 0))(0.5)
        == "rgb(97, 97, 97)"
    )
    assert (
        d3.interpolate_hcl_long("#f00", d3.hcl(math.nan, math.nan, 0))(0.5)
        == "rgb(166, 0, 0)"
    )


def test_hcl_long_7():
    assert (
        d3.interpolate_hcl_long(d3.hcl(math.nan, math.nan, 0), "#ccc")(0.5)
        == "rgb(97, 97, 97)"
    )
    assert (
        d3.interpolate_hcl_long(d3.hcl(math.nan, math.nan, 0), "#f00")(0.5)
        == "rgb(166, 0, 0)"
    )
