import math

import detroit as d3
from detroit.coloration.color import RGB, Color
from detroit.coloration.lab import LAB


def approx_equal(actual, l, a, b, opacity):
    c1 = isinstance(actual, LAB)
    c2 = math.isnan(actual.l) or l - 1e-6 <= actual.l and actual.l <= l + 1e-6
    c3 = math.isnan(actual.a) or a - 1e-6 <= actual.a and actual.a <= a + 1e-6
    c4 = math.isnan(actual.b) or b - 1e-6 <= actual.b and actual.b <= b + 1e-6
    c5 = math.isnan(actual.opacity) or round(actual.opacity) == round(opacity)
    return all((c1, c2, c3, c4, c5))


def test_lab_1():
    c = d3.lab(120, 40, 50)
    assert isinstance(c, LAB)
    assert isinstance(c, Color)


def test_lab_2():
    assert approx_equal(
        d3.lab("rgba(170, 187, 204, 0.4)"),
        74.96879980931759,
        -3.398998724348956,
        -10.696507207853333,
        0.4,
    )


def test_lab_3():
    assert str(d3.lab("#abcdef")) == "rgb(171, 205, 239)"
    assert str(d3.lab("moccasin")) == "rgb(255, 228, 181)"
    assert str(d3.lab("hsl(60, 100%, 20%)")), "rgb(102, 102, 0)"
    assert str(d3.lab("hsla(60, 100%, 20%, 0.4)")) == "rgba(102, 102, 0, 0.4)"
    assert str(d3.lab("rgb(12, 34, 56)")) == "rgb(12, 34, 56)"
    assert str(d3.lab(d3.rgb(12, 34, 56))) == "rgb(12, 34, 56)"
    assert str(d3.lab(d3.hsl(60, 1, 0.2))) == "rgb(102, 102, 0)"
    assert str(d3.lab(d3.hsl(60, 1, 0.2, 0.4))) == "rgba(102, 102, 0, 0.4)"


def test_lab_4():
    c = d3.lab("#abc")
    c.l += 10
    c.a -= 10
    c.b += 10
    c.opacity = 0.4
    assert str(c) == "rgba(184, 220, 213, 0.4)"


def test_lab_5():
    assert str(d3.lab("invalid")) == "rgb(0, 0, 0)"
    assert str(d3.lab(math.nan, 0, 0)) == "rgb(0, 0, 0)"
    assert str(d3.lab(50, math.nan, 0)) == "rgb(119, 119, 119)"
    assert str(d3.lab(50, 0, math.nan)) == "rgb(119, 119, 119)"
    assert str(d3.lab(50, math.nan, math.nan)) == "rgb(119, 119, 119)"


def test_lab_6():
    c = d3.lab("#abc")
    c.opacity = math.nan
    assert str(c) == "rgb(170, 187, 204)"


def test_lab_7():
    assert approx_equal(d3.lab(-10, 1, 2), -10, 1, 2, 1)
    assert approx_equal(d3.lab(0, 1, 2), 0, 1, 2, 1)
    assert approx_equal(d3.lab(100, 1, 2), 100, 1, 2, 1)
    assert approx_equal(d3.lab(110, 1, 2), 110, 1, 2, 1)


def test_lab_8():
    assert approx_equal(d3.lab(50, 10, 20, -0.2), 50, 10, 20, -0.2)
    assert approx_equal(d3.lab(50, 10, 20, 1.2), 50, 10, 20, 1.2)


def test_lab_9():
    assert approx_equal(d3.lab("50", "4", "-5"), 50, 4, -5, 1)


def test_lab_10():
    assert approx_equal(d3.lab(50, 4, -5, "0.2"), 50, 4, -5, 0.2)


def test_lab_11():
    assert approx_equal(d3.lab(10, 20, 30, 1), 10, 20, 30, 1)
    assert approx_equal(d3.lab(10, 20, 30, 1), 10, 20, 30, 1)


