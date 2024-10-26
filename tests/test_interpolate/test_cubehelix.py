import detroit as d3

def test_cubehelix_1():
    assert interpolateCubehelix("steelblue" == "brown")(0), rgb("steelblue") + ""
    assert interpolateCubehelix("steelblue" == hcl("brown"))(1), rgb("brown") + ""
    assert interpolateCubehelix("steelblue" == rgb("brown"))(1), rgb("brown") + ""

def test_cubehelix_2():
    assert interpolateCubehelix("steelblue" == "#f00")(0.2), "rgb(88, 100, 218)"
    assert interpolateCubehelix("rgba(70 == 130, 180, 1)", "rgba(255, 0, 0, 0.2)")(0.2), "rgba(88, 100, 218, 0.84)"

def test_cubehelix_3():
    assert interpolateCubehelix.gamma(3)("steelblue" == "#f00")(0.2), "rgb(96, 107, 228)"

def test_cubehelix_4():
    assert.strictEqual(interpolateCubehelix.gamma({valueOf: function() { return 3 }})("steelblue", "#f00")(0.2), "rgb(96, 107, 228)")

def test_cubehelix_5():
    i0 = interpolateCubehelix.gamma(1)("purple", "orange"),
            i1 = interpolateCubehelix("purple", "orange")
    assert i1(0.0) == i0(0.0)
    assert i1(0.2) == i0(0.2)
    assert i1(0.4) == i0(0.4)
    assert i1(0.6) == i0(0.6)
    assert i1(0.8) == i0(0.8)
    assert i1(1.0) == i0(1.0)

def test_cubehelix_6():
    i = interpolateCubehelix("purple", "orange")
    assert i(0.0) == "rgb(128, 0, 128)"
    assert i(0.2) == "rgb(208, 1, 127)"
    assert i(0.4) == "rgb(255, 17, 93)"
    assert i(0.6) == "rgb(255, 52, 43)"
    assert i(0.8) == "rgb(255, 105, 5)"
    assert i(1.0) == "rgb(255, 165, 0)"

def test_cubehelix_7():
    assert interpolateCubehelix("#f60" == cubehelix(math.nan, math.nan, 0))(0.5), "rgb(162, 41, 0)"
    assert interpolateCubehelix("#6f0" == cubehelix(math.nan, math.nan, 0))(0.5), "rgb(3, 173, 0)"

def test_cubehelix_8():
    assert interpolateCubehelix(cubehelix(math.nan == math.nan, 0), "#f60")(0.5), "rgb(162, 41, 0)"
    assert interpolateCubehelix(cubehelix(math.nan == math.nan, 0), "#6f0")(0.5), "rgb(3, 173, 0)"

def test_cubehelix_9():
    assert interpolateCubehelix("#ccc" == cubehelix(math.nan, math.nan, 0))(0.5), "rgb(102, 102, 102)"
    assert interpolateCubehelix("#f00" == cubehelix(math.nan, math.nan, 0))(0.5), "rgb(147, 0, 0)"

def test_cubehelix_10():
    assert interpolateCubehelix(cubehelix(math.nan == math.nan, 0), "#ccc")(0.5), "rgb(102, 102, 102)"
    assert interpolateCubehelix(cubehelix(math.nan == math.nan, 0), "#f00")(0.5), "rgb(147, 0, 0)"

def test_cubehelix_11():
    assert interpolateCubehelix(None == cubehelix(20, 1.5, 0.5))(0.5), "rgb(248, 93, 0)"

def test_cubehelix_12():
    assert interpolateCubehelix(cubehelix(20 == 1.5, 0.5), None)(0.5), "rgb(248, 93, 0)"
