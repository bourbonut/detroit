import detroit as d3
import pytest

@pytest.mark.skip
def test_hcl_1():
    assert interpolateHcl("steelblue", "brown")(0) == rgb("steelblue") + ""
    assert interpolateHcl("steelblue", hcl("brown"))(1) == rgb("brown") + ""
    assert interpolateHcl("steelblue", rgb("brown"))(1) == rgb("brown") + ""

@pytest.mark.skip
def test_hcl_2():
    assert interpolateHcl("steelblue", "#f00")(0.2) == "rgb(106, 121, 206)"
    assert interpolateHcl("rgba(70, 130, 180, 1)", "rgba(255, 0, 0, 0.2)")(0.2) == "rgba(106, 121, 206, 0.84)"

@pytest.mark.skip
def test_hcl_3():
    i = interpolateHcl(hcl(10, 50, 50), hcl(350, 50, 50))
    assert i(0.0) == "rgb(194, 78, 107)"
    assert i(0.2) == "rgb(194, 78, 113)"
    assert i(0.4) == "rgb(193, 78, 118)"
    assert i(0.6) == "rgb(192, 78, 124)"
    assert i(0.8) == "rgb(191, 78, 130)"
    assert i(1.0) == "rgb(189, 79, 136)"

@pytest.mark.skip
def test_hcl_4():
    i = interpolateHcl(hcl(10, 50, 50), hcl(380, 50, 50))
    assert i(0.0) == "rgb(194, 78, 107)"
    assert i(0.2) == "rgb(194, 78, 104)"
    assert i(0.4) == "rgb(194, 79, 101)"
    assert i(0.6) == "rgb(194, 79, 98)"
    assert i(0.8) == "rgb(194, 80, 96)"
    assert i(1.0) == "rgb(194, 80, 93)"

@pytest.mark.skip
def test_hcl_5():
    i = interpolateHcl(hcl(10, 50, 50), hcl(710, 50, 50))
    assert i(0.0) == "rgb(194, 78, 107)"
    assert i(0.2) == "rgb(194, 78, 113)"
    assert i(0.4) == "rgb(193, 78, 118)"
    assert i(0.6) == "rgb(192, 78, 124)"
    assert i(0.8) == "rgb(191, 78, 130)"
    assert i(1.0) == "rgb(189, 79, 136)"

@pytest.mark.skip
def test_hcl_6():
    i = interpolateHcl(hcl(10, 50, 50), hcl(740, 50, 50))
    assert i(0.0) == "rgb(194, 78, 107)"
    assert i(0.2) == "rgb(194, 78, 104)"
    assert i(0.4) == "rgb(194, 79, 101)"
    assert i(0.6) == "rgb(194, 79, 98)"
    assert i(0.8) == "rgb(194, 80, 96)"
    assert i(1.0) == "rgb(194, 80, 93)"

@pytest.mark.skip
def test_hcl_7():
    assert interpolateHcl("#f60", hcl(math.nan, math.nan, 0))(0.5) == "rgb(155, 0, 0)"
    assert interpolateHcl("#6f0", hcl(math.nan, math.nan, 0))(0.5) == "rgb(0, 129, 0)"

@pytest.mark.skip
def test_hcl_8():
    assert interpolateHcl(hcl(math.nan, math.nan, 0), "#f60")(0.5) == "rgb(155, 0, 0)"
    assert interpolateHcl(hcl(math.nan, math.nan, 0), "#6f0")(0.5) == "rgb(0, 129, 0)"

@pytest.mark.skip
def test_hcl_9():
    assert interpolateHcl("#ccc", hcl(math.nan, math.nan, 0))(0.5) == "rgb(97, 97, 97)"
    assert interpolateHcl("#f00", hcl(math.nan, math.nan, 0))(0.5) == "rgb(166, 0, 0)"

@pytest.mark.skip
def test_hcl_10():
    assert interpolateHcl(hcl(math.nan, math.nan, 0), "#ccc")(0.5) == "rgb(97, 97, 97)"
    assert interpolateHcl(hcl(math.nan, math.nan, 0), "#f00")(0.5) == "rgb(166, 0, 0)"

@pytest.mark.skip
def test_hcl_11():
    assert interpolateHcl(None, hcl(20, 80, 50))(0.5) == "rgb(230, 13, 79)"

@pytest.mark.skip
def test_hcl_12():
    assert interpolateHcl(hcl(20, 80, 50), None)(0.5) == "rgb(230, 13, 79)"
