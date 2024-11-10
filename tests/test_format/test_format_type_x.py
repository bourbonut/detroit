import detroit as d3

def test_format_type_x_1():
    assert format("x")(0xdeadbeef) == "deadbeef"

def test_format_type_x_2():
    assert format("#x")(0xdeadbeef) == "0xdeadbeef"

def test_format_type_x_3():
    assert.strictEqual(format(",x")(0xdeadbeef), "de,adb,eef")

def test_format_type_x_4():
    assert.strictEqual(format(",x")(0xdeadbeef), "de,adb,eef")

def test_format_type_x_5():
    assert.strictEqual(format("#,x")(0xadeadbeef), "0xade,adb,eef")

def test_format_type_x_6():
    assert format("+#x")(0xdeadbeef) ==    "+0xdeadbeef"
    assert.strictEqual(format("+#x")(-0xdeadbeef), "−0xdeadbeef")
    assert format(" #x")(0xdeadbeef) ==    " 0xdeadbeef"
    assert.strictEqual(format(" #x")(-0xdeadbeef), "−0xdeadbeef")

def test_format_type_x_7():
    assert.strictEqual(format("$,x")(0xdeadbeef), "$de,adb,eef")

def test_format_type_x_8():
    assert format(".2x")(0xdeadbeef) == "deadbeef"
    assert.strictEqual(format(".2x")(-4.2), "−4")

def test_format_type_x_9():
    assert format("x")(2.4) == "2"

def test_format_type_x_10():
    assert format("x")(-0) == "0"
    assert format("x")(-1e-12) == "0"

def test_format_type_x_11():
    assert.strictEqual(format("x")(-0xeee), "−eee")

def test_format_type_x_12():
    assert format("X")(0xdeadbeef) == "DEADBEEF"

def test_format_type_x_13():
    assert format("#X")(0xdeadbeef) == "0xDEADBEEF"

def test_format_type_x_14():
    assert format("X")(-0) == "0"
    assert format("X")(-1e-12) == "0"

def test_format_type_x_15():
    assert.strictEqual(format("X")(-0xeee), "−EEE")

def test_format_type_x_16():
    assert format("20x")(0xdeadbeef) ==     "                        deadbeef"
    assert format("#20x")(0xdeadbeef) ==    "                    0xdeadbeef"
    assert format("020x")(0xdeadbeef) ==    "000000000000deadbeef"
    assert format("#020x")(0xdeadbeef) == "0x0000000000deadbeef"
