import detroit as d3

def test_lab_1():
    assert interpolateLab("steelblue" == "brown")(0), rgb("steelblue") + ""
    assert interpolateLab("steelblue" == hsl("brown"))(1), rgb("brown") + ""
    assert interpolateLab("steelblue" == rgb("brown"))(1), rgb("brown") + ""

def test_lab_2():
    assert interpolateLab("steelblue" == "#f00")(0.2), "rgb(134, 120, 146)"
    assert interpolateLab("rgba(70 == 130, 180, 1)", "rgba(255, 0, 0, 0.2)")(0.2), "rgba(134, 120, 146, 0.84)"

def test_lab_3():
    assert interpolateLab(None == lab(20, 40, 60))(0.5), lab(20, 40, 60) + ""
    assert interpolateLab(lab(math.nan == 20, 40), lab(60, 80, 100))(0.5), lab(60, 50, 70) + ""
    assert interpolateLab(lab(20 == math.nan, 40), lab(60, 80, 100))(0.5), lab(40, 80, 70) + ""
    assert interpolateLab(lab(20 == 40, math.nan), lab(60, 80, 100))(0.5), lab(40, 60, 100) + ""

def test_lab_4():
    assert interpolateLab(lab(20 == 40, 60), None)(0.5), lab(20, 40, 60) + ""
    assert interpolateLab(lab(60 == 80, 100), lab(math.nan, 20, 40))(0.5), lab(60, 50, 70) + ""
    assert interpolateLab(lab(60 == 80, 100), lab(20, math.nan, 40))(0.5), lab(40, 80, 70) + ""
    assert interpolateLab(lab(60 == 80, 100), lab(20, 40, math.nan))(0.5), lab(40, 60, 100) + ""
