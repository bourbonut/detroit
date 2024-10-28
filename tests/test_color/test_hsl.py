import detroit as d3
from detroit.color.color import Color, RGB, HSL
import math

def approx_equal(actual, h, s, l, opacity):
    c1 = isinstance(actual, HSL)
    c2 = math.isnan(actual.h) or round(actual.h) == round(h)
    c3 = math.isnan(actual.s) or round(actual.s) == round(s)
    c4 = math.isnan(actual.l) or round(actual.l) == round(l)
    c5 = math.isnan(actual.opacity) or round(actual.opacity) == round(opacity)
    return all((c1, c2, c3, c4, c5))

def test_hsl_1():
    c = d3.hsl(120, 0.4, 0.5)
    assert isinstance(c, Color)
    assert isinstance(c, HSL)

def test_hsl_2():
    assert approx_equal(d3.hsl("#abc"), 210, 0.25, 0.7333333, 1)
    assert approx_equal(d3.hsl("hsla(60, 100%, 20%, 0.4)"), 60, 1, 0.2, 0.4)

def test_hsl_3():
    assert str(d3.hsl("#abcdef")) == "rgb(171, 205, 239)"
    assert str(d3.hsl("moccasin")) == "rgb(255, 228, 181)"
    assert str(d3.hsl("hsl(60, 100%, 20%)")) == "rgb(102, 102, 0)"
    assert str(d3.hsl("hsla(60, 100%, 20%, 0.4)")) == "rgba(102, 102, 0, 0.4)"
    assert str(d3.hsl("rgb(12, 34, 56)")) == "rgb(12, 34, 56)"
    assert str(d3.hsl(RGB(12, 34, 56))) == "rgb(12, 34, 56)"
    assert str(d3.hsl(HSL(60, 1, 0.2))) == "rgb(102, 102, 0)"
    assert str(d3.hsl(HSL(60, 1, 0.2, 0.4))) == "rgba(102, 102, 0, 0.4)"

def test_hsl_4():
    assert d3.hsl("#abcdef").format_rgb() == "rgb(171, 205, 239)"
    assert d3.hsl("hsl(60, 100%, 20%)").format_rgb() == "rgb(102, 102, 0)"
    assert d3.hsl("rgba(12%, 34%, 56%, 0.4)").format_rgb() == "rgba(31, 87, 143, 0.4)"
    assert d3.hsl("hsla(60, 100%, 20%, 0.4)").format_rgb() == "rgba(102, 102, 0, 0.4)"

def test_hsl_5():
    assert d3.hsl("#abcdef").format_hsl() == "hsl(210, 68%, 80.3921568627451%)"
    assert d3.hsl("hsl(60, 100%, 20%)").format_hsl() == "hsl(60, 100%, 20%)"
    assert d3.hsl("rgba(12%, 34%, 56%, 0.4)").format_hsl() == "hsla(210, 64.70588235294117%, 34%, 0.4)"
    assert d3.hsl("hsla(60, 100%, 20%, 0.4)").format_hsl() == "hsla(60, 100%, 20%, 0.4)"

def test_hsl_6():
    assert d3.hsl(180, -100, -50).format_hsl() == "hsl(180, 0%, 0%)"
    assert d3.hsl(180, 150, 200).format_hsl() == "hsl(180, 100%, 100%)"
    assert d3.hsl(-90, 50, 50).format_hsl() == "hsl(270, 100%, 100%)"
    assert d3.hsl(420, 50, 50).format_hsl() == "hsl(60, 100%, 100%)"

def test_hsl_7():
    assert d3.hsl("#abcdef").format_hex() == "#abcdef"
    assert d3.hsl("hsl(60, 100%, 20%)").format_hex() == "#666600"
    assert d3.hsl("rgba(12%, 34%, 56%, 0.4)").format_hex() == "#1f578f"
    assert d3.hsl("hsla(60, 100%, 20%, 0.4)").format_hex() == "#666600"

def test_hsl_8():
    c = d3.hsl("#abc")
    c.h += 10
    c.s += 0.01
    c.l -= 0.01
    c.opacity = 0.4
    assert str(c) == "rgba(166, 178, 203, 0.4)"

