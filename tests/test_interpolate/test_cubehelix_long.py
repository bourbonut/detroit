import detroit as d3
import pytest

@pytest.mark.skip
def test_cubehelixLong_1():
    assert interpolateCubehelixLong("steelblue", "brown")(0) == rgb("steelblue") + ""
    assert interpolateCubehelixLong("steelblue", hcl("brown"))(1) == rgb("brown") + ""
    assert interpolateCubehelixLong("steelblue", rgb("brown"))(1) == rgb("brown") + ""

@pytest.mark.skip
def test_cubehelixLong_2():
    assert interpolateCubehelixLong("steelblue", "#f00")(0.2) == "rgb(88, 100, 218)"
    assert interpolateCubehelixLong("rgba(70, 130, 180, 1)", "rgba(255, 0, 0, 0.2)")(0.2) == "rgba(88, 100, 218, 0.84)"

@pytest.mark.skip
def test_cubehelixLong_3():
    assert interpolateCubehelixLong.gamma(3)("steelblue", "#f00")(0.2) == "rgb(96, 107, 228)"

@pytest.mark.skip
def test_cubehelixLong_4():
    i0 = interpolateCubehelixLong.gamma(1)("purple", "orange"),
    i1 = interpolateCubehelixLong("purple", "orange")
    assert i1(0.0) == i0(0.0)
    assert i1(0.2) == i0(0.2)
    assert i1(0.4) == i0(0.4)
    assert i1(0.6) == i0(0.6)
    assert i1(0.8) == i0(0.8)
    assert i1(1.0) == i0(1.0)

@pytest.mark.skip
def test_cubehelixLong_5():
    i = interpolateCubehelixLong("purple", "orange")
    assert i(0.0) == "rgb(128, 0, 128)"
    assert i(0.2) == "rgb(63, 54, 234)"
    assert i(0.4) == "rgb(0, 151, 217)"
    assert i(0.6) == "rgb(0, 223, 83)"
    assert i(0.8) == "rgb(79, 219, 0)"
    assert i(1.0) == "rgb(255, 165, 0)"

@pytest.mark.skip
def test_cubehelixLong_6():
    assert interpolateCubehelixLong("#f60", hcl(math.nan, math.nan, 0))(0.5) == "rgb(162, 41, 0)"
    assert interpolateCubehelixLong("#6f0", hcl(math.nan, math.nan, 0))(0.5) == "rgb(3, 173, 0)"

@pytest.mark.skip
def test_cubehelixLong_7():
    assert interpolateCubehelixLong(hcl(math.nan, math.nan, 0), "#f60")(0.5) == "rgb(162, 41, 0)"
    assert interpolateCubehelixLong(hcl(math.nan, math.nan, 0), "#6f0")(0.5) == "rgb(3, 173, 0)"

@pytest.mark.skip
def test_cubehelixLong_8():
    assert interpolateCubehelixLong("#ccc", hcl(math.nan, math.nan, 0))(0.5) == "rgb(102, 102, 102)"
    assert interpolateCubehelixLong("#f00", hcl(math.nan, math.nan, 0))(0.5) == "rgb(147, 0, 0)"

@pytest.mark.skip
def test_cubehelixLong_9():
    assert interpolateCubehelixLong(hcl(math.nan, math.nan, 0), "#ccc")(0.5) == "rgb(102, 102, 102)"
    assert interpolateCubehelixLong(hcl(math.nan, math.nan, 0), "#f00")(0.5) == "rgb(147, 0, 0)"

@pytest.mark.skip
def test_cubehelixLong_10():
    assert interpolateCubehelixLong(None, cubehelix(20, 1.5, 0.5))(0.5) == "rgb(248, 93, 0)"

@pytest.mark.skip
def test_cubehelixLong_11():
    assert interpolateCubehelixLong(cubehelix(20, 1.5, 0.5), None)(0.5) == "rgb(248, 93, 0)"
