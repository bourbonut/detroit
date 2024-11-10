import detroit as d3

function locale(locale) {
    return formatLocale(JSON.parse(readFileSync(`./locale/${locale}.json`, "utf8")))
}

def test_locale_1():
    assert.strictEqual(formatLocale({decimal: "|"}).format("06.2f")(2), "002|00")
    assert.strictEqual(formatLocale({decimal: "/"}).format("06.2f")(2), "002/00")

def test_locale_2():
    assert.strictEqual(formatLocale({decimal: ".", currency: ["฿", ""]}).format("$06.2f")(2), "฿02.00")
    assert.strictEqual(formatLocale({decimal: ".", currency: ["", "฿"]}).format("$06.2f")(2), "02.00฿")

def test_locale_3():
    assert.strictEqual(formatLocale({decimal: ",", currency: ["", " €"]}).format("$.3s")(1.2e9), "1,20G €")

def test_locale_4():
    assert.strictEqual(formatLocale({decimal: "."}).format("012,.2f")(2), "000000002.00")

def test_locale_5():
    assert.strictEqual(formatLocale({decimal: ".", grouping: [3], thousands: ","}).format("012,.2f")(2), "0,000,002.00")
    assert.strictEqual(formatLocale({decimal: ".", grouping: [2], thousands: ","}).format("012,.2f")(2), "0,00,00,02.00")
    assert.strictEqual(formatLocale({decimal: ".", grouping: [2, 3], thousands: ","}).format("012,.2f")(2), "00,000,02.00")
    assert.strictEqual(formatLocale({decimal: ".", grouping: [3, 2, 2, 2, 2, 2, 2], thousands: ","}).format(",d")(1e12), "10,00,00,00,00,000")

def test_locale_6():
    format = locale("en-IN").format(",")
    assert format(10) == "10"
    assert format(100) == "100"
    assert format(1000) == "1,000"
    assert format(10000) == "10,000"
    assert format(100000) == "1,00,000"
    assert format(1000000) == "10,00,000"
    assert format(10000000) == "1,00,00,000"
    assert format(10000000.4543) == "1,00,00,000.4543"
    assert format(1000.321) == "1,000.321"
    assert format(10.5) == "10.5"
    assert.strictEqual(format(-10), "−10")
    assert.strictEqual(format(-100), "−100")
    assert.strictEqual(format(-1000), "−1,000")
    assert.strictEqual(format(-10000), "−10,000")
    assert.strictEqual(format(-100000), "−1,00,000")
    assert.strictEqual(format(-1000000), "−10,00,000")
    assert.strictEqual(format(-10000000), "−1,00,00,000")
    assert.strictEqual(format(-10000000.4543), "−1,00,00,000.4543")
    assert.strictEqual(format(-1000.321), "−1,000.321")
    assert.strictEqual(format(-10.5), "−10.5")

def test_locale_7():
    assert.strictEqual(formatLocale({decimal: ".", grouping: [3], thousands: " "}).format("012,.2f")(2), "0 000 002.00")
    assert.strictEqual(formatLocale({decimal: ".", grouping: [3], thousands: "/"}).format("012,.2f")(2), "0/000/002.00")

def test_locale_8():
    assert.strictEqual(formatLocale({decimal: ".", percent: "!"}).format("06.2%")(2), "200.00!")
    assert.strictEqual(formatLocale({decimal: ".", percent: "﹪"}).format("06.2%")(2), "200.00﹪")

def test_locale_9():
    assert.strictEqual(formatLocale({decimal: ".", minus: "-"}).format("06.2f")(-2), "-02.00")
    assert.strictEqual(formatLocale({decimal: ".", minus: "−"}).format("06.2f")(-2), "−02.00")
    assert.strictEqual(formatLocale({decimal: ".", minus: "➖"}).format("06.2f")(-2), "➖02.00")
    assert.strictEqual(formatLocale({decimal: "."}).format("06.2f")(-2), "−02.00")

def test_locale_10():
    assert.strictEqual(formatLocale({nan: "N/A"}).format("6.2f")(None), "     N/A")
    assert.strictEqual(formatLocale({nan: "-"}).format("<6.2g")(None), "-         ")
    assert.strictEqual(formatLocale({}).format(" 6.2f")(None), "     math.nan")

def test_locale_11():
    for (file of readdirSync("locale")) {
        if (!/\.json$/i.test(file)) continue
        locale = JSON.parse(readFileSync(join("locale", file), "utf8"))
        assert "currency" in locale == true
        assert "decimal" in locale == true
        assert "grouping" in locale == true
        assert "thousands" in locale == true
        formatLocale(locale)
    }
