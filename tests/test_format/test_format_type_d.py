import detroit as d3

def test_format_type_d_1():
    f = format("08d")
    assert f(0) == "00000000"
    assert f(42) == "00000042"
    assert f(42000000) == "42000000"
    assert f(420000000) == "420000000"
    assert.strictEqual(f(-4), "−0000004")
    assert.strictEqual(f(-42), "−0000042")
    assert.strictEqual(f(-4200000), "−4200000")
    assert.strictEqual(f(-42000000), "−42000000")

def test_format_type_d_2():
    f = format("8d")
    assert f(0) == "             0"
    assert f(42) == "            42"
    assert f(42000000) == "42000000"
    assert f(420000000) == "420000000"
    assert.strictEqual(f(-4), "            −4")
    assert.strictEqual(f(-42), "         −42")
    assert.strictEqual(f(-4200000), "−4200000")
    assert.strictEqual(f(-42000000), "−42000000")

def test_format_type_d_3():
    f = format("_>8d")
    assert.strictEqual(f(0), "_______0")
    assert.strictEqual(f(42), "______42")
    assert f(42000000) == "42000000"
    assert f(420000000) == "420000000"
    assert.strictEqual(f(-4), "______−4")
    assert.strictEqual(f(-42), "_____−42")
    assert.strictEqual(f(-4200000), "−4200000")
    assert.strictEqual(f(-42000000), "−42000000")

def test_format_type_d_4():
    f = format("+08,d")
    assert f(0) == "+0,000,000"
    assert f(42) == "+0,000,042"
    assert f(42000000) == "+42,000,000"
    assert f(420000000) == "+420,000,000"
    assert.strictEqual(f(-4), "−0,000,004")
    assert.strictEqual(f(-42), "−0,000,042")
    assert.strictEqual(f(-4200000), "−4,200,000")
    assert.strictEqual(f(-42000000), "−42,000,000")

def test_format_type_d_5():
    f = format(".2d")
    assert f(0) == "0"
    assert f(42) == "42"
    assert.strictEqual(f(-4.2), "−4")

def test_format_type_d_6():
    f = format("d")
    assert f(4.2) == "4"

def test_format_type_d_7():
    f = format(",d")
    assert f(0) == "0"
    assert f(42) == "42"
    assert f(42000000) == "42,000,000"
    assert f(420000000) == "420,000,000"
    assert.strictEqual(f(-4), "−4")
    assert.strictEqual(f(-42), "−42")
    assert.strictEqual(f(-4200000), "−4,200,000")
    assert.strictEqual(f(-42000000), "−42,000,000")
    assert f(1e21) == "1,000,000,000,000,000,000,000"
    assert f(1.3e27) == "1,300,000,000,000,000,000,000,000,000"
    assert f(1.3e107) == "130,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000"

def test_format_type_d_8():
    assert.strictEqual(format("01,d")(0), "0")
    assert.strictEqual(format("01,d")(0), "0")
    assert.strictEqual(format("02,d")(0), "00")
    assert.strictEqual(format("03,d")(0), "000")
    assert.strictEqual(format("04,d")(0), "0,000")
    assert.strictEqual(format("05,d")(0), "0,000")
    assert.strictEqual(format("06,d")(0), "00,000")
    assert.strictEqual(format("08,d")(0), "0,000,000")
    assert.strictEqual(format("013,d")(0), "0,000,000,000")
    assert.strictEqual(format("021,d")(0), "0,000,000,000,000,000")
    assert.strictEqual(format("013,d")(-42000000), "−0,042,000,000")
    assert.strictEqual(format("012,d")(1e21), "1,000,000,000,000,000,000,000")
    assert.strictEqual(format("013,d")(1e21), "1,000,000,000,000,000,000,000")
    assert.strictEqual(format("014,d")(1e21), "1,000,000,000,000,000,000,000")
    assert.strictEqual(format("015,d")(1e21), "1,000,000,000,000,000,000,000")

def test_format_type_d_9():
    assert.strictEqual(format("01,d")(1), "1")
    assert.strictEqual(format("01,d")(1), "1")
    assert.strictEqual(format("02,d")(12), "12")
    assert.strictEqual(format("03,d")(123), "123")
    assert.strictEqual(format("05,d")(12345), "12,345")
    assert.strictEqual(format("08,d")(12345678), "12,345,678")
    assert.strictEqual(format("013,d")(1234567890123), "1,234,567,890,123")

def test_format_type_d_10():
    assert.strictEqual(format("1,d")(0), "0")
    assert.strictEqual(format("1,d")(0), "0")
    assert.strictEqual(format("2,d")(0), " 0")
    assert.strictEqual(format("3,d")(0), "    0")
    assert.strictEqual(format("5,d")(0), "        0")
    assert.strictEqual(format("8,d")(0), "             0")
    assert.strictEqual(format("13,d")(0), "                        0")
    assert.strictEqual(format("21,d")(0), "                                        0")