def test_lab_12():
    assert approx_equal(
        d3.lab("#abcdef"), 80.77135418262527, -5.957098328496224, -20.785782794739237, 1
    )
    assert approx_equal(
        d3.lab("#abc"), 74.96879980931759, -3.398998724348956, -10.696507207853333, 1
    )
    assert approx_equal(
        d3.lab("rgb(12, 34, 56)"),
        12.404844123471648,
        -2.159950219712034,
        -17.168132391132946,
        1,
    )
    assert approx_equal(
        d3.lab("rgb(12%, 34%, 56%)"),
        35.48300043476593,
        -2.507637675606522,
        -36.95112983195855,
        1,
    )
    assert approx_equal(
        d3.lab("rgba(12%, 34%, 56%, 0.4)"),
        35.48300043476593,
        -2.507637675606522,
        -36.95112983195855,
        0.4,
    )
    assert approx_equal(
        d3.lab("hsl(60,100%,20%)"),
        41.97125732118659,
        -8.03835128380484,
        47.65411917854332,
        1,
    )
    assert approx_equal(
        d3.lab("hsla(60,100%,20%,0.4)"),
        41.97125732118659,
        -8.03835128380484,
        47.65411917854332,
        0.4,
    )
    assert approx_equal(
        d3.lab("aliceblue"),
        97.12294991108756,
        -1.773836604137824,
        -4.332680308569969,
        1,
    )


def test_lab_13():
    assert approx_equal(d3.lab("invalid"), 0, 0, 0, 1)


def test_lab_14():
    c1 = d3.lab(50, 4, -5, 0.4)
    c2 = d3.lab(c1)
    assert approx_equal(c1, 50, 4, -5, 0.4)
    c1.l = c1.a = c1.b = c1.opacity = 0
    assert approx_equal(c1, 0, 0, 0, 0)
    assert approx_equal(c2, 50, 4, -5, 0.4)


def test_lab_15():
    assert approx_equal(d3.lab(d3.hcl(d3.lab(0, 10, 0))), 0, 10, 0, 1)


def test_lab_16():
    assert approx_equal(
        d3.lab(d3.rgb(255, 0, 0, 0.4)),
        54.29173376861782,
        80.8124553179771,
        69.88504032350531,
        0.4,
    )


def test_lab_17():
    c = d3.lab("rgba(165, 42, 42, 0.4)")
    assert approx_equal(
        c.brighter(0.5), 47.149667346714935, 50.388769337115, 31.834059255569358, 0.4
    )
    assert approx_equal(
        c.brighter(1), 56.149667346714935, 50.388769337115, 31.834059255569358, 0.4
    )
    assert approx_equal(
        c.brighter(2), 74.14966734671493, 50.388769337115, 31.834059255569358, 0.4
    )


def test_lab_18():
    c1 = d3.lab("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter(1)
    assert approx_equal(
        c1, 51.98624890550498, -8.362792037014344, -32.832699449697685, 0.4
    )
    assert approx_equal(
        c2, 69.98624890550498, -8.362792037014344, -32.832699449697685, 0.4
    )


def test_lab_19():
    c1 = d3.lab("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter()
    c3 = c1.brighter(1)
    assert approx_equal(c2, c3.l, c3.a, c3.b, 0.4)


def test_lab_20():
    c1 = d3.lab("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter(1.5)
    c3 = c1.darker(-1.5)
    assert approx_equal(c2, c3.l, c3.a, c3.b, 0.4)


def test_lab_21():
    c = d3.lab("rgba(165, 42, 42, 0.4)")
    assert approx_equal(
        c.darker(0.5), 29.149667346714935, 50.388769337115, 31.834059255569358, 0.4
    )
    assert approx_equal(
        c.darker(1), 20.149667346714935, 50.388769337115, 31.834059255569358, 0.4
    )
    assert approx_equal(
        c.darker(2), 2.149667346714935, 50.388769337115, 31.834059255569358, 0.4
    )


def test_lab_22():
    c1 = d3.lab("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker(1)
    assert approx_equal(
        c1, 51.98624890550498, -8.362792037014344, -32.832699449697685, 0.4
    )
    assert approx_equal(
        c2, 33.98624890550498, -8.362792037014344, -32.832699449697685, 0.4
    )


def test_lab_23():
    c1 = d3.lab("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker()
    c3 = c1.darker(1)
    assert approx_equal(c2, c3.l, c3.a, c3.b, 0.4)


def test_lab_24():
    c1 = d3.lab("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker(1.5)
    c3 = c1.brighter(-1.5)
    assert approx_equal(c2, c3.l, c3.a, c3.b, 0.4)


def test_lab_25():
    c = d3.lab(50, 4, -5, 0.4)
    r, g, b, opacity = 123, 117, 128, 0.4
    actual = c.rgb()
    c1 = isinstance(actual, RGB)
    c2 = math.isnan(actual.r) or round(actual.r) == round(r)
    c3 = math.isnan(actual.g) or round(actual.g) == round(g)
    c4 = math.isnan(actual.b) or round(actual.b) == round(b)
    c5 = math.isnan(actual.opacity) or round(actual.opacity) == round(opacity)
    assert all((c1, c2, c3, c4, c5))
