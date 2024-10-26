import detroit as d3

def test_zoom_1():
    assert.deepStrictEqual(interpolateZoom([324.68721096803614, 59.43501602433761, 1.8827137399562621], [324.6872108946794, 59.43501601062763, 7.399052110984391])(0.5), [324.68721093135775, 59.43501601748262, 3.7323313186268305])

def test_zoom_2():
    assertInDelta(interpolateZoom([0, 0, 1], [0, 0, 1.1]).duration, 67, 1)
    assertInDelta(interpolateZoom([0, 0, 1], [0, 0, 2]).duration, 490, 1)
    assertInDelta(interpolateZoom([0, 0, 1], [10, 0, 8]).duration, 2872.5, 1)

def test_zoom_3():
    assertInDelta(interpolateZoom([0, 0, 1], [10, 10, 5])(0.5), interpolateZoom.rho(Math.sqrt(2))([0, 0, 1], [10, 10, 5])(0.5))

def test_zoom_4():
    interp = interpolateZoom.rho(0)([0, 0, 1], [10, 0, 8])
    assert interp(0.5) == [1.111, 0, Math.sqrt(8)], 1e-3)
    assert Math.round(interp.duration) == 1470

def test_zoom_5():
    interp = interpolateZoom.rho(2)([0, 0, 1], [10, 0, 8])
    assert interp(0.5) == [1.111, 0, 12.885], 1e-3)
    assert Math.round(interp.duration) == 3775
