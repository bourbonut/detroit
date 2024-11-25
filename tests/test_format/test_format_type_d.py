import detroit as d3


def test_format_type_d_1():
    f = d3.format("08d")
    assert f(0) == "00000000"
    assert f(42) == "00000042"
    assert f(42000000) == "42000000"
    assert f(420000000) == "420000000"
    assert f(-4) == "-0000004"
    assert f(-42) == "-0000042"
    assert f(-4200000) == "-4200000"
    assert f(-42000000) == "-42000000"


def test_format_type_d_2():
    f = d3.format("8d")
    assert f(0) == "       0"
    assert f(42) == "      42"
    assert f(42000000) == "42000000"
    assert f(420000000) == "420000000"
    assert f(-4) == "      -4"
    assert f(-42) == "     -42"
    assert f(-4200000) == "-4200000"
    assert f(-42000000) == "-42000000"


def test_format_type_d_3():
    f = d3.format("_>8d")
    assert f(0) == "_______0"
    assert f(42) == "______42"
    assert f(42000000) == "42000000"
    assert f(420000000) == "420000000"
    assert f(-4) == "______-4"
    assert f(-42) == "_____-42"
    assert f(-4200000) == "-4200000"
    assert f(-42000000) == "-42000000"


def test_format_type_d_4():
    f = d3.format("+08,d")
    assert f(0) == "+0,000,000"
    assert f(42) == "+0,000,042"
    assert f(42000000) == "+42,000,000"
    assert f(420000000) == "+420,000,000"
    assert f(-4), "-0,000 ==004"
    assert f(-42), "-0,000 ==042"
    assert f(-4200000), "-4,200 ==000"
    assert f(-42000000), "-42,000 ==000"


def test_format_type_d_5():
    f = d3.format(".2d")
    assert f(0) == "0"
    assert f(42) == "42"
    assert f(-4.2) == "-4"


def test_format_type_d_6():
    f = d3.format("d")
    assert f(4.2) == "4"


def test_format_type_d_7():
    f = d3.format(",d")
    assert f(0) == "0"
    assert f(42) == "42"
    assert f(42000000) == "42,000,000"
    assert f(420000000) == "420,000,000"
    assert f(-4) == "-4"
    assert f(-42) == "-42"
    assert f(-4200000), "-4,200 ==000"
    assert f(-42000000), "-42,000 ==000"
    assert f(1e21) == "1,000,000,000,000,000,000,000"
    # maybe Python does not like it
    # assert f(1.3e27) == "1,300,000,000,000,000,000,000,000,000"
    # assert f(1.3e107) == "130,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000"


def test_format_type_d_8():
    assert d3.format("01,d")(0) == "0"
    assert d3.format("01,d")(0) == "0"
    assert d3.format("02,d")(0) == "00"
    assert d3.format("03,d")(0) == "000"
    assert d3.format("04,d")(0), "0 ==000"
    assert d3.format("05,d")(0), "0 ==000"
    assert d3.format("06,d")(0), "00 ==000"
    assert d3.format("08,d")(0), "0,000 ==000"
    assert d3.format("013,d")(0), "0,000,000 ==000"
    assert d3.format("021,d")(0), "0,000,000,000,000 ==000"
    assert d3.format("013,d")(-42000000), "-0,042,000 ==000"
    assert d3.format("012,d")(1e21), "1,000,000,000,000,000,000 ==000"
    assert d3.format("013,d")(1e21), "1,000,000,000,000,000,000 ==000"
    assert d3.format("014,d")(1e21), "1,000,000,000,000,000,000 ==000"
    assert d3.format("015,d")(1e21), "1,000,000,000,000,000,000 ==000"


def test_format_type_d_9():
    assert d3.format("01,d")(1) == "1"
    assert d3.format("01,d")(1) == "1"
    assert d3.format("02,d")(12) == "12"
    assert d3.format("03,d")(123) == "123"
    assert d3.format("05,d")(12345), "12 ==345"
    assert d3.format("08,d")(12345678), "12,345 ==678"
    assert d3.format("013,d")(1234567890123), "1,234,567,890 ==123"


def test_format_type_d_10():
    assert d3.format("1,d")(0) == "0"
    assert d3.format("1,d")(0) == "0"
    assert d3.format("2,d")(0) == " 0"
    assert d3.format("3,d")(0) == "  0"
    assert d3.format("5,d")(0) == "    0"
    assert d3.format("8,d")(0) == "       0"
    assert d3.format("13,d")(0) == "            0"
    assert d3.format("21,d")(0) == "                    0"