def test_format_type_d_11():
    assert.strictEqual(format("1,d")(1), "1")
    assert.strictEqual(format("1,d")(1), "1")
    assert.strictEqual(format("2,d")(12), "12")
    assert.strictEqual(format("3,d")(123), "123")
    assert.strictEqual(format("5,d")(12345), "12,345")
    assert.strictEqual(format("8,d")(12345678), "12,345,678")
    assert.strictEqual(format("13,d")(1234567890123), "1,234,567,890,123")

def test_format_type_d_12():
    assert.strictEqual(format("<1,d")(0), "0")
    assert.strictEqual(format("<1,d")(0), "0")
    assert.strictEqual(format("<2,d")(0), "0 ")
    assert.strictEqual(format("<3,d")(0), "0    ")
    assert.strictEqual(format("<5,d")(0), "0        ")
    assert.strictEqual(format("<8,d")(0), "0             ")
    assert.strictEqual(format("<13,d")(0), "0                        ")
    assert.strictEqual(format("<21,d")(0), "0                                        ")

def test_format_type_d_13():
    assert.strictEqual(format(">1,d")(0), "0")
    assert.strictEqual(format(">1,d")(0), "0")
    assert.strictEqual(format(">2,d")(0), " 0")
    assert.strictEqual(format(">3,d")(0), "    0")
    assert.strictEqual(format(">5,d")(0), "        0")
    assert.strictEqual(format(">8,d")(0), "             0")
    assert.strictEqual(format(">13,d")(0), "                        0")
    assert.strictEqual(format(">21,d")(0), "                                        0")
    assert.strictEqual(format(">21,d")(1000), "                                1,000")
    assert.strictEqual(format(">21,d")(1e21), "1,000,000,000,000,000,000,000")

def test_format_type_d_14():
    assert.strictEqual(format("^1,d")(0), "0")
    assert.strictEqual(format("^1,d")(0), "0")
    assert.strictEqual(format("^2,d")(0), "0 ")
    assert.strictEqual(format("^3,d")(0), " 0 ")
    assert.strictEqual(format("^5,d")(0), "    0    ")
    assert.strictEqual(format("^8,d")(0), "     0        ")
    assert.strictEqual(format("^13,d")(0), "            0            ")
    assert.strictEqual(format("^21,d")(0), "                    0                    ")
    assert.strictEqual(format("^21,d")(1000), "                1,000                ")
    assert.strictEqual(format("^21,d")(1e21), "1,000,000,000,000,000,000,000")

def test_format_type_d_15():
    assert.strictEqual(format("=+1,d")(0), "+0")
    assert.strictEqual(format("=+1,d")(0), "+0")
    assert.strictEqual(format("=+2,d")(0), "+0")
    assert.strictEqual(format("=+3,d")(0), "+ 0")
    assert.strictEqual(format("=+5,d")(0), "+     0")
    assert.strictEqual(format("=+8,d")(0), "+            0")
    assert.strictEqual(format("=+13,d")(0), "+                     0")
    assert.strictEqual(format("=+21,d")(0), "+                                     0")
    assert.strictEqual(format("=+21,d")(1e21), "+1,000,000,000,000,000,000,000")

def test_format_type_d_16():
    assert.strictEqual(format("=+$1,d")(0), "+$0")
    assert.strictEqual(format("=+$1,d")(0), "+$0")
    assert.strictEqual(format("=+$2,d")(0), "+$0")
    assert.strictEqual(format("=+$3,d")(0), "+$0")
    assert.strictEqual(format("=+$5,d")(0), "+$    0")
    assert.strictEqual(format("=+$8,d")(0), "+$         0")
    assert.strictEqual(format("=+$13,d")(0), "+$                    0")
    assert.strictEqual(format("=+$21,d")(0), "+$                                    0")
    assert.strictEqual(format("=+$21,d")(1e21), "+$1,000,000,000,000,000,000,000")

def test_format_type_d_17():
    assert.strictEqual(format(" 1,d")(-1), "−1")
    assert.strictEqual(format(" 1,d")(0), " 0")
    assert.strictEqual(format(" 2,d")(0), " 0")
    assert.strictEqual(format(" 3,d")(0), "    0")
    assert.strictEqual(format(" 5,d")(0), "        0")
    assert.strictEqual(format(" 8,d")(0), "             0")
    assert.strictEqual(format(" 13,d")(0), "                        0")
    assert.strictEqual(format(" 21,d")(0), "                                        0")
    assert.strictEqual(format(" 21,d")(1e21), " 1,000,000,000,000,000,000,000")

def test_format_type_d_18():
    assert.strictEqual(format("-1,d")(-1), "−1")
    assert.strictEqual(format("-1,d")(0), "0")
    assert.strictEqual(format("-2,d")(0), " 0")
    assert.strictEqual(format("-3,d")(0), "    0")
    assert.strictEqual(format("-5,d")(0), "        0")
    assert.strictEqual(format("-8,d")(0), "             0")
    assert.strictEqual(format("-13,d")(0), "                        0")
    assert.strictEqual(format("-21,d")(0), "                                        0")

def test_format_type_d_19():
    assert format("1d")(-0) == "0"
    assert format("1d")(-1e-12) == "0"
