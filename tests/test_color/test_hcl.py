import detroit as d3
from detroit.coloration.color import HSL, RGB, Color
from detroit.coloration.lab import LAB, HCL
import math

def approx_equal(actual, h, c, l, opacity):
    c1 = isinstance(actual, HCL)
    c2 = math.isnan(actual.h) or h - 1e-6 <= actual.h and actual.h <= h + 1e-6
    c3 = math.isnan(actual.c) or c - 1e-6 <= actual.c and actual.c <= c + 1e-6
    c4 = math.isnan(actual.l) or l - 1e-6 <= actual.l and actual.l <= l + 1e-6
    c5 = math.isnan(actual.opacity) or round(actual.opacity) == round(opacity)
    return all((c1, c2, c3, c4, c5))

def test_hcl_1():
    c = d3.hcl(120, 40, 50)
    assert isinstance(c, HCL)
    assert isinstance(c, Color)

def test_hcl_2():
    assert approx_equal(d3.hcl("#abc"), 252.37145234745182, 11.223567114593477, 74.96879980931759, 1)

def test_hcl_3():
    assert approx_equal(d3.hcl("black"), math.nan, math.nan, 0, 1)
    assert approx_equal(d3.hcl("#000"), math.nan, math.nan, 0, 1)
    assert approx_equal(d3.hcl(d3.lab("#000")), math.nan, math.nan, 0, 1)
    assert approx_equal(d3.hcl("white"), math.nan, math.nan, 100, 1)
    assert approx_equal(d3.hcl("#fff"), math.nan, math.nan, 100, 1)
    assert approx_equal(d3.hcl(d3.lab("#fff")), math.nan, math.nan, 100, 1)

def test_hcl_4():
    assert approx_equal(d3.hcl("gray"), math.nan, 0, 53.585013, 1)
    assert approx_equal(d3.hcl(d3.lab("gray")), math.nan, 0, 53.585013, 1)

def test_hcl_5():
    assert str(d3.hcl("#abcdef")) == "rgb(171, 205, 239)"
    assert str(d3.hcl("moccasin")) == "rgb(255, 228, 181)"
    assert str(d3.hcl("hsl(60, 100%, 20%)")) == "rgb(102, 102, 0)"
    assert str(d3.hcl("rgb(12, 34, 56)")) == "rgb(12, 34, 56)"
    assert str(d3.hcl(RGB(12, 34, 56))) == "rgb(12, 34, 56)"
    assert str(d3.hcl(HSL(60, 1, 0.2))) == "rgb(102, 102, 0)"

def test_hcl_6():
    c = d3.hcl("#abc")
    c.h += 10
    c.c += 1
    c.l -= 1
    assert str(c) == "rgb(170, 183, 204)"

def test_hcl_7():
    c = d3.hcl("#abc")
    c.opacity = math.nan
    assert str(c) == "rgb(170, 187, 204)"

def test_hcl_8():
    assert str(d3.hcl("invalid")) == "rgb(0, 0, 0)"
    assert str(d3.hcl("#000")) == "rgb(0, 0, 0)"
    assert str(d3.hcl("#ccc")) == "rgb(204, 204, 204)"
    assert str(d3.hcl("#fff")) == "rgb(255, 255, 255)"
    assert str(d3.hcl(math.nan, 20, 40)), "rgb(94, 94, 94)" # equivalent to hcl(*, *, 40)
    assert str(d3.hcl(120, math.nan, 40)), "rgb(94, 94, 94)"
    assert str(d3.hcl(0, math.nan, 40)), "rgb(94, 94, 94)"
    assert str(d3.hcl(120, 50, math.nan)), "rgb(0, 0, 0)" # equivalent to hcl(*, *, 0)
    assert str(d3.hcl(0, 50, math.nan)), "rgb(0, 0, 0)"
    assert str(d3.hcl(120, 0, math.nan)), "rgb(0, 0, 0)"

def test_hcl_9():
    assert str(d3.hcl("yellow")) == "rgb(255, 255, 0)"

def test_hcl_10():
    assert approx_equal(d3.hcl(-10, 40, 50), -10, 40, 50, 1)
    assert approx_equal(d3.hcl(0, 40, 50), 0, 40, 50, 1)
    assert approx_equal(d3.hcl(360, 40, 50), 360, 40, 50, 1)
    assert approx_equal(d3.hcl(370, 40, 50), 370, 40, 50, 1)

def test_hcl_11():
    assert approx_equal(d3.hcl(120, 20, -10), 120, 20, -10, 1)
    assert approx_equal(d3.hcl(120, 20, 0), 120, 20, 0, 1)
    assert approx_equal(d3.hcl(120, 20, 100), 120, 20, 100, 1)
    assert approx_equal(d3.hcl(120, 20, 110), 120, 20, 110, 1)

def test_hcl_12():
    assert approx_equal(d3.hcl(120, 20, 100, -0.2), 120, 20, 100, -0.2)
    assert approx_equal(d3.hcl(120, 20, 110, 1.2), 120, 20, 110, 1.2)

def test_hcl_13():
    assert approx_equal(d3.hcl("120", "40", "50"), 120, 40, 50, 1)

def test_hcl_14():
    assert approx_equal(d3.hcl(120, 40, 50, "0.2"), 120, 40, 50, 0.2)

def test_hcl_15():
    assert approx_equal(d3.hcl(10, 20, 30, 1), 10, 20, 30, 1)
    assert approx_equal(d3.hcl(10, 20, 30, 1), 10, 20, 30, 1)

