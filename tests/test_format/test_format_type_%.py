import detroit as d3

def test_format_type_p_1():
    f = d3.format(".0%")
    assert f(0) == "0%"
    assert f(0.042) == "4%"
    assert f(0.42) == "42%"
    assert f(4.2) == "420%"
    assert f(-.042) == "-4%"
    assert f(-.42) == "-42%"
    assert f(-4.2) == "-420%"

def test_format_type_p_2():
    f1 = d3.format(".1%")
    assert f1(0.234) == "23.4%"
    f2 = d3.format(".2%")
    assert f2(0.234) == "23.40%"

def test_format_type_p_3():
    assert d3.format("020.0%")(42) == "0000000000000004200%"
    assert d3.format("20.0%")(42) == "               4200%"

def test_format_type_p_4():
    assert d3.format("^21.0%")(0.42) == "         42%         "
    assert d3.format("^21,.0%")(422) == "       42,200%       " 
    assert d3.format("^21,.0%")(-422) == "      -42,200%       "