def test_hsl_9():
    assert str(d3.hsl("invalid")) == "rgb(0, 0, 0)"
    assert str(d3.hsl("#000")) == "rgb(0, 0, 0)"
    assert str(d3.hsl("#ccc")) == "rgb(204, 204, 204)"
    assert str(d3.hsl("#fff")) == "rgb(255, 255, 255)"
    assert str(d3.hsl(math.nan, 0.5, 0.4)) == "rgb(102, 102, 102)" # equivalent to hsl(*, 0, 0.4)
    assert str(d3.hsl(120, math.nan, 0.4)) == "rgb(102, 102, 102)"
    assert str(d3.hsl(math.nan, math.nan, 0.4)) == "rgb(102, 102, 102)"
    assert str(d3.hsl(120, 0.5, math.nan)) == "rgb(0, 0, 0)" # equivalent to hsl(120, 0.5, 0)

def test_hsl_10():
    c = d3.hsl("#abc")
    c.opacity = math.nan
    assert str(c) == "rgb(170, 187, 204)"

def test_hsl_11():
    assert approx_equal(d3.hsl(-10, 0.4, 0.5), -10, 0.4, 0.5, 1)
    assert approx_equal(d3.hsl(0, 0.4, 0.5), 0, 0.4, 0.5, 1)
    assert approx_equal(d3.hsl(360, 0.4, 0.5), 360, 0.4, 0.5, 1)
    assert approx_equal(d3.hsl(370, 0.4, 0.5), 370, 0.4, 0.5, 1)

def test_hsl_12():
    assert approx_equal(d3.hsl(120, -0.1, 0.5), 120, -0.1, 0.5, 1)
    assert approx_equal(d3.hsl(120, 1.1, 0.5), 120, 1.1, 0.5, 1)
    assert approx_equal(d3.hsl(120, 0.2, -0.1), 120, 0.2, -0.1, 1)
    assert approx_equal(d3.hsl(120, 0.2, 1.1), 120, 0.2, 1.1, 1)

def test_hsl_13():
    assert approx_equal(d3.hsl(120, -0.1, -0.2).clamp(), 120, 0, 0, 1)
    assert approx_equal(d3.hsl(120, 1.1, 1.2).clamp(), 120, 1, 1, 1)
    assert approx_equal(d3.hsl(120, 2.1, 2.2).clamp(), 120, 1, 1, 1)
    assert approx_equal(d3.hsl(420, -0.1, -0.2).clamp(), 60, 0, 0, 1)
    assert approx_equal(d3.hsl(-420, -0.1, -0.2).clamp(), 300, 0, 0, 1)
    assert d3.hsl(-420, -0.1, -0.2, math.nan).clamp().opacity == 1
    assert d3.hsl(-420, -0.1, -0.2, 0.5).clamp().opacity == 0.5
    assert d3.hsl(-420, -0.1, -0.2, -1).clamp().opacity == 0
    assert d3.hsl(-420, -0.1, -0.2, 2).clamp().opacity == 1

def test_hsl_14():
    assert approx_equal(d3.hsl(120, 0.1, 0.5, -0.2), 120, 0.1, 0.5, -0.2)
    assert approx_equal(d3.hsl(120, 0.9, 0.5, 1.2), 120, 0.9, 0.5, 1.2)

def test_hsl_15():
    assert approx_equal(d3.hsl("120", ".4", ".5"), 120, 0.4, 0.5, 1)

def test_hsl_16():
    assert approx_equal(d3.hsl(120, 0.1, 0.5, "0.2"), 120, 0.1, 0.5, 0.2)
    assert approx_equal(d3.hsl(120, 0.9, 0.5, "0.9"), 120, 0.9, 0.5, 0.9)

def test_hsl_17():
    assert approx_equal(d3.hsl(10, 0.2, 0.3, 1), 10, 0.2, 0.3, 1)
    assert approx_equal(d3.hsl(10, 0.2, 0.3, 1), 10, 0.2, 0.3, 1)

