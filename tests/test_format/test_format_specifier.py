import detroit as d3

# def test_formatSpecifier_1():
#     assert.throws(() => { formatSpecifier("foo") }, /invalid format: foo/)
#     assert.throws(() => { formatSpecifier(".-2s") }, /invalid format: \.-2s/)
#     assert.throws(() => { formatSpecifier(".f") }, /invalid format: \.f/)
#
# def test_formatSpecifier_2():
#     s = formatSpecifier("")
#     assert s instanceof formatSpecifier == true
#
# def test_formatSpecifier_3():
#     s = formatSpecifier("")
#     assert s.fill == " "
#     assert.strictEqual(s.align, ">")
#     assert s.sign == "-"
#     assert s.symbol == ""
#     assert s.zero == false
#     assert s.width == None
#     assert s.comma == false
#     assert s.precision == None
#     assert s.trim == false
#     assert s.type == ""
#
# def test_formatSpecifier_4():
#     s = formatSpecifier("q")
#     assert s.trim == false
#     assert s.type == "q"
#
# def test_formatSpecifier_5():
#     s = formatSpecifier("")
#     assert s.trim == false
#     assert s.type == ""
#
# def test_formatSpecifier_6():
#     s = formatSpecifier("")
#     assert.strictEqual((s.fill = "_", s) + "", "_>-")
#     assert.strictEqual((s.align = "^", s) + "", "_^-")
#     assert.strictEqual((s.sign = "+", s) + "", "_^+")
#     assert.strictEqual((s.symbol = "$", s) + "", "_^+$")
#     assert.strictEqual((s.zero = true, s) + "", "_^+$0")
#     assert.strictEqual((s.width = 12, s) + "", "_^+$012")
#     assert.strictEqual((s.comma = true, s) + "", "_^+$012,")
#     assert.strictEqual((s.precision = 2, s) + "", "_^+$012,.2")
#     assert.strictEqual((s.type = "f", s) + "", "_^+$012,.2f")
#     assert.strictEqual((s.trim = true, s) + "", "_^+$012,.2~f")
#     assert.strictEqual(format(s)(42), "+$0,000,000,042")
#
# def test_formatSpecifier_7():
#     s = formatSpecifier("")
#     assert.strictEqual((s.precision = -1, s) + "", " >-.0")
#
# def test_formatSpecifier_8():
#     s = formatSpecifier("")
#     assert.strictEqual((s.width = -1, s) + "", " >-1")
#
# def test_formatSpecifier_9():
#     s = new FormatSpecifier({})
#     assert s.fill == " "
#     assert.strictEqual(s.align, ">")
#     assert s.sign == "-"
#     assert s.symbol == ""
#     assert s.zero == false
#     assert s.width == None
#     assert s.comma == false
#     assert s.precision == None
#     assert s.trim == false
#     assert s.type == ""
#
# def test_formatSpecifier_10():
#     s = new FormatSpecifier({
#         fill: 1,
#         align: 2,
#         sign: 3,
#         symbol: 4,
#         zero: 5,
#         width: 6,
#         comma: 7,
#         precision: 8,
#         trim: 9,
#         type: 10
#     })
#     assert s.fill == "1"
#     assert s.align == "2"
#     assert s.sign == "3"
#     assert s.symbol == "4"
#     assert s.zero == true
#     assert s.width == 6
#     assert s.comma == true
#     assert s.precision == 8
#     assert s.trim == true
#     assert s.type == "10"
