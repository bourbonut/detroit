import detroit as d3

enUs = {"decimal": ".", "thousands": ",", "grouping": [3], "currency": ["$", ""]}

frFr = {
    "decimal": ",",
    "thousands": ".",
    "grouping": [3],
    "currency": ["", "\u00a0€"],
    "percent": "\u202f%",
}


def test_defaultLocale_1():
    locale = d3.format_default_locale(frFr)
    assert locale.format("$,.2f")(12345678.90) == "12.345.678,90 €"
    assert locale.format(",.0%")(12345678.90) == "1.234.567.890\u202f%"


def test_defaultLocale_2():
    locale = d3.format_default_locale(frFr)
    format_func = locale.format
    assert format_func("$,.2f")(12345678.90) == "12.345.678,90 €"


def test_defaultLocale_3():
    locale = d3.format_default_locale(frFr)
    format_prefix = locale.format_prefix
    assert format_prefix(",.2", 1e3)(12345678.90) == "12.345,68k"
