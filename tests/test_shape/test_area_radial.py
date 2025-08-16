import detroit as d3
from detroit.shape.curves import curve_radial, curve_radial_linear


def test_area_radial_1():
    a = d3.area_radial()
    assert a.get_start_angle()([42, 34]) == 42
    assert a.get_end_angle() is None
    assert a.get_inner_radius()([42, 34]) == 0
    assert a.get_outer_radius()([42, 34]) == 34
    assert a.get_defined()([42, 34]) is True
    assert a.get_curve() == curve_radial_linear
    assert a.get_context() is None
    assert a([[0, 1], [2, 3], [4, 5]]) == "M0,-1L2.728,1.248L-3.784,3.268L0,0L0,0L0,0Z"


def test_area_radial_2():
    def defined():
        return True

    curve = d3.curve_cardinal
    context = {}

    def start_angle():
        return

    def end_angle():
        return

    def radius():
        return

    a = (
        d3.area_radial()
        .set_defined(defined)
        .set_curve(curve)
        .set_context(context)
        .radius(radius)
        .start_angle(start_angle)
        .end_angle(end_angle)
    )
    l = a.line_start_angle()
    assert l.get_defined() == defined
    assert type(l.get_curve()(None)) == type(curve_radial(curve)(None))
    assert l.get_context() == context
    assert l.get_angle() == start_angle
    assert l.get_radius() == radius


def test_area_radial_3():
    def defined():
        return True

    curve = d3.curve_cardinal
    context = {}

    def start_angle():
        return

    def end_angle():
        return

    def radius():
        return

    a = (
        d3.area_radial()
        .set_defined(defined)
        .set_curve(curve)
        .set_context(context)
        .radius(radius)
        .start_angle(start_angle)
        .end_angle(end_angle)
    )
    l = a.line_end_angle()
    assert l.get_defined() == defined
    assert type(l.get_curve()(None)) == type(curve_radial(curve)(None))
    assert l.get_context() == context
    assert l.get_angle() == end_angle
    assert l.get_radius() == radius


def test_area_radial_4():
    def defined():
        return True

    curve = d3.curve_cardinal
    context = {}

    def angle():
        return

    def inner_radius():
        return

    def outer_radius():
        return

    a = (
        d3.area_radial()
        .set_defined(defined)
        .set_curve(curve)
        .set_context(context)
        .angle(angle)
        .inner_radius(inner_radius)
        .outer_radius(outer_radius)
    )
    l = a.line_inner_radius()
    assert l.get_defined() == defined
    assert type(l.get_curve()(None)) == type(curve_radial(curve)(None))
    assert l.get_context() == context
    assert l.get_angle() == angle
    assert l.get_radius() == inner_radius


def test_area_radial_5():
    def defined():
        return True

    curve = d3.curve_cardinal
    context = {}

    def angle():
        return

    def inner_radius():
        return

    def outer_radius():
        return

    a = (
        d3.area_radial()
        .set_defined(defined)
        .set_curve(curve)
        .set_context(context)
        .angle(angle)
        .inner_radius(inner_radius)
        .outer_radius(outer_radius)
    )
    l = a.line_outer_radius()
    assert l.get_defined() == defined
    assert type(l.get_curve()(None)) == type(curve_radial(curve)(None))
    assert l.get_context() == context
    assert l.get_angle() == angle
    assert l.get_radius() == outer_radius
