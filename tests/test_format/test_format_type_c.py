import detroit as d3

def test_format_type_c_1():
    assert d3.format("c")("☃") == "☃"
    assert d3.format("020c")("☃") ==    "0000000000000000000☃"
    assert d3.format(" ^20c")("☃") == "         ☃          "
    assert d3.format("$c")("☃") == "$☃"

def test_format_type_c_2():
    assert d3.format_default_locale({"decimal": "/"}).format("c")(".") == "."
