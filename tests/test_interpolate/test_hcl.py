import math

import detroit as d3


def test_hcl_1():
    assert d3.interpolate_hcl("steelblue", "brown")(0) == str(d3.rgb("steelblue"))
    assert d3.interpolate_hcl("steelblue", d3.hcl("brown"))(1) == str(d3.rgb("brown"))
    assert d3.interpolate_hcl("steelblue", d3.rgb("brown"))(1) == str(d3.rgb("brown"))


def test_hcl_2():
    assert d3.interpolate_hcl("steelblue", "#f00")(0.2) == "rgb(106, 121, 206)"
    assert (
        d3.interpolate_hcl("rgba(70, 130, 180, 1)", "rgba(255, 0, 0, 0.2)")(0.2)
        == "rgba(106, 121, 206, 0.84)"
    )


def test_hcl_3():
    i = d3.interpolate_hcl(d3.hcl(10, 50, 50), d3.hcl(350, 50, 50))
    assert i(0.0) == "rgb(194, 78, 107)"
    assert i(0.2) == "rgb(194, 78, 113)"
    assert i(0.4) == "rgb(193, 78, 118)"
    assert i(0.6) == "rgb(192, 78, 124)"
    assert i(0.8) == "rgb(191, 78, 130)"
    assert i(1.0) == "rgb(189, 79, 136)"


def test_hcl_4():
    i = d3.interpolate_hcl(d3.hcl(10, 50, 50), d3.hcl(380, 50, 50))
    assert i(0.0) == "rgb(194, 78, 107)"
    assert i(0.2) == "rgb(194, 78, 104)"
    assert i(0.4) == "rgb(194, 79, 101)"
    assert i(0.6) == "rgb(194, 79, 98)"
    assert i(0.8) == "rgb(194, 80, 96)"
    assert i(1.0) == "rgb(194, 80, 93)"


def test_hcl_5():
    i = d3.interpolate_hcl(d3.hcl(10, 50, 50), d3.hcl(710, 50, 50))
    assert i(0.0) == "rgb(194, 78, 107)"
    assert i(0.2) == "rgb(194, 78, 113)"
    assert i(0.4) == "rgb(193, 78, 118)"
    assert i(0.6) == "rgb(192, 78, 124)"
    assert i(0.8) == "rgb(191, 78, 130)"
    assert i(1.0) == "rgb(189, 79, 136)"


def test_hcl_6():
    i = d3.interpolate_hcl(d3.hcl(10, 50, 50), d3.hcl(740, 50, 50))
    assert i(0.0) == "rgb(194, 78, 107)"
    assert i(0.2) == "rgb(194, 78, 104)"
    assert i(0.4) == "rgb(194, 79, 101)"
    assert i(0.6) == "rgb(194, 79, 98)"
    assert i(0.8) == "rgb(194, 80, 96)"
    assert i(1.0) == "rgb(194, 80, 93)"


def test_hcl_7():
    assert (
        d3.interpolate_hcl("#f60", d3.hcl(math.nan, math.nan, 0))(0.5)
        == "rgb(155, 0, 0)"
    )
    assert (
        d3.interpolate_hcl("#6f0", d3.hcl(math.nan, math.nan, 0))(0.5)
        == "rgb(0, 129, 0)"
    )


def test_hcl_8():
    assert (
        d3.interpolate_hcl(d3.hcl(math.nan, math.nan, 0), "#f60")(0.5)
        == "rgb(155, 0, 0)"
    )
    assert (
        d3.interpolate_hcl(d3.hcl(math.nan, math.nan, 0), "#6f0")(0.5)
        == "rgb(0, 129, 0)"
    )


def test_hcl_9():
    assert (
        d3.interpolate_hcl("#ccc", d3.hcl(math.nan, math.nan, 0))(0.5)
        == "rgb(97, 97, 97)"
    )
    assert (
        d3.interpolate_hcl("#f00", d3.hcl(math.nan, math.nan, 0))(0.5)
        == "rgb(166, 0, 0)"
    )


def test_hcl_10():
    assert (
        d3.interpolate_hcl(d3.hcl(math.nan, math.nan, 0), "#ccc")(0.5)
        == "rgb(97, 97, 97)"
    )
    assert (
        d3.interpolate_hcl(d3.hcl(math.nan, math.nan, 0), "#f00")(0.5)
        == "rgb(166, 0, 0)"
    )
