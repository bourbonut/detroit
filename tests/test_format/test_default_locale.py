import detroit as d3

enUs = {
    decimal: ".",
    thousands: ",",
    grouping: [3],
    currency: ["$", ""]
}

frFr = {
    decimal: ",",
    thousands: ".",
    grouping: [3],
    currency: ["", "\u00a0€"],
    percent: "\u202f%"
}

def test_defaultLocale_1():
    locale = formatDefaultLocale(frFr)
    try {
        assert.strictEqual(locale.format("$,.2f")(12345678.90), "12.345.678,90 €")
        assert.strictEqual(locale.format(",.0%")(12345678.90), "1.234.567.890\u202f%")
    } finally {
        formatDefaultLocale(enUs)
    }

def test_defaultLocale_2():
    locale = formatDefaultLocale(frFr)
    try {
        assert format == locale.format
        assert.strictEqual(format("$,.2f")(12345678.90), "12.345.678,90 €")
    } finally {
        formatDefaultLocale(enUs)
    }

def test_defaultLocale_3():
    locale = formatDefaultLocale(frFr)
    try {
        assert formatPrefix == locale.formatPrefix
        assert.strictEqual(formatPrefix(",.2", 1e3)(12345678.90), "12.345,68k")
    } finally {
        formatDefaultLocale(enUs)
    }
