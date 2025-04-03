import math

import detroit as d3
from detroit.color.color import HSL, RGB, Color


def approx_equal(actual, expected):
    r, g, b, opacity = expected
    c1 = isinstance(actual, RGB)
    c2 = math.isnan(actual.r) or round(actual.r) == round(r)
    c3 = math.isnan(actual.g) or round(actual.g) == round(g)
    c4 = math.isnan(actual.b) or round(actual.b) == round(b)
    c5 = math.isnan(actual.opacity) or round(actual.opacity) == round(opacity)
    return all((c1, c2, c3, c4, c5))


def test_rgb_1():
    c = d3.rgb(70, 130, 180)
    assert isinstance(c, Color)
    assert isinstance(c, RGB)


def test_rgb_2():
    assert approx_equal(d3.rgb("#abc"), (170, 187, 204, 1))
    assert approx_equal(d3.rgb("rgba(170, 187, 204, 0.4)"), (170, 187, 204, 0.4))


def test_rgb_3():
    assert str(d3.rgb("#abcdef")) == "rgb(171, 205, 239)"
    assert str(d3.rgb("moccasin")) == "rgb(255, 228, 181)"
    assert str(d3.rgb("hsl(60, 100%, 20%)")) == "rgb(102, 102, 0)"
    assert str(d3.rgb("rgb(12, 34, 56)")) == "rgb(12, 34, 56)"
    assert str(d3.rgb(RGB(12, 34, 56))) == "rgb(12, 34, 56)"
    assert str(d3.rgb(HSL(60, 1, 0.2))) == "rgb(102, 102, 0)"
    assert str(d3.rgb("rgba(12, 34, 56, 0.4)")) == "rgba(12, 34, 56, 0.4)"
    assert str(d3.rgb("rgba(12%, 34%, 56%, 0.4)")) == "rgba(31, 87, 143, 0.4)"
    assert str(d3.rgb("hsla(60, 100%, 20%, 0.4)")) == "rgba(102, 102, 0, 0.4)"


def test_rgb_4():
    assert d3.rgb("#abcdef").format_rgb() == "rgb(171, 205, 239)"
    assert d3.rgb("hsl(60, 100%, 20%)").format_rgb() == "rgb(102, 102, 0)"
    assert d3.rgb("rgba(12%, 34%, 56%, 0.4)").format_rgb() == "rgba(31, 87, 143, 0.4)"
    assert d3.rgb("hsla(60, 100%, 20%, 0.4)").format_rgb() == "rgba(102, 102, 0, 0.4)"


def test_rgb_5():
    assert d3.rgb("#abcdef").format_hsl() == "hsl(210, 68%, 80.3921568627451%)"
    assert d3.rgb("hsl(60, 100%, 20%)").format_hsl() == "hsl(60, 100%, 20%)"
    assert (
        d3.rgb("rgba(12%, 34%, 56%, 0.4)").format_hsl()
        == "hsla(210, 64.70588235294117%, 34%, 0.4)"
    )
    assert d3.rgb("hsla(60, 100%, 20%, 0.4)").format_hsl() == "hsla(60, 100%, 20%, 0.4)"


def test_rgb_6():
    assert d3.rgb("#abcdef").format_hex() == "#abcdef"
    assert d3.rgb("hsl(60, 100%, 20%)").format_hex() == "#666600"
    assert d3.rgb("rgba(12%, 34%, 56%, 0.4)").format_hex() == "#1f578f"
    assert d3.rgb("hsla(60, 100%, 20%, 0.4)").format_hex() == "#666600"


def test_rgb_7():
    assert d3.rgb("#abcdef").format_hex_8() == "#abcdefff"
    assert d3.rgb("hsl(60, 100%, 20%)").format_hex_8() == "#666600ff"
    assert d3.rgb("rgba(12%, 34%, 56%, 0.4)").format_hex_8() == "#1f578f66"
    assert d3.rgb("hsla(60, 100%, 20%, 0.4)").format_hex_8() == "#66660066"


