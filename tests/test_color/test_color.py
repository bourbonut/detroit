import math

import detroit as d3
from detroit.color.color import HSL, RGB


def approx_equal(actual, r, g, b, opacity):
    c1 = isinstance(actual, RGB)
    c2 = math.isnan(actual.r) or round(actual.r) == round(r)
    c3 = math.isnan(actual.g) or round(actual.g) == round(g)
    c4 = math.isnan(actual.b) or round(actual.b) == round(b)
    c5 = math.isnan(actual.opacity) or round(actual.opacity) == round(opacity)
    return all((c1, c2, c3, c4, c5))


def hsl_approx_equal(actual, h, s, l, opacity):
    c1 = isinstance(actual, HSL)
    c2 = math.isnan(actual.h) or round(actual.h) == round(h)
    c3 = math.isnan(actual.s) or round(actual.s) == round(s)
    c4 = math.isnan(actual.l) or round(actual.l) == round(l)
    c5 = math.isnan(actual.opacity) or round(actual.opacity) == round(opacity)
    return all((c1, c2, c3, c4, c5))


def test_color_1():
    assert approx_equal(d3.color("moccasin"), 255, 228, 181, 1)
    assert approx_equal(d3.color("aliceblue"), 240, 248, 255, 1)
    assert approx_equal(d3.color("yellow"), 255, 255, 0, 1)
    assert approx_equal(d3.color("moccasin"), 255, 228, 181, 1)
    assert approx_equal(d3.color("aliceblue"), 240, 248, 255, 1)
    assert approx_equal(d3.color("yellow"), 255, 255, 0, 1)
    assert approx_equal(d3.color("rebeccapurple"), 102, 51, 153, 1)
    assert approx_equal(d3.color("transparent"), math.nan, math.nan, math.nan, 0)


def test_color_2():
    assert approx_equal(d3.color("#abcdef"), 171, 205, 239, 1)


def test_color_3():
    assert approx_equal(d3.color("#abc"), 170, 187, 204, 1)


def test_color_4():
    assert d3.color("#abcdef3") is None


def test_color_5():
    assert approx_equal(d3.color("#abcdef33"), 171, 205, 239, 0.2)


def test_color_6():
    assert approx_equal(d3.color("#abc3"), 170, 187, 204, 0.2)


def test_color_7():
    assert approx_equal(d3.color("rgb(12,34,56)"), 12, 34, 56, 1)


def test_color_8():
    assert approx_equal(d3.color("rgba(12,34,56,0.4)"), 12, 34, 56, 0.4)


def test_color_9():
    assert approx_equal(d3.color("rgb(12%,34%,56%)"), 31, 87, 143, 1)
    assert approx_equal(d3.color("rgb(100%,100%,100%)"), 255, 255, 255, 1)


def test_color_10():
    assert approx_equal(d3.color("rgba(12%,34%,56%,0.4)"), 31, 87, 143, 0.4)
    assert approx_equal(d3.color("rgba(100%,100%,100%,0.4)"), 255, 255, 255, 0.4)


def test_color_11():
    assert hsl_approx_equal(d3.color("hsl(60,100%,20%)"), 60, 1, 0.2, 1)


def test_color_12():
    assert hsl_approx_equal(d3.color("hsla(60,100%,20%,0.4)"), 60, 1, 0.2, 0.4)


def test_color_13():
    assert approx_equal(d3.color(" aliceblue\t\n"), 240, 248, 255, 1)
    assert approx_equal(d3.color(" #abc\t\n"), 170, 187, 204, 1)
    assert approx_equal(d3.color(" #aabbcc\t\n"), 170, 187, 204, 1)
    assert approx_equal(d3.color(" rgb(120,30,50)\t\n"), 120, 30, 50, 1)
    assert hsl_approx_equal(d3.color(" hsl(120,30%,50%)\t\n"), 120, 0.3, 0.5, 1)


def test_color_14():
    assert approx_equal(d3.color(" rgb( 120, 30 , 50 ) "), 120, 30, 50, 1)
    assert hsl_approx_equal(d3.color(" hsl( 120 , 30% , 50% ) "), 120, 0.3, 0.5, 1)
    assert approx_equal(d3.color(" rgba( 12, 34 , 56 , 0.4 ) "), 12, 34, 56, 0.4)
    assert approx_equal(d3.color(" rgba( 12% , 34% , 56% , 0.4 ) "), 31, 87, 143, 0.4)
    assert hsl_approx_equal(
        d3.color(" hsla( 60 , 100% , 20% , 0.4 ) "), 60, 1, 0.2, 0.4
    )


