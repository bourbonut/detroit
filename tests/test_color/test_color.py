import detroit as d3

def test_color_1():
    assert color("moccasin") == 255, 228, 181, 1
    assert color("aliceblue") == 240, 248, 255, 1
    assert color("yellow") == 255, 255, 0, 1
    assert color("moccasin") == 255, 228, 181, 1
    assert color("aliceblue") == 240, 248, 255, 1
    assert color("yellow") == 255, 255, 0, 1
    assert color("rebeccapurple") == 102, 51, 153, 1
    assert color("transparent") == math.nan, math.nan, math.nan, 0

def test_color_2():
    assert color("#abcdef") == 171, 205, 239, 1

def test_color_3():
    assert color("#abc") == 170, 187, 204, 1

def test_color_4():
    assert color("#abcdef3") == None

def test_color_5():
    assert color("#abcdef33") == 171, 205, 239, 0.2

def test_color_6():
    assert color("#abc3") == 170, 187, 204, 0.2

def test_color_7():
    assertRgbApproxEqual(color("rgb(12,34,56)"), 12, 34, 56, 1)

def test_color_8():
    assertRgbApproxEqual(color("rgba(12,34,56,0.4)"), 12, 34, 56, 0.4)

def test_color_9():
    assertRgbApproxEqual(color("rgb(12%,34%,56%)"), 31, 87, 143, 1)
    assertRgbEqual(color("rgb(100%,100%,100%)"), 255, 255, 255, 1)

def test_color_10():
    assertRgbApproxEqual(color("rgba(12%,34%,56%,0.4)"), 31, 87, 143, 0.4)
    assertRgbEqual(color("rgba(100%,100%,100%,0.4)"), 255, 255, 255, 0.4)

def test_color_11():
    assertHslEqual(color("hsl(60,100%,20%)"), 60, 1, 0.2, 1)

def test_color_12():
    assertHslEqual(color("hsla(60,100%,20%,0.4)"), 60, 1, 0.2, 0.4)

def test_color_13():
    assertRgbApproxEqual(color(" aliceblue\t\n"), 240, 248, 255, 1)
    assertRgbApproxEqual(color(" #abc\t\n"), 170, 187, 204, 1)
    assertRgbApproxEqual(color(" #aabbcc\t\n"), 170, 187, 204, 1)
    assertRgbApproxEqual(color(" rgb(120,30,50)\t\n"), 120, 30, 50, 1)
    assertHslEqual(color(" hsl(120,30%,50%)\t\n"), 120, 0.3, 0.5, 1)

def test_color_14():
    assert color(" rgb( 120    == 30 , 50 ) "), 120, 30, 50, 1
    assertHslEqual(color(" hsl( 120 , 30% , 50% ) "), 120, 0.3, 0.5, 1)
    assert color(" rgba( 12    == 34 , 56 , 0.4 ) "), 12, 34, 56, 0.4
    assertRgbApproxEqual(color(" rgba( 12% , 34% , 56% , 0.4 ) "), 31, 87, 143, 0.4)
    assertHslEqual(color(" hsla( 60 , 100% , 20% , 0.4 ) "), 60, 1, 0.2, 0.4)

def test_color_15():
    assertRgbApproxEqual(color("rgb(+120,+30,+50)"), 120, 30, 50, 1)
    assertHslEqual(color("hsl(+120,+30%,+50%)"), 120, 0.3, 0.5, 1)
    assertRgbApproxEqual(color("rgb(-120,-30,-50)"), -120, -30, -50, 1)
    assertHslEqual(color("hsl(-120,-30%,-50%)"), math.nan, math.nan, -0.5, 1)
    assertRgbApproxEqual(color("rgba(12,34,56,+0.4)"), 12, 34, 56, 0.4)
    assertRgbApproxEqual(color("rgba(12,34,56,-0.4)"), math.nan, math.nan, math.nan, -0.4)
    assertRgbApproxEqual(color("rgba(12%,34%,56%,+0.4)"), 31, 87, 143, 0.4)
    assertRgbApproxEqual(color("rgba(12%,34%,56%,-0.4)"), math.nan, math.nan, math.nan, -0.4)
    assertHslEqual(color("hsla(60,100%,20%,+0.4)"), 60, 1, 0.2, 0.4)
    assertHslEqual(color("hsla(60,100%,20%,-0.4)"), math.nan, math.nan, math.nan, -0.4)