def test_rgb_8():
    c = d3.rgb("#abc")
    c.r += 1
    c.g += 1
    c.b += 1
    c.opacity = 0.5
    assert str(c) == "rgba(171, 188, 205, 0.5)"


def test_rgb_9():
    assert str(d3.rgb("invalid")) == "rgb(0, 0, 0)"
    assert str(d3.rgb(math.nan, 12, 34)) == "rgb(0, 12, 34)"


def test_rgb_10():
    c = d3.rgb("#abc")
    c.r += 1
    c.g += 1
    c.b += 1
    c.opacity = math.nan
    assert str(c) == "rgb(171, 188, 205)"


def test_rgb_11():
    assert str(d3.rgb(-1, 2, 3)) == "rgb(0, 2, 3)"
    assert str(d3.rgb(2, -1, 3)) == "rgb(2, 0, 3)"
    assert str(d3.rgb(2, 3, -1)) == "rgb(2, 3, 0)"
    assert str(d3.rgb(2, 3, -1, -0.2)) == "rgba(2, 3, 0, 0)"
    assert str(d3.rgb(2, 3, -1, 1.2)) == "rgb(2, 3, 0)"


def test_rgb_12():
    assert str(d3.rgb(0.6, 2.0, 3.0)) == "rgb(1, 2, 3)"
    assert str(d3.rgb(2.0, 0.6, 3.0)) == "rgb(2, 1, 3)"
    assert str(d3.rgb(2.0, 3.0, 0.6)) == "rgb(2, 3, 1)"


def test_rgb_13():
    assert approx_equal(d3.rgb(1.2, 2.6, 42.9), (1.2, 2.6, 42.9, 1))


def test_rgb_14():
    assert approx_equal(d3.rgb(-10, -20, -30), (-10, -20, -30, 1))
    assert approx_equal(d3.rgb(300, 400, 500), (300, 400, 500, 1))


def test_rgb_15():
    assert approx_equal(d3.rgb(-10, -20, -30).clamp(), (0, 0, 0, 1))
    assert approx_equal(d3.rgb(10.6, 20.6, 30.6).clamp(), (11, 21, 31, 1))
    assert approx_equal(d3.rgb(300, 400, 500).clamp(), (255, 255, 255, 1))
    assert d3.rgb(10.5, 20.5, 30.5, -1).clamp().opacity == 0
    assert d3.rgb(10.5, 20.5, 30.5, 0.5).clamp().opacity == 0.5
    assert d3.rgb(10.5, 20.5, 30.5, 2).clamp().opacity == 1
    assert d3.rgb(10.5, 20.5, 30.5, math.nan).clamp().opacity == 1


def test_rgb_16():
    assert approx_equal(d3.rgb(-10, -20, -30, -0.2), (-10, -20, -30, -0.2))
    assert approx_equal(d3.rgb(300, 400, 500, 1.2), (300, 400, 500, 1.2))


def test_rgb_17():
    assert approx_equal(d3.rgb("12", "34", "56"), (12, 34, 56, 1))


def test_rgb_18():
    assert approx_equal(d3.rgb(-10, -20, -30, "-0.2"), (-10, -20, -30, -0.2))
    assert approx_equal(d3.rgb(300, 400, 500, "1.2"), (300, 400, 500, 1.2))


def test_rgb_21():
    assert approx_equal(d3.rgb(10, 20, 30, 1), (10, 20, 30, 1))
    assert approx_equal(d3.rgb(10, 20, 30, 1), (10, 20, 30, 1))


def test_rgb_22():
    assert approx_equal(d3.rgb("#abcdef"), (171, 205, 239, 1))
    assert approx_equal(d3.rgb("#abc"), (170, 187, 204, 1))
    assert approx_equal(d3.rgb("rgb(12, 34, 56)"), (12, 34, 56, 1))
    assert approx_equal(d3.rgb("rgb(12%, 34%, 56%)"), (31, 87, 143, 1))
    assert approx_equal(d3.rgb("hsl(60,100%,20%)"), (102, 102, 0, 1))
    assert approx_equal(d3.rgb("aliceblue"), (240, 248, 255, 1))
    assert approx_equal(d3.rgb("hsla(60,100%,20%,0.4)"), (102, 102, 0, 0.4))