def test_hsl_18():
    assert approx_equal(d3.hsl(0, 0, 0), 0, 0, 0, 1)
    assert approx_equal(d3.hsl(42, 0, 0.5), 42, 0, 0.5, 1)
    assert approx_equal(d3.hsl(118, 0, 1), 118, 0, 1, 1)

def test_hsl_19():
    assert approx_equal(d3.hsl(0, 0, 0), 0, 0, 0, 1)
    assert approx_equal(d3.hsl(0, 0.18, 0), 0, 0.18, 0, 1)
    assert approx_equal(d3.hsl(0, 0.42, 1), 0, 0.42, 1, 1)
    assert approx_equal(d3.hsl(0, 1, 1), 0, 1, 1, 1)

def test_hsl_20():
    assert approx_equal(d3.hsl("#abcdef"), 210, 0.68, 0.8039215, 1)
    assert approx_equal(d3.hsl("#abc"), 210, 0.25, 0.733333333, 1)
    assert approx_equal(d3.hsl("rgb(12, 34, 56)"), 210, 0.647058, 0.1333333, 1)
    assert approx_equal(d3.hsl("rgb(12%, 34%, 56%)"), 210, 0.647058, 0.34, 1)
    assert approx_equal(d3.hsl("hsl(60,100%,20%)"), 60, 1, 0.2, 1)
    assert approx_equal(d3.hsl("hsla(60,100%,20%,0.4)"), 60, 1, 0.2, 0.4)
    assert approx_equal(d3.hsl("aliceblue"), 208, 1, 0.9705882, 1)
    assert approx_equal(d3.hsl("transparent"), math.nan, math.nan, math.nan, 0)

def test_hsl_21():
    assert approx_equal(d3.hsl("hsl(120,0%,20%)"), math.nan, 0, 0.2, 1)
    assert approx_equal(d3.hsl("hsl(120,-10%,20%)"), math.nan, -0.1, 0.2, 1)

def test_hsl_22():
    assert approx_equal(d3.hsl("hsl(120,20%,-10%)"), math.nan, math.nan, -0.1, 1)
    assert approx_equal(d3.hsl("hsl(120,20%,0%)"), math.nan, math.nan, 0.0, 1)
    assert approx_equal(d3.hsl("hsl(120,20%,100%)"), math.nan, math.nan, 1.0, 1)
    assert approx_equal(d3.hsl("hsl(120,20%,120%)"), math.nan, math.nan, 1.2, 1)

def test_hsl_23():
    assert approx_equal(d3.hsl("hsla(120,20%,10%,0)"), math.nan, math.nan, math.nan, 0)
    assert approx_equal(d3.hsl("hsla(120,20%,10%,-0.1)"), math.nan, math.nan, math.nan, -0.1)

def test_hsl_24():
    assert approx_equal(d3.hsl("hsl(325,50%,40%)"), 325, 0.5, 0.4, 1)

def test_hsl_25():
    assert approx_equal(d3.hsl("invalid"), 0, 0, 0, 1)

def test_hsl_26():
    c1 = d3.hsl("hsla(120,30%,50%,0.4)")
    c2 = d3.hsl(c1)
    assert approx_equal(c1, 120, 0.3, 0.5, 0.4)
    c1.h = c1.s = c1.l = c1.opacity = 0
    assert approx_equal(c1, 0, 0, 0, 0)
    assert approx_equal(c2, 120, 0.3, 0.5, 0.4)

def test_hsl_27():
    assert approx_equal(d3.hsl(RGB(255, 0, 0, 0.4)), 0, 1, 0.5, 0.4)

def test_hsl_28():
    assert approx_equal(d3.hsl("gray"), math.nan, 0, 0.5019608, 1)
    assert approx_equal(d3.hsl("#ccc"), math.nan, 0, 0.8, 1)
    assert approx_equal(d3.hsl(d3.rgb("gray")), math.nan, 0, 0.5019608, 1)

