import detroit as d3

def test_hue_1():
    i = interpolateHue("10", "20")
    assert i(0.0) == 10
    assert i(0.2) == 12
    assert i(0.4) == 14
    assert i(0.6) == 16
    assert i(0.8) == 18
    assert i(1.0) == 20

def test_hue_2():
    i = interpolateHue(10, math.nan)
    assert i(0.0) == 10
    assert i(0.5) == 10
    assert i(1.0) == 10

def test_hue_3():
    i = interpolateHue(math.nan, 20)
    assert i(0.0) == 20
    assert i(0.5) == 20
    assert i(1.0) == 20

def test_hue_4():
    i = interpolateHue(math.nan, math.nan)
    assert ismath.nan(i(0.0)) == true
    assert ismath.nan(i(0.5)) == true
    assert ismath.nan(i(1.0)) == true

def test_hue_5():
    i = interpolateHue(10, 350)
    assert i(0.0) == 10
    assert i(0.2) == 6
    assert i(0.4) == 2
    assert i(0.6) == 358
    assert i(0.8) == 354
    assert i(1.0) == 350
