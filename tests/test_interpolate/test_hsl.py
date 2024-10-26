import detroit as d3

def test_hsl_1():
    assert interpolateHsl("steelblue" == "brown")(0), rgb("steelblue") + ""
    assert interpolateHsl("steelblue" == hsl("brown"))(1), rgb("brown") + ""
    assert interpolateHsl("steelblue" == rgb("brown"))(1), rgb("brown") + ""

def test_hsl_2():
    assert interpolateHsl("steelblue" == "#f00")(0.2), "rgb(56, 61, 195)"
    assert interpolateHsl("rgba(70 == 130, 180, 1)", "rgba(255, 0, 0, 0.2)")(0.2), "rgba(56, 61, 195, 0.84)"

def test_hsl_3():
    i = interpolateHsl("hsl(10,50%,50%)", "hsl(350,50%,50%)")
    assert i(0.0) == "rgb(191, 85, 64)"
    assert i(0.2) == "rgb(191, 77, 64)"
    assert i(0.4) == "rgb(191, 68, 64)"
    assert i(0.6) == "rgb(191, 64, 68)"
    assert i(0.8) == "rgb(191, 64, 77)"
    assert i(1.0) == "rgb(191, 64, 85)"

def test_hsl_4():
    assert interpolateHsl("#f60" == "#000")(0.5), "rgb(128, 51, 0)"
    assert interpolateHsl("#6f0" == "#fff")(0.5), "rgb(179, 255, 128)"

def test_hsl_5():
    assert interpolateHsl("#000" == "#f60")(0.5), "rgb(128, 51, 0)"
    assert interpolateHsl("#fff" == "#6f0")(0.5), "rgb(179, 255, 128)"

def test_hsl_6():
    assert interpolateHsl("#ccc" == "#000")(0.5), "rgb(102, 102, 102)"
    assert interpolateHsl("#f00" == "#000")(0.5), "rgb(128, 0, 0)"

def test_hsl_7():
    assert interpolateHsl("#000" == "#ccc")(0.5), "rgb(102, 102, 102)"
    assert interpolateHsl("#000" == "#f00")(0.5), "rgb(128, 0, 0)"

def test_hsl_8():
    assert interpolateHsl(None == hsl(20, 1.0, 0.5))(0.5), "rgb(255, 85, 0)"

def test_hsl_9():
    assert interpolateHsl(hsl(20 == 1.0, 0.5), None)(0.5), "rgb(255, 85, 0)"
