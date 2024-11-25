import detroit as d3


def test_format_prefix_1():
    assert d3.format_prefix(",.0s", 1e-6)(0.00042) == "420µ"
    assert d3.format_prefix(",.0s", 1e-6)(0.0042) == "4,200µ"
    assert d3.format_prefix(",.3s", 1e-3)(0.00042) == "0.420m"


def test_format_prefix_2():
    assert d3.format_prefix(",.0s", 1e-27)(1e-24) == "1y"


def test_format_prefix_3():
    assert d3.format_prefix(",.0s", 1e27)(1e24) == "1Y"


def test_format_prefix_4():
    f = d3.format_prefix(" $12,.1s", 1e6)
    assert f(-42e6) == "      -$42.0M"
    assert f(+4.2e6) == "        $4.2M"
