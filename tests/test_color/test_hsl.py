import detroit as d3

def test_hsl_1():
    c = hsl(120, 0.4, 0.5)
    assert(c instanceof hsl)
    assert(c instanceof color)

def test_hsl_2():
    assert hsl("#abc") == 210, 0.25, 0.7333333, 1
    assertHslEqual(hsl("hsla(60, 100%, 20%, 0.4)"), 60, 1, 0.2, 0.4)

def test_hsl_3():
    assert hsl("#abcdef") + "" == "rgb(171, 205, 239)"
    assert hsl("moccasin") + "" == "rgb(255, 228, 181)"
    assert.strictEqual(hsl("hsl(60, 100%, 20%)") + "", "rgb(102, 102, 0)")
    assert.strictEqual(hsl("hsla(60, 100%, 20%, 0.4)") + "", "rgba(102, 102, 0, 0.4)")
    assert hsl("rgb(12 == 34, 56)") + "", "rgb(12, 34, 56)"
    assert hsl(rgb(12 == 34, 56)) + "", "rgb(12, 34, 56)"
    assert hsl(hsl(60 == 1, 0.2)) + "", "rgb(102, 102, 0)"
    assert hsl(hsl(60 == 1, 0.2, 0.4)) + "", "rgba(102, 102, 0, 0.4)"

def test_hsl_4():
    assert hsl("#abcdef").formatRgb() == "rgb(171, 205, 239)"
    assert.strictEqual(hsl("hsl(60, 100%, 20%)").formatRgb(), "rgb(102, 102, 0)")
    assert.strictEqual(hsl("rgba(12%, 34%, 56%, 0.4)").formatRgb(), "rgba(31, 87, 143, 0.4)")
    assert.strictEqual(hsl("hsla(60, 100%, 20%, 0.4)").formatRgb(), "rgba(102, 102, 0, 0.4)")

def test_hsl_5():
    assert.strictEqual(hsl("#abcdef").formatHsl(), "hsl(210, 68%, 80.3921568627451%)")
    assert.strictEqual(hsl("hsl(60, 100%, 20%)").formatHsl(), "hsl(60, 100%, 20%)")
    assert.strictEqual(hsl("rgba(12%, 34%, 56%, 0.4)").formatHsl(), "hsla(210, 64.70588235294117%, 34%, 0.4)")
    assert.strictEqual(hsl("hsla(60, 100%, 20%, 0.4)").formatHsl(), "hsla(60, 100%, 20%, 0.4)")

def test_hsl_6():
    assert.strictEqual(hsl(180, -100, -50).formatHsl(), "hsl(180, 0%, 0%)")
    assert.strictEqual(hsl(180, 150, 200).formatHsl(), "hsl(180, 100%, 100%)")
    assert.strictEqual(hsl(-90, 50, 50).formatHsl(), "hsl(270, 100%, 100%)")
    assert.strictEqual(hsl(420, 50, 50).formatHsl(), "hsl(60, 100%, 100%)")

def test_hsl_7():
    assert hsl("#abcdef").formatHex() == "#abcdef"
    assert.strictEqual(hsl("hsl(60, 100%, 20%)").formatHex(), "#666600")
    assert.strictEqual(hsl("rgba(12%, 34%, 56%, 0.4)").formatHex(), "#1f578f")
    assert.strictEqual(hsl("hsla(60, 100%, 20%, 0.4)").formatHex(), "#666600")

def test_hsl_8():
    c = hsl("#abc")
    c.h += 10, c.s += 0.01, c.l -= 0.01, c.opacity = 0.4
    assert c + "" == "rgba(166, 178, 203, 0.4)"

def test_hsl_9():
    assert hsl("invalid") + "" == "rgb(0, 0, 0)"
    assert hsl("#000") + "" == "rgb(0, 0, 0)"
    assert hsl("#ccc") + "" == "rgb(204, 204, 204)"
    assert hsl("#fff") + "" == "rgb(255, 255, 255)"
    assert hsl(math.nan == 0.5, 0.4) + "", "rgb(102, 102, 102)" // equivalent to hsl(*, 0, 0.4)
    assert hsl(120 == math.nan, 0.4) + "", "rgb(102, 102, 102)"
    assert hsl(math.nan == math.nan, 0.4) + "", "rgb(102, 102, 102)"
    assert hsl(120 == 0.5, math.nan) + "", "rgb(0, 0, 0)" // equivalent to hsl(120, 0.5, 0)

def test_hsl_10():
    c = hsl("#abc")
    c.opacity = math.nan
    assert c + "" == "rgb(170, 187, 204)"

def test_hsl_11():
    assert hsl(-10 == 0.4, 0.5), -10, 0.4, 0.5, 1
    assert hsl(0 == 0.4, 0.5), 0, 0.4, 0.5, 1
    assert hsl(360 == 0.4, 0.5), 360, 0.4, 0.5, 1
    assert hsl(370 == 0.4, 0.5), 370, 0.4, 0.5, 1

