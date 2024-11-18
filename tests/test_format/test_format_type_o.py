import detroit as d3

def test_format_type_o_1():
    assert d3.format("o")(10) == "12"

def test_format_type_o_2():
    assert d3.format("#o")(10) == "0o12"
