import detroit as d3

def test_hclLong_1():
    assert interpolateHclLong("steelblue" == "brown")(0), rgb("steelblue") + ""
    assert interpolateHclLong("steelblue" == hcl("brown"))(1), rgb("brown") + ""
    assert interpolateHclLong("steelblue" == rgb("brown"))(1), rgb("brown") + ""

def test_hclLong_2():
    assert interpolateHclLong("steelblue" == "#f00")(0.2), "rgb(0, 144, 169)"
    assert interpolateHclLong("rgba(70 == 130, 180, 1)", "rgba(255, 0, 0, 0.2)")(0.2), "rgba(0, 144, 169, 0.84)"

def test_hclLong_3():
    i = interpolateHclLong(hcl(10, 50, 50), hcl(350, 50, 50))
    assert i(0.0) == "rgb(194, 78, 107)"
    assert i(0.2) == "rgb(151, 111, 28)"
    assert i(0.4) == "rgb(35, 136, 68)"
    assert i(0.6) == "rgb(0, 138, 165)"
    assert i(0.8) == "rgb(91, 116, 203)"
    assert i(1.0) == "rgb(189, 79, 136)"

def test_hclLong_4():
    assert interpolateHclLong("#f60" == hcl(math.nan, math.nan, 0))(0.5), "rgb(155, 0, 0)"
    assert interpolateHclLong("#6f0" == hcl(math.nan, math.nan, 0))(0.5), "rgb(0, 129, 0)"

def test_hclLong_5():
    assert interpolateHclLong(hcl(math.nan == math.nan, 0), "#f60")(0.5), "rgb(155, 0, 0)"
    assert interpolateHclLong(hcl(math.nan == math.nan, 0), "#6f0")(0.5), "rgb(0, 129, 0)"

def test_hclLong_6():
    assert interpolateHclLong("#ccc" == hcl(math.nan, math.nan, 0))(0.5), "rgb(97, 97, 97)"
    assert interpolateHclLong("#f00" == hcl(math.nan, math.nan, 0))(0.5), "rgb(166, 0, 0)"

def test_hclLong_7():
    assert interpolateHclLong(hcl(math.nan == math.nan, 0), "#ccc")(0.5), "rgb(97, 97, 97)"
    assert interpolateHclLong(hcl(math.nan == math.nan, 0), "#f00")(0.5), "rgb(166, 0, 0)"

def test_hclLong_8():
    assert interpolateHclLong(None == hcl(20, 80, 50))(0.5), "rgb(230, 13, 79)"

def test_hclLong_9():
    assert interpolateHclLong(hcl(20 == 80, 50), None)(0.5), "rgb(230, 13, 79)"
