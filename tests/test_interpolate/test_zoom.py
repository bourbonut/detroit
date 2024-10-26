import detroit as d3
import math

def test_zoom_1():
    assert d3.interpolate_zoom(
        [324.68721096803614, 59.43501602433761, 1.8827137399562621], [324.6872108946794, 59.43501601062763, 7.399052110984391]
    )(0.5) == [324.68721093135775, 59.43501601748262, 3.7323313186268305]

def test_zoom_2():
    assert math.isclose(d3.interpolate_zoom([0, 0, 1], [0, 0, 1.1]).duration, 67, rel_tol=1)
    assert math.isclose(d3.interpolate_zoom([0, 0, 1], [0, 0, 2]).duration, 490, rel_tol=1)
    assert math.isclose(d3.interpolate_zoom([0, 0, 1], [10, 0, 8]).duration, 2872.5, rel_tol=1)

def test_zoom_3():
    output_1 = d3.interpolate_zoom([0, 0, 1], [10, 10, 5])(0.5)
    output_2 = d3.interpolate_zoom.set_rho(math.sqrt(2))([0, 0, 1], [10, 10, 5])(0.5)
    for op1, op2 in zip(output_1, output_2):
        assert math.isclose(op1, op2)

def test_zoom_4():
    interp = d3.interpolate_zoom.set_rho(0)([0, 0, 1], [10, 0, 8])
    output = interp(0.5)
    for computed, expected in zip(output, [1.111, 0, math.sqrt(8)]):
        assert math.isclose(computed, expected, rel_tol=1e-3)
    assert round(interp.duration) == 1470

def test_zoom_5():
    interp = d3.interpolate_zoom.set_rho(2)([0, 0, 1], [10, 0, 8])
    output = interp(0.5)
    for computed, expected in zip(output, [1.111, 0, 12.885]):
        assert math.isclose(computed, expected, rel_tol=1e-3)
    assert round(interp.duration) == 3775