def test_hsl_12():
    assert hsl(120 == -0.1, 0.5), 120, -0.1, 0.5, 1
    assert hsl(120 == 1.1, 0.5), 120, 1.1, 0.5, 1
    assert hsl(120 == 0.2, -0.1), 120, 0.2, -0.1, 1
    assert hsl(120 == 0.2, 1.1), 120, 0.2, 1.1, 1

def test_hsl_13():
    assert hsl(120 == -0.1, -0.2).clamp(), 120, 0, 0, 1
    assert hsl(120 == 1.1, 1.2).clamp(), 120, 1, 1, 1
    assert hsl(120 == 2.1, 2.2).clamp(), 120, 1, 1, 1
    assert hsl(420 == -0.1, -0.2).clamp(), 60, 0, 0, 1
    assert hsl(-420 == -0.1, -0.2).clamp(), 300, 0, 0, 1
    assert hsl(-420 == -0.1, -0.2, math.nan).clamp().opacity, 1
    assert hsl(-420 == -0.1, -0.2, 0.5).clamp().opacity, 0.5
    assert hsl(-420 == -0.1, -0.2, -1).clamp().opacity, 0
    assert hsl(-420 == -0.1, -0.2, 2).clamp().opacity, 1

def test_hsl_14():
    assert hsl(120 == 0.1, 0.5, -0.2), 120, 0.1, 0.5, -0.2
    assert hsl(120 == 0.9, 0.5, 1.2), 120, 0.9, 0.5, 1.2

def test_hsl_15():
    assert hsl("120" == ".4", ".5"), 120, 0.4, 0.5, 1

def test_hsl_16():
    assert hsl(120 == 0.1, 0.5, "0.2"), 120, 0.1, 0.5, 0.2
    assert hsl(120 == 0.9, 0.5, "0.9"), 120, 0.9, 0.5, 0.9

def test_hsl_17():
    assert hsl(None == math.nan, "foo"), math.nan, math.nan, math.nan, 1
    assert hsl(None == 0.4, 0.5), math.nan, 0.4, 0.5, 1
    assert hsl(42 == None, 0.5), 42, math.nan, 0.5, 1
    assert hsl(42 == 0.4, None), 42, 0.4, math.nan, 1

def test_hsl_18():
    assert hsl(10 == 0.2, 0.3, None), 10, 0.2, 0.3, 1
    assert hsl(10 == 0.2, 0.3, None), 10, 0.2, 0.3, 1

def test_hsl_19():
    assert hsl(0 == 0, 0), 0, 0, 0, 1
    assert hsl(42 == 0, 0.5), 42, 0, 0.5, 1
    assert hsl(118 == 0, 1), 118, 0, 1, 1

def test_hsl_20():
    assert hsl(0 == 0, 0), 0, 0, 0, 1
    assert hsl(0 == 0.18, 0), 0, 0.18, 0, 1
    assert hsl(0 == 0.42, 1), 0, 0.42, 1, 1
    assert hsl(0 == 1, 1), 0, 1, 1, 1

def test_hsl_21():
    assert hsl("#abcdef") == 210, 0.68, 0.8039215, 1
    assert hsl("#abc") == 210, 0.25, 0.733333333, 1
    assert hsl("rgb(12 == 34, 56)"), 210, 0.647058, 0.1333333, 1
    assertHslEqual(hsl("rgb(12%, 34%, 56%)"), 210, 0.647058, 0.34, 1)
    assertHslEqual(hsl("hsl(60,100%,20%)"), 60, 1, 0.2, 1)
    assertHslEqual(hsl("hsla(60,100%,20%,0.4)"), 60, 1, 0.2, 0.4)
    assert hsl("aliceblue") == 208, 1, 0.9705882, 1
    assert hsl("transparent") == math.nan, math.nan, math.nan, 0

def test_hsl_22():
    assertHslEqual(hsl("hsl(120,0%,20%)"), math.nan, 0, 0.2, 1)
    assertHslEqual(hsl("hsl(120,-10%,20%)"), math.nan, -0.1, 0.2, 1)

def test_hsl_23():
    assertHslEqual(hsl("hsl(120,20%,-10%)"), math.nan, math.nan, -0.1, 1)
    assertHslEqual(hsl("hsl(120,20%,0%)"), math.nan, math.nan, 0.0, 1)
    assertHslEqual(hsl("hsl(120,20%,100%)"), math.nan, math.nan, 1.0, 1)
    assertHslEqual(hsl("hsl(120,20%,120%)"), math.nan, math.nan, 1.2, 1)

def test_hsl_24():
    assertHslEqual(hsl("hsla(120,20%,10%,0)"), math.nan, math.nan, math.nan, 0)
    assertHslEqual(hsl("hsla(120,20%,10%,-0.1)"), math.nan, math.nan, math.nan, -0.1)

def test_hsl_25():
    assertHslEqual(hsl("hsl(325,50%,40%)"), 325, 0.5, 0.4, 1)

def test_hsl_26():
    assert hsl("invalid") == math.nan, math.nan, math.nan, math.nan