def test_rgb_25():
    c1 = d3.rgb("rgba(70, 130, 180, 0.4)")
    c2 = d3.rgb(c1)
    assert approx_equal(c1, (70, 130, 180, 0.4))
    c1.r = c1.g = c1.b = c1.opacity = 0
    assert approx_equal(c1, (0, 0, 0, 0))
    assert approx_equal(c2, (70, 130, 180, 0.4))


def test_rgb_26():
    assert approx_equal(d3.rgb(HSL(0, 1, 0.5)), (255, 0, 0, 1))
    assert approx_equal(d3.rgb(HSL(0, 1, 0.5, 0.4)), (255, 0, 0, 0.4))


def test_rgb_27():
    assert d3.rgb("white").displayable() is True
    assert d3.rgb("red").displayable() is True
    assert d3.rgb("black").displayable() is True
    assert d3.rgb("invalid").displayable() is True
    assert d3.rgb(-1, 0, 0).displayable() is False
    assert d3.rgb(0, -1, 0).displayable() is False
    assert d3.rgb(0, 0, -1).displayable() is False
    assert d3.rgb(256, 0, 0).displayable() is False
    assert d3.rgb(0, 256, 0).displayable() is False
    assert d3.rgb(0, 0, 256).displayable() is False
    assert d3.rgb(0, 0, 255, 0).displayable() is True
    assert d3.rgb(0, 0, 255, 1.2).displayable() is False
    assert d3.rgb(0, 0, 255, -0.2).displayable() is False


def test_rgb_28():
    c = d3.rgb("rgba(165, 42, 42, 0.4)")
    assert approx_equal(c.brighter(0.5), (197, 50, 50, 0.4))
    assert approx_equal(c.brighter(1), (236, 60, 60, 0.4))
    assert approx_equal(c.brighter(2), (337, 86, 86, 0.4))


def test_rgb_29():
    c1 = d3.rgb("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter(1)
    assert approx_equal(c1, (70, 130, 180, 0.4))
    assert approx_equal(c2, (100, 186, 257, 0.4))


def test_rgb_30():
    c1 = d3.rgb("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter()
    c3 = c1.brighter(1)
    assert approx_equal(c2, (c3.r, c3.g, c3.b, 0.4))


def test_rgb_31():
    c1 = d3.rgb("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter(1.5)
    c3 = c1.darker(-1.5)
    assert approx_equal(c2, (c3.r, c3.g, c3.b, 0.4))


def test_rgb_32():
    c1 = d3.rgb("black")
    c2 = c1.brighter(1)
    assert approx_equal(c1, (0, 0, 0, 1))
    assert approx_equal(c2, (0, 0, 0, 1))


def test_rgb_33():
    c = d3.rgb("rgba(165, 42, 42, 0.4)")
    assert approx_equal(c.darker(0.5), (138, 35, 35, 0.4))
    assert approx_equal(c.darker(1), (115, 29, 29, 0.4))
    assert approx_equal(c.darker(2), (81, 21, 21, 0.4))


def test_rgb_34():
    c1 = d3.rgb("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker(1)
    assert approx_equal(c1, (70, 130, 180, 0.4))
    assert approx_equal(c2, (49, 91, 126, 0.4))


def test_rgb_35():
    c1 = d3.rgb("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker()
    c3 = c1.darker(1)
    assert approx_equal(c2, (c3.r, c3.g, c3.b, 0.4))


def test_rgb_36():
    c1 = d3.rgb("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker(1.5)
    c3 = c1.brighter(-1.5)
    assert approx_equal(c2, (c3.r, c3.g, c3.b, 0.4))


def test_rgb_37():
    c = d3.rgb(70, 130, 180)
    assert c.rgb() == c
