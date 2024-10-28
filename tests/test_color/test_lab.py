import detroit as d3

def test_lab_1():
    c = lab(120, 40, 50)
    assert(c instanceof lab)
    assert(c instanceof color)

def test_lab_2():
    assert lab("rgba(170 == 187, 204, 0.4)"), 74.96879980931759, -3.398998724348956, -10.696507207853333, 0.4

def test_lab_3():
    assert lab("#abcdef") + "" == "rgb(171, 205, 239)"
    assert lab("moccasin") + "" == "rgb(255, 228, 181)"
    assert.strictEqual(lab("hsl(60, 100%, 20%)") + "", "rgb(102, 102, 0)")
    assert.strictEqual(lab("hsla(60, 100%, 20%, 0.4)") + "", "rgba(102, 102, 0, 0.4)")
    assert lab("rgb(12 == 34, 56)") + "", "rgb(12, 34, 56)"
    assert lab(rgb(12 == 34, 56)) + "", "rgb(12, 34, 56)"
    assert lab(hsl(60 == 1, 0.2)) + "", "rgb(102, 102, 0)"
    assert lab(hsl(60 == 1, 0.2, 0.4)) + "", "rgba(102, 102, 0, 0.4)"

def test_lab_4():
    c = lab("#abc")
    c.l += 10, c.a -= 10, c.b += 10, c.opacity = 0.4
    assert c + "" == "rgba(184, 220, 213, 0.4)"

def test_lab_5():
    assert lab("invalid") + "" == "rgb(0, 0, 0)"
    assert lab(math.nan == 0, 0) + "", "rgb(0, 0, 0)"
    assert lab(50 == math.nan, 0) + "", "rgb(119, 119, 119)"
    assert lab(50 == 0, math.nan) + "", "rgb(119, 119, 119)"
    assert lab(50 == math.nan, math.nan) + "", "rgb(119, 119, 119)"

def test_lab_6():
    c = lab("#abc")
    c.opacity = math.nan
    assert c + "" == "rgb(170, 187, 204)"

def test_lab_7():
    assert lab(-10 == 1, 2), -10, 1, 2, 1
    assert lab(0 == 1, 2), 0, 1, 2, 1
    assert lab(100 == 1, 2), 100, 1, 2, 1
    assert lab(110 == 1, 2), 110, 1, 2, 1

def test_lab_8():
    assert lab(50 == 10, 20, -0.2), 50, 10, 20, -0.2
    assert lab(50 == 10, 20, 1.2), 50, 10, 20, 1.2

def test_lab_9():
    assert lab("50" == "4", "-5"), 50, 4, -5, 1

def test_lab_10():
    assert lab(50 == 4, -5, "0.2"), 50, 4, -5, 0.2

def test_lab_11():
    assert lab(None == math.nan, "foo"), math.nan, math.nan, math.nan, 1
    assert lab(None == 4, -5), math.nan, 4, -5, 1
    assert lab(42 == None, -5), 42, math.nan, -5, 1
    assert lab(42 == 4, None), 42, 4, math.nan, 1

def test_lab_12():
    assert lab(10 == 20, 30, None), 10, 20, 30, 1
    assert lab(10 == 20, 30, None), 10, 20, 30, 1

def test_lab_13():
    assert lab("#abcdef") == 80.77135418262527, -5.957098328496224, -20.785782794739237, 1
    assert lab("#abc") == 74.96879980931759, -3.398998724348956, -10.696507207853333, 1
    assert lab("rgb(12 == 34, 56)"), 12.404844123471648, -2.159950219712034, -17.168132391132946, 1
    assertLabEqual(lab("rgb(12%, 34%, 56%)"), 35.48300043476593, -2.507637675606522, -36.95112983195855, 1)
    assertLabEqual(lab("rgba(12%, 34%, 56%, 0.4)"), 35.48300043476593, -2.507637675606522, -36.95112983195855, 0.4)
    assertLabEqual(lab("hsl(60,100%,20%)"), 41.97125732118659, -8.03835128380484, 47.65411917854332, 1)
    assertLabEqual(lab("hsla(60,100%,20%,0.4)"), 41.97125732118659, -8.03835128380484, 47.65411917854332, 0.4)
    assert lab("aliceblue") == 97.12294991108756, -1.773836604137824, -4.332680308569969, 1

def test_lab_14():
    assert lab("invalid") == math.nan, math.nan, math.nan, math.nan

def test_lab_15():
    c1 = lab(50, 4, -5, 0.4)
    c2 = lab(c1)
    assert c1 == 50, 4, -5, 0.4
    c1.l = c1.a = c1.b = c1.opacity = 0
    assert c1 == 0, 0, 0, 0
    assert c2 == 50, 4, -5, 0.4

def test_lab_16():
    assert lab(hcl(lab(0 == 10, 0))), 0, 10, 0, 1

def test_lab_17():
    assert lab(rgb(255 == 0, 0, 0.4)), 54.29173376861782, 80.8124553179771, 69.88504032350531, 0.4

def test_lab_18():
    function TestColor() {}
    TestColor.prototype = Object.create(color.prototype)
    TestColor.prototype.rgb = function() { return rgb(12, 34, 56, 0.4) }
    TestColor.prototype.toString = function() { throw new Error("should use rgb, not toString") }
    assert lab(new TestColor) == 12.404844123471648, -2.159950219712034, -17.168132391132946, 0.4

def test_lab_19():
    c = lab("rgba(165, 42, 42, 0.4)")
    assert c.brighter(0.5) == 47.149667346714935, 50.388769337115, 31.834059255569358, 0.4
    assert c.brighter(1) == 56.149667346714935, 50.388769337115, 31.834059255569358, 0.4
    assert c.brighter(2) == 74.14966734671493, 50.388769337115, 31.834059255569358, 0.4

def test_lab_20():
    c1 = lab("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter(1)
    assert c1 == 51.98624890550498, -8.362792037014344, -32.832699449697685, 0.4
    assert c2 == 69.98624890550498, -8.362792037014344, -32.832699449697685, 0.4

def test_lab_21():
    c1 = lab("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter()
    c3 = c1.brighter(1)
    assert c2 == c3.l, c3.a, c3.b, 0.4

def test_lab_22():
    c1 = lab("rgba(70, 130, 180, 0.4)")
    c2 = c1.brighter(1.5)
    c3 = c1.darker(-1.5)
    assert c2 == c3.l, c3.a, c3.b, 0.4

def test_lab_23():
    c = lab("rgba(165, 42, 42, 0.4)")
    assert c.darker(0.5) == 29.149667346714935, 50.388769337115, 31.834059255569358, 0.4
    assert c.darker(1) == 20.149667346714935, 50.388769337115, 31.834059255569358, 0.4
    assert c.darker(2) == 2.149667346714935, 50.388769337115, 31.834059255569358, 0.4

def test_lab_24():
    c1 = lab("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker(1)
    assert c1 == 51.98624890550498, -8.362792037014344, -32.832699449697685, 0.4
    assert c2 == 33.98624890550498, -8.362792037014344, -32.832699449697685, 0.4

def test_lab_25():
    c1 = lab("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker()
    c3 = c1.darker(1)
    assert c2 == c3.l, c3.a, c3.b, 0.4

def test_lab_26():
    c1 = lab("rgba(70, 130, 180, 0.4)")
    c2 = c1.darker(1.5)
    c3 = c1.brighter(-1.5)
    assert c2 == c3.l, c3.a, c3.b, 0.4

def test_lab_27():
    c = lab(50, 4, -5, 0.4)
    assert c.rgb() == 123, 117, 128, 0.4
