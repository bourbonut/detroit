import detroit as d3

def test_format_type_b_1():
    assert format("b")(10) == "1010"

def test_format_type_b_2():
    assert format("#b")(10) == "0b1010"