def test_hcl_16():
    assert approx_equal(d3.hcl("#abcdef"), 254.0079700170605, 21.62257586147983, 80.77135418262527, 1)
    assert approx_equal(d3.hcl("#abc"), 252.37145234745182, 11.223567114593477, 74.96879980931759, 1)
    assert approx_equal(d3.hcl("rgb(12, 34, 56)"), 262.8292023352897, 17.30347233219686, 12.404844123471648, 1)
    assert approx_equal(d3.hcl("rgb(12%, 34%, 56%)"), 266.117653326772, 37.03612078188506, 35.48300043476593, 1)
    assert approx_equal(d3.hcl("rgba(12%, 34%, 56%, 0.4)"), 266.117653326772, 37.03612078188506, 35.48300043476593, 0.4)
    assert approx_equal(d3.hcl("hsl(60,100%,20%)"), 99.57458688693686, 48.327323183108916, 41.97125732118659, 1)
    assert approx_equal(d3.hcl("hsla(60,100%,20%,0.4)"), 99.57458688693686, 48.327323183108916, 41.97125732118659, 0.4)
    assert approx_equal(d3.hcl("aliceblue"), 247.7353849904697, 4.681732046417135, 97.12294991108756, 1)

def test_hcl_17():
    assert approx_equal(d3.hcl("invalid"), 0, 0, 0, 1)

def test_hcl_18():
    c1 = d3.hcl(120, 30, 50, 0.4)
    c2 = d3.hcl(c1)
    assert approx_equal(c1, 120, 30, 50, 0.4)
    c1.h = c1.c = c1.l = c1.opacity = 0
    assert approx_equal(c1, 0, 0, 0, 0)
    assert approx_equal(c2, 120, 30, 50, 0.4)

def test_hcl_19():
    assert approx_equal(d3.hcl(LAB(0, 0, 0, 1)), math.nan, math.nan, 0, 1)
    assert approx_equal(d3.hcl(LAB(50, 0, 0, 1)), math.nan, 0, 50, 1)
    assert approx_equal(d3.hcl(LAB(100, 0, 0, 1)), math.nan, math.nan, 100, 1)
    assert approx_equal(d3.hcl(LAB(0, 10, 0, 1)), 0, 10, 0, 1)
    assert approx_equal(d3.hcl(LAB(50, 10, 0, 1)), 0, 10, 50, 1)
    assert approx_equal(d3.hcl(LAB(100, 10, 0, 1)), 0, 10, 100, 1)
    assert approx_equal(d3.hcl(LAB(0, 0, 10, 1)), 90, 10, 0, 1)
    assert approx_equal(d3.hcl(LAB(50, 0, 10, 1)), 90, 10, 50, 1)
    assert approx_equal(d3.hcl(LAB(100, 0, 10, 1)), 90, 10, 100, 1)

def test_hcl_20():
    assert approx_equal(d3.hcl(RGB(255, 0, 0, 0.4)), 40.85261277607024, 106.83899941284552, 54.29173376861782, 0.4)

def test_hcl_21():
    c = d3.hcl("rgba(165, 42, 42, 0.4)")
    assert approx_equal(c.brighter(0.5), 32.28342524928155, 59.60231039142763, 47.149667346714935, 0.4)
    assert approx_equal(c.brighter(1), 32.28342524928155, 59.60231039142763, 56.149667346714935, 0.4)
    assert approx_equal(c.brighter(2), 32.28342524928155, 59.60231039142763, 74.14966734671493, 0.4)

def test_hcl_22():
    c1 = d3.hcl("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter(1)
    assert approx_equal(c1, 255.71009124439382, 33.88100417355615, 51.98624890550498, 0.4)
    assert approx_equal(c2, 255.71009124439382, 33.88100417355615, 69.98624890550498, 0.4)

def test_hcl_23():
    c1 = d3.hcl("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter()
    c3 = c1.brighter(1)
    assert approx_equal(c2, c3.h, c3.c, c3.l, 0.4)

def test_hcl_24():
    c1 = d3.hcl("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter(1.5)
    c3 = c1.darker(-1.5)
    assert approx_equal(c2, c3.h, c3.c, c3.l, 0.4)

def test_hcl_25():
    c = d3.hcl("rgba(165, 42, 42, 0.4)")
    assert approx_equal(c.darker(0.5), 32.28342524928155, 59.60231039142763, 29.149667346714935, 0.4)
    assert approx_equal(c.darker(1), 32.28342524928155, 59.60231039142763, 20.149667346714935, 0.4)
    assert approx_equal(c.darker(2), 32.28342524928155, 59.60231039142763, 2.149667346714935, 0.4)

def test_hcl_26():
    c1 = d3.hcl("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker(1)
    assert approx_equal(c1, 255.71009124439382, 33.88100417355615, 51.98624890550498, 0.4)
    assert approx_equal(c2, 255.71009124439382, 33.88100417355615, 33.98624890550498, 0.4)

def test_hcl_27():
    c1 = d3.hcl("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker()
    c3 = c1.darker(1)
    assert approx_equal(c2, c3.h, c3.c, c3.l, 0.4)

def test_hcl_28():
    c1 = d3.hcl("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker(1.5)
    c3 = c1.brighter(-1.5)
    assert approx_equal(c2, c3.h, c3.c, c3.l, 0.4)

def test_hcl_29():
    c = d3.hcl(120, 30, 50, 0.4)
    actual = c.rgb()
    r, g, b, opacity = 105, 126, 73, 0.4
    c1 = isinstance(actual, RGB)
    c2 = math.isnan(actual.r) or round(actual.r) == round(r)
    c3 = math.isnan(actual.g) or round(actual.g) == round(g)
    c4 = math.isnan(actual.b) or round(actual.b) == round(b)
    c5 = math.isnan(actual.opacity) or round(actual.opacity) == round(opacity)
    assert all((c1, c2, c3, c4, c5))
