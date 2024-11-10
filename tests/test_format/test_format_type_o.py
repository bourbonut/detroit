import detroit as d3

def test_format_type_o_1():
    assert format("o")(10) == "12"

def test_format_type_o_2():
    assert format("#o")(10) == "0o12"