def test_hsl_29():
    assert approx_equal(d3.hsl("black"), math.nan, math.nan, 0, 1)
    assert approx_equal(d3.hsl("#000"), math.nan, math.nan, 0, 1)
    assert approx_equal(d3.hsl("white"), math.nan, math.nan, 1, 1)
    assert approx_equal(d3.hsl("#fff"), math.nan, math.nan, 1, 1)
    assert approx_equal(d3.hsl(d3.rgb("#fff")), math.nan, math.nan, 1, 1)

def test_hsl_31():
    assert d3.hsl("white").displayable() is True
    assert d3.hsl("red").displayable() is True
    assert d3.hsl("black").displayable() is True
    assert d3.hsl("invalid").displayable() is True
    assert d3.hsl(math.nan, math.nan, 1).displayable() is True
    assert d3.hsl(math.nan, math.nan, 1.5).displayable() is False
    assert d3.hsl(120, -0.5, 0).displayable() is False
    assert d3.hsl(120, 1.5, 0).displayable() is False
    assert d3.hsl(0, 1, 1, 0).displayable() is True
    assert d3.hsl(0, 1, 1, 1).displayable() is True
    assert d3.hsl(0, 1, 1, -0.2).displayable() is False
    assert d3.hsl(0, 1, 1, 1.2).displayable() is False

def test_hsl_32():
    c = d3.hsl("rgba(165, 42, 42, 0.4)")
    assert approx_equal(c.brighter(0.5), 0, 0.5942028, 0.4851222, 0.4)
    assert approx_equal(c.brighter(1), 0, 0.5942028, 0.5798319, 0.4)
    assert approx_equal(c.brighter(2), 0, 0.5942028, 0.8283313, 0.4)

def test_hsl_33():
    c1 = d3.hsl("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter(1)
    assert approx_equal(c1, 207.272727, 0.44, 0.4901961, 0.4)
    assert approx_equal(c2, 207.272727, 0.44, 0.7002801, 0.4)

def test_hsl_34():
    c1 = d3.hsl("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter()
    c3 = c1.brighter(1)
    assert approx_equal(c2, c3.h, c3.s, c3.l, 0.4)

def test_hsl_35():
    c1 = d3.hsl("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter(1.5)
    c3 = c1.darker(-1.5)
    assert approx_equal(c2, c3.h, c3.s, c3.l, 0.4)

def test_hsl_36():
    c1 = d3.hsl("black")
    c2 = c1.brighter(1)
    assert approx_equal(c1, math.nan, math.nan, 0, 1)
    assert approx_equal(c2, math.nan, math.nan, 0, 1)

def test_hsl_37():
    c = d3.hsl("rgba(165, 42, 42, 0.4)")
    assert approx_equal(c.darker(0.5), 0, 0.5942029, 0.3395855, 0.4)
    assert approx_equal(c.darker(1), 0, 0.5942029, 0.2841176, 0.4)
    assert approx_equal(c.darker(2), 0, 0.5942029, 0.1988823, 0.4)

def test_hsl_38():
    c1 = d3.hsl("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker(1)
    assert approx_equal(c1, 207.272727, 0.44, 0.4901961, 0.4)
    assert approx_equal(c2, 207.272727, 0.44, 0.3431373, 0.4)

def test_hsl_39():
    c1 = d3.hsl("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker()
    c3 = c1.darker(1)
    assert approx_equal(c2, c3.h, c3.s, c3.l, 0.4)

def test_hsl_40():
    c1 = d3.hsl("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker(1.5)
    c3 = c1.brighter(-1.5)
    assert approx_equal(c2, c3.h, c3.s, c3.l, 0.4)

def test_hsl_41():
    c = d3.hsl(120, 0.3, 0.5, 0.4)
    r, g, b, opacity = 89, 166, 89, 0.4
    actual = c.rgb()
    c1 = isinstance(actual, RGB)
    c2 = math.isnan(actual.r) or round(actual.r) == round(r)
    c3 = math.isnan(actual.g) or round(actual.g) == round(g)
    c4 = math.isnan(actual.b) or round(actual.b) == round(b)
    c5 = math.isnan(actual.opacity) or round(actual.opacity) == round(opacity)
    assert all((c1, c2, c3, c4, c5))