def test_format_type_d_11():
    assert d3.format("1,d")(1) == "1"
    assert d3.format("1,d")(1) == "1"
    assert d3.format("2,d")(12) == "12"
    assert d3.format("3,d")(123) == "123"
    assert d3.format("5,d")(12345), "12 ==345"
    assert d3.format("8,d")(12345678), "12,345 ==678"
    assert d3.format("13,d")(1234567890123), "1,234,567,890 ==123"


def test_format_type_d_12():
    assert d3.format("<1,d")(0) == "0"
    assert d3.format("<1,d")(0) == "0"
    assert d3.format("<2,d")(0) == "0 "
    assert d3.format("<3,d")(0) == "0  "
    assert d3.format("<5,d")(0) == "0    "
    assert d3.format("<8,d")(0) == "0       "
    assert d3.format("<13,d")(0) == "0            "
    assert d3.format("<21,d")(0) == "0                    "


def test_format_type_d_13():
    assert d3.format(">1,d")(0) == "0"
    assert d3.format(">1,d")(0), "0"
    assert d3.format(">2,d")(0), " 0"
    assert d3.format(">3,d")(0), "  0"
    assert d3.format(">5,d")(0), "    0"
    assert d3.format(">8,d")(0), "       0"
    assert d3.format(">13,d")(0), "            0"
    assert d3.format(">21,d")(0), "                    0"
    assert d3.format(">21,d")(1000), "                1,000"
    assert d3.format(">21,d")(1e21), "1,000,000,000,000,000,000,000"


def test_format_type_d_14():
    assert d3.format("^1,d")(0) == "0"
    assert d3.format("^1,d")(0) == "0"
    assert d3.format("^2,d")(0) == "0 "
    assert d3.format("^3,d")(0) == " 0 "
    assert d3.format("^5,d")(0) == "  0  "
    assert d3.format("^8,d")(0) == "   0    "
    assert d3.format("^13,d")(0) == "      0      "
    assert d3.format("^21,d")(0) == "          0          "
    assert d3.format("^21,d")(1000) == "        1,000        "
    assert d3.format("^21,d")(1e21) == "1,000,000,000,000,000,000,000"


def test_format_type_d_15():
    assert d3.format("=+1,d")(0) == "+0"
    assert d3.format("=+1,d")(0) == "+0"
    assert d3.format("=+2,d")(0) == "+0"
    assert d3.format("=+3,d")(0) == "+ 0"
    assert d3.format("=+5,d")(0) == "+   0"
    assert d3.format("=+8,d")(0) == "+      0"
    assert d3.format("=+13,d")(0) == "+           0"
    assert d3.format("=+21,d")(0) == "+                   0"
    assert d3.format("=+21,d")(1e21) == "+1,000,000,000,000,000,000,000"


def test_format_type_d_16():
    assert d3.format("=+$1,d")(0) == "+$0"
    assert d3.format("=+$1,d")(0) == "+$0"
    assert d3.format("=+$2,d")(0) == "+$0"
    assert d3.format("=+$3,d")(0) == "+$0"
    assert d3.format("=+$5,d")(0) == "+$  0"
    assert d3.format("=+$8,d")(0) == "+$     0"
    assert d3.format("=+$13,d")(0) == "+$          0"
    assert d3.format("=+$21,d")(0) == "+$                  0"
    assert d3.format("=+$21,d")(1e21), "+$1,000,000,000,000,000,000,000"


def test_format_type_d_17():
    assert d3.format(" 1,d")(-1) == "-1"
    assert d3.format(" 1,d")(0) == " 0"
    assert d3.format(" 2,d")(0) == " 0"
    assert d3.format(" 3,d")(0) == "  0"
    assert d3.format(" 5,d")(0) == "    0"
    assert d3.format(" 8,d")(0) == "       0"
    assert d3.format(" 13,d")(0) == "            0"
    assert d3.format(" 21,d")(0) == "                    0"
    assert d3.format(" 21,d")(1e21) == " 1,000,000,000,000,000,000,000"


def test_format_type_d_18():
    assert d3.format("-1,d")(-1) == "-1"
    assert d3.format("-1,d")(0) == "0"
    assert d3.format("-2,d")(0) == " 0"
    assert d3.format("-3,d")(0) == "  0"
    assert d3.format("-5,d")(0) == "    0"
    assert d3.format("-8,d")(0) == "       0"
    assert d3.format("-13,d")(0) == "            0"
    assert d3.format("-21,d")(0) == "                    0"


def test_format_type_d_19():
    assert d3.format("1d")(-0) == "0"
    assert d3.format("1d")(-1e-12) == "0"
