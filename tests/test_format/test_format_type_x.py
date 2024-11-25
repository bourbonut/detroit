import detroit as d3


def test_format_type_x_1():
    assert d3.format("x")(0xDEADBEEF) == "deadbeef"


def test_format_type_x_2():
    assert d3.format("#x")(0xDEADBEEF) == "0xdeadbeef"


def test_format_type_x_3():
    assert d3.format(",x")(0xDEADBEEF) == "de,adb,eef"


def test_format_type_x_4():
    assert d3.format(",x")(0xDEADBEEF) == "de,adb,eef"


def test_format_type_x_5():
    assert d3.format("#,x")(0xADEADBEEF) == "0xade,adb,eef"


def test_format_type_x_6():
    assert d3.format("+#x")(0xDEADBEEF) == "+0xdeadbeef"
    assert d3.format("+#x")(-0xDEADBEEF) == "-0xdeadbeef"
    assert d3.format(" #x")(0xDEADBEEF) == " 0xdeadbeef"
    assert d3.format(" #x")(-0xDEADBEEF) == "-0xdeadbeef"


def test_format_type_x_7():
    assert d3.format("$,x")(0xDEADBEEF) == "$de,adb,eef"


def test_format_type_x_8():
    assert d3.format(".2x")(0xDEADBEEF) == "deadbeef"
    assert d3.format(".2x")(-4.2) == "-4"


def test_format_type_x_9():
    assert d3.format("x")(2.4) == "2"


def test_format_type_x_10():
    assert d3.format("x")(-0) == "0"
    assert d3.format("x")(-1e-12) == "0"


def test_format_type_x_11():
    assert d3.format("x")(-0xEEE) == "-eee"


def test_format_type_x_12():
    assert d3.format("X")(0xDEADBEEF) == "DEADBEEF"


def test_format_type_x_13():
    assert d3.format("#X")(0xDEADBEEF) == "0xDEADBEEF"


def test_format_type_x_14():
    assert d3.format("X")(-0) == "0"
    assert d3.format("X")(-1e-12) == "0"


def test_format_type_x_15():
    assert d3.format("X")(-0xEEE) == "-EEE"


def test_format_type_x_16():
    assert d3.format("20x")(0xDEADBEEF) == "            deadbeef"
    assert d3.format("#20x")(0xDEADBEEF) == "          0xdeadbeef"
    assert d3.format("020x")(0xDEADBEEF) == "000000000000deadbeef"
    assert d3.format("#020x")(0xDEADBEEF) == "0x0000000000deadbeef"