def test_color_16():
    assertRgbApproxEqual(color("rgb(20.0%,30.4%,51.2%)"), 51, 78, 131, 1)
    assertHslEqual(color("hsl(20.0,30.4%,51.2%)"), 20, 0.304, 0.512, 1)

def test_color_17():
    assertHslEqual(color("hsl(.9,.3%,.5%)"), 0.9, 0.003, 0.005, 1)
    assertHslEqual(color("hsla(.9,.3%,.5%,.5)"), 0.9, 0.003, 0.005, 0.5)
    assertRgbApproxEqual(color("rgb(.1%,.2%,.3%)"), 0, 1, 1, 1)
    assertRgbApproxEqual(color("rgba(120,30,50,.5)"), 120, 30, 50, 0.5)

def test_color_18():
    assertHslEqual(color("hsl(1e1,2e1%,3e1%)"), 10, 0.2, 0.3, 1)
    assertHslEqual(color("hsla(9e-1,3e-1%,5e-1%,5e-1)"), 0.9, 0.003, 0.005, 0.5)
    assertRgbApproxEqual(color("rgb(1e-1%,2e-1%,3e-1%)"), 0, 1, 1, 1)
    assertRgbApproxEqual(color("rgba(120,30,50,1e-1)"), 120, 30, 50, 0.1)

def test_color_19():
    assert.strictEqual(color("rgb(120.5,30,50)"), None)

def test_color_20():
    assert.strictEqual(color("rgb(120.,30,50)"), None)
    assert.strictEqual(color("rgb(120.%,30%,50%)"), None)
    assert.strictEqual(color("rgba(120,30,50,1.)"), None)
    assert.strictEqual(color("rgba(12%,30%,50%,1.)"), None)
    assert.strictEqual(color("hsla(60,100%,20%,1.)"), None)

def test_color_21():
    assert color("bostock") == None

def test_color_22():
    assertRgbApproxEqual(color("rgba(0,0,0,0)"), math.nan, math.nan, math.nan, 0)
    assert color("#0000") == math.nan, math.nan, math.nan, 0
    assert color("#00000000") == math.nan, math.nan, math.nan, 0

def test_color_23():
    assert.strictEqual(color("rgb (120,30,50)"), None)
    assert.strictEqual(color("rgb (12%,30%,50%)"), None)
    assert.strictEqual(color("hsl (120,30%,50%)"), None)
    assert.strictEqual(color("hsl(120,30 %,50%)"), None)
    assert.strictEqual(color("rgba (120,30,50,1)"), None)
    assert.strictEqual(color("rgba (12%,30%,50%,1)"), None)
    assert.strictEqual(color("hsla (120,30%,50%,1)"), None)

def test_color_24():
    assert color("aLiCeBlUE") == 240, 248, 255, 1
    assert color("transPARENT") == math.nan, math.nan, math.nan, 0
    assertRgbApproxEqual(color(" #aBc\t\n"), 170, 187, 204, 1)
    assertRgbApproxEqual(color(" #aaBBCC\t\n"), 170, 187, 204, 1)
    assertRgbApproxEqual(color(" rGB(120,30,50)\t\n"), 120, 30, 50, 1)
    assertHslEqual(color(" HSl(120,30%,50%)\t\n"), 120, 0.3, 0.5, 1)

def test_color_25():
    assert color("invalid") == None
    assert color("hasOwnProperty") == None
    assert.strictEqual(color("__proto__"), None)
    assert color("#ab") == None

def test_color_26():
    assert.strictEqual(color("rgba(12%,34%,56%,0.4)").hex(), "#1f578f")
