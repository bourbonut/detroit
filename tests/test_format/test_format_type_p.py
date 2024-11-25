import detroit as d3


def test_format_type_p_1():
    f = d3.format("p")
    assert f(0.00123) == "0.123000%"
    assert f(0.0123) == "1.23000%"
    assert f(0.123) == "12.3000%"
    assert f(0.234) == "23.4000%"
    assert f(1.23) == "123.000%"
    assert f(-0.00123) == "-0.123000%"
    assert f(-0.0123) == "-1.23000%"
    assert f(-0.123) == "-12.3000%"
    assert f(-1.23) == "-123.000%"


def test_format_type_p_2():
    f = d3.format("+.2p")
    assert f(0.00123) == "+0.12%"
    assert f(0.0123) == "+1.2%"
    assert f(0.123) == "+12%"
    assert f(1.23) == "+120%"
    assert f(-0.00123) == "-0.12%"
    assert f(-0.0123) == "-1.2%"
    assert f(-0.123) == "-12%"
    assert f(-1.23) == "-120%"
