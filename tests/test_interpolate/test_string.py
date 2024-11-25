import detroit as d3


def test_string_1():
    assert d3.interpolate_string(" 10/20 30", "50/10 100 ")(0.2) == "18/18 44 "
    assert d3.interpolate_string(" 10/20 30", "50/10 100 ")(0.4) == "26/16 58 "


def test_string_2():
    assert d3.interpolate_string(" 10/20 30", "50/10 foo ")(0.2) == "18/18 foo "
    assert d3.interpolate_string(" 10/20 30", "50/10 foo ")(0.4) == "26/16 foo "


def test_string_3():
    assert d3.interpolate_string(" 10/20 foo", "50/10 100 ")(0.2) == "18/18 100 "
    assert d3.interpolate_string(" 10/20 bar", "50/10 100 ")(0.4) == "26/16 100 "


def test_string_4():
    assert (
        d3.interpolate_string(" 10/20 100 20", "50/10 100, 20 ")(0.2)
        == "18/18 100, 20 "
    )
    assert (
        d3.interpolate_string(" 10/20 100 20", "50/10 100, 20 ")(0.4)
        == "26/16 100, 20 "
    )


def test_string_5():
    assert d3.interpolate_string("1.", "2.")(0.5) == "1.5"


def test_string_6():
    assert d3.interpolate_string("1e+3", "1e+4")(0.5) == "5500.0"
    assert d3.interpolate_string("1e-3", "1e-4")(0.5) == "0.00055"
    assert d3.interpolate_string("1.e-3", "1.e-4")(0.5) == "0.00055"
    assert d3.interpolate_string("-1.e-3", "-1.e-4")(0.5) == "-0.00055"
    assert d3.interpolate_string("+1.e-3", "+1.e-4")(0.5) == "0.00055"
    assert d3.interpolate_string(".1e-2", ".1e-3")(0.5) == "0.00055"


def test_string_7():
    assert d3.interpolate_string("foo", "bar")(0.5) == "bar"
    assert d3.interpolate_string("foo", "")(0.5) == ""
    assert d3.interpolate_string("", "bar")(0.5) == "bar"
    assert d3.interpolate_string("", "")(0.5) == ""


def test_string_8():
    assert d3.interpolate_string("top: 1000px", "top: 1e3px")(0.5) == "top: 1000px"
    assert d3.interpolate_string("top: 1e3px", "top: 1000px")(0.5) == "top: 1000px"