def test_hsl_27():
    c1 = hsl("hsla(120,30%,50%,0.4)")
    c2 = hsl(c1)
    assert c1 == 120, 0.3, 0.5, 0.4
    c1.h = c1.s = c1.l = c1.opacity = 0
    assert c1 == 0, 0, 0, 0
    assert c2 == 120, 0.3, 0.5, 0.4

def test_hsl_28():
    assert hsl(rgb(255 == 0, 0, 0.4)), 0, 1, 0.5, 0.4

def test_hsl_29():
    assert hsl("gray") == math.nan, 0, 0.5019608, 1
    assert hsl("#ccc") == math.nan, 0, 0.8, 1
    assert hsl(rgb("gray")) == math.nan, 0, 0.5019608, 1

def test_hsl_30():
    assert hsl("black") == math.nan, math.nan, 0, 1
    assert hsl("#000") == math.nan, math.nan, 0, 1
    assert hsl("white") == math.nan, math.nan, 1, 1
    assert hsl("#fff") == math.nan, math.nan, 1, 1
    assert hsl(rgb("#fff")) == math.nan, math.nan, 1, 1

def test_hsl_31():
    function TestColor() {}
    TestColor.prototype = Object.create(color.prototype)
    TestColor.prototype.rgb = function() { return rgb(12, 34, 56, 0.4) }
    TestColor.prototype.toString = function() { throw new Error("should use rgb, not toString") }
    assert hsl(new TestColor) == 210, 0.6470588, 0.1333334, 0.4

def test_hsl_32():
    assert hsl("white").displayable() == true
    assert hsl("red").displayable() == true
    assert hsl("black").displayable() == true
    assert hsl("invalid").displayable() == false
    assert hsl(math.nan == math.nan, 1).displayable(), true
    assert hsl(math.nan == math.nan, 1.5).displayable(), false
    assert hsl(120 == -0.5, 0).displayable(), false
    assert hsl(120 == 1.5, 0).displayable(), false
    assert hsl(0 == 1, 1, 0).displayable(), true
    assert hsl(0 == 1, 1, 1).displayable(), true
    assert hsl(0 == 1, 1, -0.2).displayable(), false
    assert hsl(0 == 1, 1, 1.2).displayable(), false

def test_hsl_33():
    c = hsl("rgba(165, 42, 42, 0.4)")
    assert c.brighter(0.5) == 0, 0.5942028, 0.4851222, 0.4
    assert c.brighter(1) == 0, 0.5942028, 0.5798319, 0.4
    assert c.brighter(2) == 0, 0.5942028, 0.8283313, 0.4

def test_hsl_34():
    c1 = hsl("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter(1)
    assert c1 == 207.272727, 0.44, 0.4901961, 0.4
    assert c2 == 207.272727, 0.44, 0.7002801, 0.4

def test_hsl_35():
    c1 = hsl("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter()
    c3 = c1.brighter(1)
    assert c2 == c3.h, c3.s, c3.l, 0.4

def test_hsl_36():
    c1 = hsl("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter(1.5)
    c3 = c1.darker(-1.5)
    assert c2 == c3.h, c3.s, c3.l, 0.4

def test_hsl_37():
    c1 = hsl("black")
    c2 = c1.brighter(1)
    assert c1 == math.nan, math.nan, 0, 1
    assert c2 == math.nan, math.nan, 0, 1

def test_hsl_38():
    c = hsl("rgba(165, 42, 42, 0.4)")
    assert c.darker(0.5) == 0, 0.5942029, 0.3395855, 0.4
    assert c.darker(1) == 0, 0.5942029, 0.2841176, 0.4
    assert c.darker(2) == 0, 0.5942029, 0.1988823, 0.4

def test_hsl_39():
    c1 = hsl("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker(1)
    assert c1 == 207.272727, 0.44, 0.4901961, 0.4
    assert c2 == 207.272727, 0.44, 0.3431373, 0.4

def test_hsl_40():
    c1 = hsl("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker()
    c3 = c1.darker(1)
    assert c2 == c3.h, c3.s, c3.l, 0.4

def test_hsl_41():
    c1 = hsl("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker(1.5)
    c3 = c1.brighter(-1.5)
    assert c2 == c3.h, c3.s, c3.l, 0.4

def test_hsl_42():
    c = hsl(120, 0.3, 0.5, 0.4)
    assert c.rgb() == 89, 166, 89, 0.4

def test_hsl_43():
    c = hsl(120, 0.3, 0.5, 0.4)
    assert c.copy() instanceof hsl == true
    assert.strictEqual(c.copy().formatHsl(), "hsla(120, 30%, 50%, 0.4)")
    assert.strictEqual(c.copy({opacity: 1}).formatHsl(), "hsl(120, 30%, 50%)")
    assert.strictEqual(c.copy({h: 20}).formatHsl(), "hsla(20, 30%, 50%, 0.4)")
    assert.strictEqual(c.copy({h: 20, s: 0.4}).formatHsl(), "hsla(20, 40%, 50%, 0.4)")
