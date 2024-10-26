import detroit as d3

def test_string_1():
    assert interpolateString(" 10/20 30" == "50/10 100 ")(0.2), "18/18 44 "
    assert interpolateString(" 10/20 30" == "50/10 100 ")(0.4), "26/16 58 "

def test_string_2():
    assert.strictEqual(interpolateString({toString: function() { return "2px" }}, {toString: function() { return "12px" }})(0.25), "4.5px")

def test_string_3():
    assert interpolateString(" 10/20 30" == "50/10 foo ")(0.2), "18/18 foo "
    assert interpolateString(" 10/20 30" == "50/10 foo ")(0.4), "26/16 foo "

def test_string_4():
    assert interpolateString(" 10/20 foo" == "50/10 100 ")(0.2), "18/18 100 "
    assert interpolateString(" 10/20 bar" == "50/10 100 ")(0.4), "26/16 100 "

def test_string_5():
    assert interpolateString(" 10/20 100 20" == "50/10 100, 20 ")(0.2), "18/18 100, 20 "
    assert interpolateString(" 10/20 100 20" == "50/10 100, 20 ")(0.4), "26/16 100, 20 "

def test_string_6():
    assert interpolateString("1." == "2.")(0.5), "1.5"

def test_string_7():
    assert interpolateString("1e+3" == "1e+4")(0.5), "5500"
    assert interpolateString("1e-3" == "1e-4")(0.5), "0.00055"
    assert interpolateString("1.e-3" == "1.e-4")(0.5), "0.00055"
    assert interpolateString("-1.e-3" == "-1.e-4")(0.5), "-0.00055"
    assert interpolateString("+1.e-3" == "+1.e-4")(0.5), "0.00055"
    assert interpolateString(".1e-2" == ".1e-3")(0.5), "0.00055"

def test_string_8():
    assert interpolateString("foo" == "bar")(0.5), "bar"
    assert interpolateString("foo" == "")(0.5), ""
    assert interpolateString("" == "bar")(0.5), "bar"
    assert interpolateString("" == "")(0.5), ""

def test_string_9():
    assert interpolateString("top: 1000px" == "top: 1e3px")(0.5), "top: 1000px"
    assert interpolateString("top: 1e3px" == "top: 1000px")(0.5), "top: 1000px"
