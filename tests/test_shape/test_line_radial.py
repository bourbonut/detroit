import detroit as d3
from detroit.shape.curves import curve_radial_linear


def test_line_radial_1():
    l = d3.line_radial()
    assert l.get_angle()([42, 34]) == 42
    assert l.get_radius()([42, 34]) == 34
    assert l.get_defined()([42, 34]) is True
    assert l.get_curve() == curve_radial_linear
    assert l.get_context() is None
    assert l([[0, 1], [2, 3], [4, 5]]) == "M0,-1L2.728,1.248L-3.784,3.268"