def test_color_15():
    assert approx_equal(d3.color("rgb(+120,+30,+50)"), 120, 30, 50, 1)
    assert hsl_approx_equal(d3.color("hsl(+120,+30%,+50%)"), 120, 0.3, 0.5, 1)
    assert approx_equal(d3.color("rgb(-120,-30,-50)"), -120, -30, -50, 1)
    assert hsl_approx_equal(
        d3.color("hsl(-120,-30%,-50%)"), math.nan, math.nan, -0.5, 1
    )
    assert approx_equal(d3.color("rgba(12,34,56,+0.4)"), 12, 34, 56, 0.4)
    assert approx_equal(
        d3.color("rgba(12,34,56,-0.4)"), math.nan, math.nan, math.nan, -0.4
    )
    assert approx_equal(d3.color("rgba(12%,34%,56%,+0.4)"), 31, 87, 143, 0.4)
    assert approx_equal(
        d3.color("rgba(12%,34%,56%,-0.4)"), math.nan, math.nan, math.nan, -0.4
    )
    assert hsl_approx_equal(d3.color("hsla(60,100%,20%,+0.4)"), 60, 1, 0.2, 0.4)
    assert hsl_approx_equal(
        d3.color("hsla(60,100%,20%,-0.4)"), math.nan, math.nan, math.nan, -0.4
    )


def test_color_16():
    assert approx_equal(d3.color("rgb(20.0%,30.4%,51.2%)"), 51, 78, 131, 1)
    assert hsl_approx_equal(d3.color("hsl(20.0,30.4%,51.2%)"), 20, 0.304, 0.512, 1)


def test_color_17():
    assert hsl_approx_equal(d3.color("hsl(.9,.3%,.5%)"), 0.9, 0.003, 0.005, 1)
    assert hsl_approx_equal(d3.color("hsla(.9,.3%,.5%,.5)"), 0.9, 0.003, 0.005, 0.5)
    assert approx_equal(d3.color("rgb(.1%,.2%,.3%)"), 0, 1, 1, 1)
    assert approx_equal(d3.color("rgba(120,30,50,.5)"), 120, 30, 50, 0.5)


def test_color_18():
    assert hsl_approx_equal(d3.color("hsl(1e1,2e1%,3e1%)"), 10, 0.2, 0.3, 1)
    assert hsl_approx_equal(
        d3.color("hsla(9e-1,3e-1%,5e-1%,5e-1)"), 0.9, 0.003, 0.005, 0.5
    )
    assert approx_equal(d3.color("rgb(1e-1%,2e-1%,3e-1%)"), 0, 1, 1, 1)
    assert approx_equal(d3.color("rgba(120,30,50,1e-1)"), 120, 30, 50, 0.1)


def test_color_19():
    assert d3.color("rgb(120.5,30,50)") is None


def test_color_20():
    assert d3.color("rgb(120.,30,50)") is None
    assert d3.color("rgb(120.%,30%,50%)") is None
    assert d3.color("rgba(120,30,50,1.)") is None
    assert d3.color("rgba(12%,30%,50%,1.)") is None
    assert d3.color("hsla(60,100%,20%,1.)") is None


def test_color_21():
    assert d3.color("bostock") is None


def test_color_22():
    assert approx_equal(d3.color("rgba(0,0,0,0)"), math.nan, math.nan, math.nan, 0)
    assert approx_equal(d3.color("#0000"), math.nan, math.nan, math.nan, 0)
    assert approx_equal(d3.color("#00000000"), math.nan, math.nan, math.nan, 0)


def test_color_23():
    assert d3.color("rgb (120,30,50)") is None
    assert d3.color("rgb (12%,30%,50%)") is None
    assert d3.color("hsl (120,30%,50%)") is None
    assert d3.color("hsl(120,30 %,50%)") is None
    assert d3.color("rgba (120,30,50,1)") is None
    assert d3.color("rgba (12%,30%,50%,1)") is None
    assert d3.color("hsla (120,30%,50%,1)") is None


def test_color_24():
    assert approx_equal(d3.color("aLiCeBlUE"), 240, 248, 255, 1)
    assert approx_equal(d3.color("transPARENT"), math.nan, math.nan, math.nan, 0)
    assert approx_equal(d3.color(" #aBc\t\n"), 170, 187, 204, 1)
    assert approx_equal(d3.color(" #aaBBCC\t\n"), 170, 187, 204, 1)
    assert approx_equal(d3.color(" rGB(120,30,50)\t\n"), 120, 30, 50, 1)
    assert hsl_approx_equal(d3.color(" HSl(120,30%,50%)\t\n"), 120, 0.3, 0.5, 1)


def test_color_25():
    assert d3.color("invalid") is None
    assert d3.color("hasOwnProperty") is None
    assert d3.color("__proto__") is None
    assert d3.color("#ab") is None


def test_color_26():
    assert d3.color("rgba(12%,34%,56%,0.4)").format_hex() == "#1f578f"
