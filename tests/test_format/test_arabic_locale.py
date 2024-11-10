import detroit as d3

def test_arabicLocale_1():
    assert locale("ar-001").format("$,.2f")(-1234.56) == "−١٬٢٣٤٫٥٦"

def test_arabicLocale_2():
    assert locale("ar-AE").format("$,.2f")(1234.56) == "١٬٢٣٤٫٥٦ د.إ."

def test_arabicLocale_3():
    assert locale("ar-BH").format("$,.2f")(1234.56) == "١٬٢٣٤٫٥٦ د.ب."

def test_arabicLocale_4():
    assert locale("ar-DJ").format("$,.2f")(1234.56) == "\u200fFdj ١٬٢٣٤٫٥٦"

def test_arabicLocale_5():
    assert locale("ar-DZ").format("$,.2f")(1234.56) == "د.ج. 1.234,56"

def test_arabicLocale_6():
    assert locale("ar-EG").format("$,.2f")(1234.56) == "١٬٢٣٤٫٥٦ ج.م."

def test_arabicLocale_7():
    assert locale("ar-EH").format("$,.2f")(1234.56) == "د.م. 1,234.56"

def test_arabicLocale_8():
    assert locale("ar-ER").format("$,.2f")(1234.56) == "Nfk ١٬٢٣٤٫٥٦"

def test_arabicLocale_9():
    assert locale("ar-IL").format("$,.2f")(1234.56) == "₪ ١٬٢٣٤٫٥٦"

def test_arabicLocale_10():
    assert locale("ar-IQ").format("$,.2f")(1234.56) == "١٬٢٣٤٫٥٦ د.ع."

def test_arabicLocale_11():
    assert locale("ar-JO").format("$,.2f")(1234.56) == "١٬٢٣٤٫٥٦ د.أ."

def test_arabicLocale_12():
    assert locale("ar-KM").format("$,.2f")(1234.56) == "١٬٢٣٤٫٥٦ ف.ج.ق."

def test_arabicLocale_13():
    assert locale("ar-KW").format("$,.2f")(1234.56) == "١٬٢٣٤٫٥٦ د.ك."

def test_arabicLocale_14():
    assert locale("ar-LB").format("$,.2f")(1234.56) == "١٬٢٣٤٫٥٦ ل.ل."

def test_arabicLocale_15():
    assert locale("ar-MA").format("$,.2f")(1234.56) == "د.م. 1.234,56"

def test_arabicLocale_16():
    assert locale("ar-MR").format("$,.2f")(1234.56) == "١٬٢٣٤٫٥٦ أ.م."

def test_arabicLocale_17():
    assert locale("ar-OM").format("$,.2f")(1234.56) == "١٬٢٣٤٫٥٦ ر.ع."

def test_arabicLocale_18():
    assert locale("ar-PS").format("$,.2f")(1234.56) == "₪ ١٬٢٣٤٫٥٦"

def test_arabicLocale_19():
    assert locale("ar-QA").format("$,.2f")(1234.56) == "١٬٢٣٤٫٥٦ ر.ق."

def test_arabicLocale_20():
    assert locale("ar-SA").format("$,.2f")(1234.56) == "١٬٢٣٤٫٥٦ ر.س."

def test_arabicLocale_21():
    assert locale("ar-SD").format("$,.2f")(1234.56) == "١٬٢٣٤٫٥٦ ج.س."

def test_arabicLocale_22():
    assert locale("ar-SO").format("$,.2f")(1234.56) == "‏S ١٬٢٣٤٫٥٦"

def test_arabicLocale_23():
    assert locale("ar-SS").format("$,.2f")(1234.56) == "£ ١٬٢٣٤٫٥٦"

def test_arabicLocale_24():
    assert locale("ar-SY").format("$,.2f")(1234.56) == "١٬٢٣٤٫٥٦ ل.س."

def test_arabicLocale_25():
    assert locale("ar-TD").format("$,.2f")(1234.56) == "\u200fFCFA ١٬٢٣٤٫٥٦"

def test_arabicLocale_26():
    assert locale("ar-TN").format("$,.2f")(1234.56) == "د.ت. 1.234,56"

def test_arabicLocale_27():
    assert locale("ar-YE").format("$,.2f")(1234.56) == "١٬٢٣٤٫٥٦ ر.ى."
