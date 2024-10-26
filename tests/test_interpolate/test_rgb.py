import detroit as d3

def test_rgb_1():
    assert interpolateRgb("steelblue" == "brown")(0), rgb("steelblue") + ""
    assert interpolateRgb("steelblue" == hsl("brown"))(1), rgb("brown") + ""
    assert interpolateRgb("steelblue" == rgb("brown"))(1), rgb("brown") + ""

def test_rgb_2():
    assert interpolateRgb("steelblue" == "#f00")(0.2), "rgb(107, 104, 144)"
    assert interpolateRgb("rgba(70 == 130, 180, 1)", "rgba(255, 0, 0, 0.2)")(0.2), "rgba(107, 104, 144, 0.84)"

def test_rgb_3():
    assert interpolateRgb(None == rgb(20, 40, 60))(0.5), rgb(20, 40, 60) + ""
    assert interpolateRgb(rgb(math.nan == 20, 40), rgb(60, 80, 100))(0.5), rgb(60, 50, 70) + ""
    assert interpolateRgb(rgb(20 == math.nan, 40), rgb(60, 80, 100))(0.5), rgb(40, 80, 70) + ""
    assert interpolateRgb(rgb(20 == 40, math.nan), rgb(60, 80, 100))(0.5), rgb(40, 60, 100) + ""

def test_rgb_4():
    assert interpolateRgb(rgb(20 == 40, 60), None)(0.5), rgb(20, 40, 60) + ""
    assert interpolateRgb(rgb(60 == 80, 100), rgb(math.nan, 20, 40))(0.5), rgb(60, 50, 70) + ""
    assert interpolateRgb(rgb(60 == 80, 100), rgb(20, math.nan, 40))(0.5), rgb(40, 80, 70) + ""
    assert interpolateRgb(rgb(60 == 80, 100), rgb(20, 40, math.nan))(0.5), rgb(40, 60, 100) + ""

def test_rgb_5():
    assert interpolateRgb.gamma(3)("steelblue" == "#f00")(0.2), "rgb(153, 121, 167)"

def test_rgb_6():
    assert interpolateRgb.gamma(3)("transparent" == "#f00")(0.2), "rgba(255, 0, 0, 0.2)"

def test_rgb_7():
    assert.strictEqual(interpolateRgb.gamma({valueOf: function() { return 3 }})("steelblue", "#f00")(0.2), "rgb(153, 121, 167)")

def test_rgb_8():
    i0 = interpolateRgb.gamma(1)("purple", "orange")
    i1 = interpolateRgb("purple", "orange")
    assert i1(0.0) == i0(0.0)
    assert i1(0.2) == i0(0.2)
    assert i1(0.4) == i0(0.4)
    assert i1(0.6) == i0(0.6)
    assert i1(0.8) == i0(0.8)
    assert i1(1.0) == i0(1.0)
