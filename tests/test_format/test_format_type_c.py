import detroit as d3

def test_format_type_c_1():
    assert.strictEqual(format("c")("☃"), "☃")
    assert.strictEqual(format("020c")("☃"),    "0000000000000000000☃")
    assert.strictEqual(format(" ^20c")("☃"), "                 ☃                    ")
    assert.strictEqual(format("$c")("☃"), "$☃")

def test_format_type_c_2():
    assert.strictEqual(formatLocale({decimal: "/"}).format("c")("."), ".")
