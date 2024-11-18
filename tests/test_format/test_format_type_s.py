import detroit as d3

def test_format_type_s_1():
    f = d3.format("s")
    assert f(0) == "0.00000"
    assert f(1) == "1.00000"
    assert f(10) == "10.0000"
    assert f(100) == "100.000"
    assert f(999.5) == "999.500"
    assert f(999500) == "999.500k"
    assert f(1000) == "1.00000k"
    assert f(100) == "100.000"
    assert f(1400) == "1.40000k"
    assert f(1500.5) == "1.50050k"
    assert f(.00001) == "10.0000µ"
    assert f(.000001) == "1.00000µ"

def test_format_type_s_2():
    f1 = d3.format(".3s")
    assert f1(0) == "0.00"
    assert f1(1) == "1.00"
    assert f1(10) == "10.0"
    assert f1(100) == "100"
    assert f1(999.5) == "1.00k"
    assert f1(999500) == "1.00M"
    assert f1(1000) == "1.00k"
    assert f1(1500.5) == "1.50k"
    assert f1(145500000) == "146M"
    assert f1(145999999.99999347) == "146M"
    assert f1(1e26) == "100Y"
    assert f1(.000001) == "1.00µ"
    assert f1(.009995) == "10.0m"
    f2 = d3.format(".4s")
    assert f2(999.5) == "999.5"
    assert f2(999500) == "999.5k"
    assert f2(.009995) == "9.995m"

def test_format_type_s_3():
    f = d3.format(".8s")
    assert f(1.29e-30) == "0.0000013y" # Note: rounded!
    assert f(1.29e-29) == "0.0000129y"
    assert f(1.29e-28) == "0.0001290y"
    assert f(1.29e-27) == "0.0012900y"
    assert f(1.29e-26) == "0.0129000y"
    assert f(1.29e-25) == "0.1290000y"
    assert f(1.29e-24) == "1.2900000y"
    assert f(1.29e-23) == "12.900000y"
    assert f(1.29e-22) == "129.00000y"
    assert f(1.29e-21) == "1.2900000z"
    assert f(-1.29e-30) == "-0.0000013y" # Note: rounded
    assert f(-1.29e-29) == "-0.0000129y"
    assert f(-1.29e-28) == "-0.0001290y"
    assert f(-1.29e-27) == "-0.0012900y"
    assert f(-1.29e-26) == "-0.0129000y"
    assert f(-1.29e-25) == "-0.1290000y"
    assert f(-1.29e-24) == "-1.2900000y"
    assert f(-1.29e-23) == "-12.900000y"
    assert f(-1.29e-22) == "-129.00000y"
    assert f(-1.29e-21) == "-1.2900000z"

def test_format_type_s_4():
    f = d3.format(".8s")
    assert f(1.23e+21) == "1.2300000Z"
    assert f(1.23e+22) == "12.300000Z"
    assert f(1.23e+23) == "123.00000Z"
    assert f(1.23e+24) == "1.2300000Y"
    assert f(1.23e+25) == "12.300000Y"
    assert f(1.23e+26) == "123.00000Y"
    assert f(1.23e+27) == "1230.0000Y"
    assert f(1.23e+28) == "12300.000Y"
    assert f(1.23e+29) == "123000.00Y"
    assert f(1.23e+30) == "1230000.0Y"
    assert f(-1.23e+21) == "-1.2300000Z"
    assert f(-1.23e+22) == "-12.300000Z"
    assert f(-1.23e+23) == "-123.00000Z"
    assert f(-1.23e+24) == "-1.2300000Y"
    assert f(-1.23e+25) == "-12.300000Y"
    assert f(-1.23e+26) == "-123.00000Y"
    assert f(-1.23e+27) == "-1230.0000Y"
    assert f(-1.23e+28) == "-12300.000Y"
    assert f(-1.23e+29) == "-123000.00Y"
    assert f(-1.23e+30) == "-1230000.0Y"

def test_format_type_s_5():
    f1 = d3.format("$.2s")
    assert f1(0) == "$0.0"
    assert f1(2.5e5) == "$250k"
    assert f1(-2.5e8) == "-$250M"
    assert f1(2.5e11) == "$250G"
    f2 = d3.format("$.3s")
    assert f2(0) == "$0.00"
    assert f2(1) == "$1.00"
    assert f2(10) == "$10.0"
    assert f2(100) == "$100"
    assert f2(999.5) == "$1.00k"
    assert f2(999500) == "$1.00M"
    assert f2(1000) == "$1.00k"
    assert f2(1500.5) == "$1.50k"
    assert f2(145500000) == "$146M"
    assert f2(145999999.9999347) == "$146M"
    assert f2(1e26) == "$100Y"
    assert f2(.000001) == "$1.00µ"
    assert f2(.009995) == "$10.0m"
    f3 = d3.format("$.4s")
    assert f3(999.5) == "$999.5"
    assert f3(999500) == "$999.5k"
    assert f3(.009995) == "$9.995m"

def test_format_type_s_6():
    f1 = d3.format(".0s")
    assert f1(1e-5) == "10µ"
    assert f1(1e-4) == "100µ"
    assert f1(1e-3) == "1m"
    assert f1(1e-2) == "10m"
    assert f1(1e-1) == "100m"
    assert f1(1e+0) == "1"
    assert f1(1e+1) == "10"
    assert f1(1e+2) == "100"
    assert f1(1e+3) == "1k"
    assert f1(1e+4) == "10k"
    assert f1(1e+5) == "100k"
    f2 = d3.format(".4s")
    assert f2(1e-5) == "10.00µ"
    assert f2(1e-4) == "100.0µ"
    assert f2(1e-3) == "1.000m"
    assert f2(1e-2) == "10.00m"
    assert f2(1e-1) == "100.0m"
    assert f2(1e+0) == "1.000"
    assert f2(1e+1) == "10.00"
    assert f2(1e+2) == "100.0"
    assert f2(1e+3) == "1.000k"
    assert f2(1e+4) == "10.00k"
    assert f2(1e+5) == "100.0k"

def test_format_type_s_7():
    f = d3.format("020,s")
    assert f(42) ==        "000,000,000,042.0000"
    assert f(42e12) == "00,000,000,042.0000T"

def test_format_type_s_8():
    f = d3.format(",s")
    assert f(42e30) == "42,000,000Y"
