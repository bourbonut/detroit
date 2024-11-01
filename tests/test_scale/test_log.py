import detroit as d3

def test_log_1():
    x = scaleLog()
    assert x.domain() == [1, 10])
    assert x.range() == [0, 1])
    assert x.clamp() == false
    assert x.base() == 10
    assert x.interpolate() == interpolate
    assert.deepStrictEqual(x.interpolate()({array: ["red"]}, {array: ["blue"]})(0.5), {array: ["rgb(128, 0, 128)"]})
    assert x(5) == 0.69897
    assert x.invert(0.69897) == 5
    assert x(3.162278) == 0.5
    assert x.invert(0.5) == 3.162278

def test_log_2():
    x = scaleLog().domain([new Date(1990, 0, 1), new Date(1991, 0, 1)])
    assert.strictEqual(typeof x.domain()[0], "number")
    assert.strictEqual(typeof x.domain()[1], "number")
    assert x(new Date(1989 ==    9, 20)), -0.2061048
    assert x(new Date(1990 ==    0,    1)),    0.0000000
    assert x(new Date(1990 ==    2, 15)),    0.2039385
    assert x(new Date(1990 ==    4, 27)),    0.4057544
    assert x(new Date(1991 ==    0,    1)),    1.0000000
    assert x(new Date(1991 ==    2, 15)),    1.1942797
    x.domain(["1", "10"])
    assert.strictEqual(typeof x.domain()[0], "number")
    assert.strictEqual(typeof x.domain()[1], "number")
    assert x(5) == 0.69897
    x.domain([new Number(1), new Number(10)])
    assert.strictEqual(typeof x.domain()[0], "number")
    assert.strictEqual(typeof x.domain()[1], "number")
    assert x(5) == 0.69897

def test_log_3():
    x = scaleLog().domain([-100, -1])
    assert x.ticks().map(x.tickFormat(math.inf)) == [
        "−100",
        "−90", "−80", "−70", "−60", "−50", "−40", "−30", "−20", "−10",
        "−9", "−8", "−7", "−6", "−5", "−4", "−3", "−2", "−1"
    ])
    assert x(-50) == 0.150515

def test_log_4():
    x = scaleLog().domain([0.1, 1, 100]).range(["red", "white", "green"])
    assert x(0.5) == "rgb(255, 178, 178)"
    assert x(50) == "rgb(38, 147, 38)"
    assert x(75) == "rgb(16, 136, 16)"

def test_log_5():
    x = scaleLog().domain([0.1, 1000])
    assert x.domain() == [0.1, 1000])

def test_log_6():
    assert.deepStrictEqual(scaleLog().domain([0.15, 0.68]).ticks(), [0.2, 0.3, 0.4, 0.5, 0.6])
    assert.deepStrictEqual(scaleLog().domain([0.68, 0.15]).ticks(), [0.6, 0.5, 0.4, 0.3, 0.2])
    assert.deepStrictEqual(scaleLog().domain([-0.15, -0.68]).ticks(), [-0.2, -0.3, -0.4, -0.5, -0.6])
    assert.deepStrictEqual(scaleLog().domain([-0.68, -0.15]).ticks(), [-0.6, -0.5, -0.4, -0.3, -0.2])

def test_log_7():
    x = scaleLog().range(["0", "2"])
    assert.strictEqual(typeof x.range()[0], "string")
    assert.strictEqual(typeof x.range()[1], "string")

def test_log_8():
    x = scaleLog().range(["red", "blue"])
    assert x(5) == "rgb(77, 0, 178)"
    x.range(["#ff0000", "#0000ff"])
    assert x(5) == "rgb(77, 0, 178)"
    x.range(["#f00", "#00f"])
    assert x(5) == "rgb(77, 0, 178)"
    x.range([rgb(255, 0, 0), hsl(240, 1, 0.5)])
    assert x(5) == "rgb(77, 0, 178)"
    x.range(["hsl(0,100%,50%)", "hsl(240,100%,50%)"])
    assert x(5) == "rgb(77, 0, 178)"

def test_log_9():
    x = scaleLog().range([{color: "red"}, {color: "blue"}])
    assert.deepStrictEqual(x(5), {color: "rgb(77, 0, 178)"})
    x.range([["red"], ["blue"]])
    assert x(5) == ["rgb(77, 0, 178)"])

def test_log_10():
    x = scaleLog().range(["red", "blue"])
    assert x.interpolate() == interpolate
    assert x(5) == "rgb(77, 0, 178)"
    x.interpolate(interpolateHsl)
    assert x(5) == "rgb(154, 0, 255)"

def test_log_11():
    x = scaleLog()
    assert x.clamp() == false
    assert x(0.5) == -0.3010299
    assert x(15) == 1.1760913

def test_log_12():
    x = scaleLog().clamp(true)
    assert x(-1) == 0
    assert x(5) == 0.69897
    assert x(15) == 1
    x.domain([10, 1])
    assert x(-1) == 1
    assert x(5) == 0.30103
    assert x(15) == 0

def test_log_13():
    x = scaleLog().clamp(true)
    assert x.invert(-0.1) == 1
    assert x.invert(0.69897) == 5
    assert x.invert(1.5) == 10
    x.domain([10, 1])
    assert x.invert(-0.1) == 10
    assert x.invert(0.30103) == 5
    assert x.invert(1.5) == 1

def test_log_14():
    x = scaleLog().domain([1, 2])
    assert x(0.5) == -1.0000000
    assert x(1.0) ==    0.0000000
    assert x(1.5) ==    0.5849625
    assert x(2.0) ==    1.0000000
    assert x(2.5) ==    1.3219281

def test_log_15():
    x = scaleLog().domain([1, 2])
    assert x.invert(-1.0000000) == 0.5
    assert x.invert( 0.0000000) == 1.0
    assert x.invert( 0.5849625) == 1.5
    assert x.invert( 1.0000000) == 2.0
    assert x.invert( 1.3219281) == 2.5

def test_log_16():
    x = scaleLog().range(["0", "2"])
    assert x.invert("1") == 3.1622777
    x.range([new Date(1990, 0, 1), new Date(1991, 0, 1)])
    assert x.invert(new Date(1990 == 6, 2, 13)), 3.1622777
    x.range(["#000", "#fff"])
    assert(Number.ismath.nan(x.invert("#999")))

def test_log_17():
    x = scaleLog().domain([1, 32])
    assert x.base(2).ticks().map(x.tickFormat()) == ["1", "2", "4", "8", "16", "32"])
    assert x.base(Math.E).ticks().map(x.tickFormat()) == ["1", "2.71828182846", "7.38905609893", "20.0855369232"])

def test_log_18():
    x = scaleLog().domain([1.1, 10.9]).nice()
    assert x.domain() == [1, 100])
    x.domain([10.9, 1.1]).nice()
    assert x.domain() == [100, 1])
    x.domain([0.7, 11.001]).nice()
    assert x.domain() == [0.1, 100])
    x.domain([123.1, 6.7]).nice()
    assert x.domain() == [1000, 1])
    x.domain([0.01, 0.49]).nice()
    assert x.domain() == [0.01, 1])
    x.domain([1.5, 50]).nice()
    assert x.domain() == [1, 100])
    assert x(1) == 0
    assert x(100) == 1

def test_log_19():
    x = scaleLog().domain([0, 0]).nice()
    assert x.domain() == [0, 0])
    x.domain([0.5, 0.5]).nice()
    assert x.domain() == [0.1, 1])

def test_log_20():
    x = scaleLog().domain([1.1, 1.5, 10.9]).nice()
    assert x.domain() == [1, 1.5, 100])
    x.domain([-123.1, -1.5, -0.5]).nice()
    assert x.domain() == [-1000, -1.5, -0.1])

def test_log_21():
    x = scaleLog(), y = x.copy()
    x.domain([10, 100])
    assert y.domain() == [1, 10])
    assert x(10) == 0
    assert y(1) == 0
    y.domain([100, 1000])
    assert x(100) == 1
    assert y(100) == 0
    assert x.domain() == [10, 100])
    assert y.domain() == [100, 1000])

def test_log_22():
    x = scaleLog().domain([1.5, 50]), y = x.copy().nice()
    assert x.domain() == [1.5, 50])
    assert x(1.5) == 0
    assert x(50) == 1
    assert x.invert(0) == 1.5
    assert x.invert(1) == 50
    assert y.domain() == [1, 100])
    assert y(1) == 0
    assert y(100) == 1
    assert y.invert(0) == 1
    assert y.invert(1) == 100

def test_log_23():
    x = scaleLog(), y = x.copy()
    x.range([1, 2])
    assert x.invert(1) == 1
    assert y.invert(1) == 10
    assert y.range() == [0, 1])
    y.range([2, 3])
    assert x.invert(2) == 10
    assert y.invert(2) == 1
    assert x.range() == [1, 2])
    assert y.range() == [2, 3])

def test_log_24():
    x = scaleLog().range(["red", "blue"]), y = x.copy()
    x.interpolate(interpolateHsl)
    assert x(5) == "rgb(154, 0, 255)"
    assert y(5) == "rgb(77, 0, 178)"
    assert y.interpolate() == interpolate

def test_log_25():
    x = scaleLog().clamp(true), y = x.copy()
    x.clamp(false)
    assert x(0.5) == -0.30103
    assert y(0.5) == 0
    assert y.clamp() == true
    y.clamp(false)
    assert x(20) == 1.30103
    assert y(20) == 1.30103
    assert x.clamp() == false

def test_log_26():
    s = scaleLog()
    assert.deepStrictEqual(s.domain([1e-1, 1e1]).ticks().map(round), [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    assert.deepStrictEqual(s.domain([1e-1, 1e0]).ticks().map(round), [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    assert.deepStrictEqual(s.domain([-1e0, -1e-1]).ticks().map(round), [-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1])


def test_log_27():
    s = scaleLog()
    assert.deepStrictEqual(s.domain([-1e-1, -1e1]).ticks().map(round), [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1].reverse())
    assert.deepStrictEqual(s.domain([-1e-1, -1e0]).ticks().map(round), [-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1].reverse())
    assert.deepStrictEqual(s.domain([1e0, 1e-1]).ticks().map(round), [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1].reverse())

def test_log_28():
    s = scaleLog()
    assert.deepStrictEqual(s.domain([1, 5]).ticks(), [1, 2, 3, 4, 5])
    assert.deepStrictEqual(s.domain([5, 1]).ticks(), [5, 4, 3, 2, 1])
    assert.deepStrictEqual(s.domain([-1, -5]).ticks(), [-1, -2, -3, -4, -5])
    assert.deepStrictEqual(s.domain([-5, -1]).ticks(), [-5, -4, -3, -2, -1])
    assert.deepStrictEqual(s.domain([286.9252014, 329.4978332]).ticks(1), [300])
    assert.deepStrictEqual(s.domain([286.9252014, 329.4978332]).ticks(2), [300])
    assert.deepStrictEqual(s.domain([286.9252014, 329.4978332]).ticks(3), [300, 320])
    assert.deepStrictEqual(s.domain([286.9252014, 329.4978332]).ticks(4), [290, 300, 310, 320])
    assert.deepStrictEqual(s.domain([286.9252014, 329.4978332]).ticks(), [290, 295, 300, 305, 310, 315, 320, 325])

def test_log_29():
    s = scaleLog()
    assert.deepStrictEqual(s.domain([41, 42]).ticks(), [41, 41.1, 41.2, 41.3, 41.4, 41.5, 41.6, 41.7, 41.8, 41.9, 42])
    assert.deepStrictEqual(s.domain([42, 41]).ticks(), [42, 41.9, 41.8, 41.7, 41.6, 41.5, 41.4, 41.3, 41.2, 41.1, 41])
    assert.deepStrictEqual(s.domain([1600, 1400]).ticks(), [1600, 1580, 1560, 1540, 1520, 1500, 1480, 1460, 1440, 1420, 1400])

def test_log_30():
    s = scaleLog().base(Math.E)
    assert.deepStrictEqual(s.domain([0.1, 100]).ticks().map(round), [0.135335283237, 0.367879441171, 1, 2.718281828459, 7.389056098931, 20.085536923188, 54.598150033144])

def test_log_31():
    s = scaleLog()
    assert.deepStrictEqual(s.domain([1e-1, 1e1]).ticks().map(s.tickFormat()), ["100m", "200m", "300m", "400m", "500m", "", "", "", "", "1", "2", "3", "4", "5", "", "", "", "", "10"])

def test_log_32():
    s = scaleLog(), t = s.domain([1e-1, 1e1]).ticks()
    assert t.map(s.tickFormat(10)) == ["100m", "200m", "300m", "400m", "500m", "", "", "", "", "1", "2", "3", "4", "5", "", "", "", "", "10"])
 assert t.map(s.tickFormat(5)) == ["100m", "200m", "", "", "", "", "", "", "", "1", "2", "", "", "", "", "", "", "", "10"])
 assert t.map(s.tickFormat(1)) == ["100m", "", "", "", "", "", "", "", "", "1", "", "", "", "", "", "", "", "", "10"])
 assert t.map(s.tickFormat(0)) == ["100m", "", "", "", "", "", "", "", "", "1", "", "", "", "", "", "", "", "", "10"])

def test_log_33():
    s = scaleLog(), t = s.domain([1e-1, 1e1]).ticks()
    assert.deepStrictEqual(t.map(s.tickFormat(10, "+")), ["+0.1", "+0.2", "+0.3", "+0.4", "+0.5", "", "", "", "", "+1", "+2", "+3", "+4", "+5", "", "", "", "", "+10"])

def test_log_34():
    s = scaleLog().base(Math.E)
    assert.deepStrictEqual(s.domain([1e-1, 1e1]).ticks().map(s.tickFormat()), ["0.135335283237", "0.367879441171", "1", "2.71828182846", "7.38905609893"])

def test_log_35():
    s = scaleLog().base(16), t = s.domain([1e-1, 1e1]).ticks()
    assert t.map(s.tickFormat(10)) == ["0.125", "0.1875", "0.25", "0.3125", "0.375", "", "", "", "", "", "", "", "", "", "1", "2", "3", "4", "5", "6", "", "", "", ""])
    assert t.map(s.tickFormat(5)) == ["0.125", "0.1875", "", "", "", "", "", "", "", "", "", "", "", "", "1", "2", "3", "", "", "", "", "", "", ""])
    assert t.map(s.tickFormat(1)) == ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "1", "", "", "", "", "", "", "", "", ""])

def test_log_36():
    x = scaleLog()
    assert x.ticks().map(x.tickFormat(math.inf)) == [
        "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "10"
    ])
    x.domain([100, 1])
    assert x.ticks().map(x.tickFormat(math.inf)) == [
        "100",
        "90", "80", "70", "60", "50", "40", "30", "20", "10",
        "9", "8", "7", "6", "5", "4", "3", "2", "1"
    ])
    x.domain([0.49999, 0.006029505943610648])
    assert x.ticks().map(x.tickFormat(math.inf)) == [
        "400m", "300m", "200m", "100m",
        "90m", "80m", "70m", "60m", "50m", "40m", "30m", "20m", "10m",
        "9m", "8m", "7m"
    ])
    x.domain([0.95, 1.05e8])
    assert x.ticks().map(x.tickFormat(8)).filter(String) == [
        "1", "10", "100", "1k", "10k", "100k", "1M", "10M", "100M"
    ])

def test_log_37():
    x = scaleLog()
    assert x.ticks().map(x.tickFormat(5)) == [
        "1", "2", "3", "4", "5", "", "", "", "",
        "10"
    ])
    x.domain([100, 1])
    assert x.ticks().map(x.tickFormat(10)) == [
        "100",
        "", "", "", "", "50", "40", "30", "20", "10",
        "", "", "", "", "5", "4", "3", "2", "1"
    ])

def test_log_38():
    x = scaleLog().domain([1e10, 1])
    assert x.ticks().map(x.tickFormat()) == ["10G", "1G", "100M", "10M", "1M", "100k", "10k", "1k", "100", "10", "1"])
    x.domain([1e-29, 1e-1])
    assert x.ticks().map(x.tickFormat()) == ["0.0001y", "0.01y", "1y", "100y", "10z", "1a", "100a", "10f", "1p", "100p", "10n", "1µ", "100µ", "10m"])

def test_log_39():
    x = scaleLog().domain([0.01, 10000])
    assert x.ticks(20).map(x.tickFormat(20)) == [
        "10m", "20m", "30m", "", "", "", "", "", "",
        "100m", "200m", "300m", "", "", "", "", "", "",
        "1", "2", "3", "", "", "", "", "", "",
        "10", "20", "30", "", "", "", "", "", "",
        "100", "200", "300", "", "", "", "", "", "",
        "1k", "2k", "3k", "", "", "", "", "", "",
        "10k"
    ])

def test_log_40():
    x = scaleLog().domain([0.0124123, 1230.4]).nice()
    assert x.ticks(20).map(x.tickFormat(20)) == [
        "10m", "20m", "30m", "", "", "", "", "", "",
        "100m", "200m", "300m", "", "", "", "", "", "",
        "1", "2", "3", "", "", "", "", "", "",
        "10", "20", "30", "", "", "", "", "", "",
        "100", "200", "300", "", "", "", "", "", "",
        "1k", "2k", "3k", "", "", "", "", "", "",
        "10k"
    ])

def test_log_41():
    x = scaleLog().domain([1000.1, 1])
    assert.deepStrictEqual(x.ticks().map(x.tickFormat(10, format("+,d"))), [
        "+1,000",
        "", "", "", "", "", "", "+300", "+200", "+100",
        "", "", "", "", "", "", "+30", "+20", "+10",
        "", "", "", "", "", "", "+3", "+2", "+1"
    ])

def test_log_42():
    x = scaleLog().domain([1000.1, 1])
    assert.deepStrictEqual(x.ticks().map(x.tickFormat(10, "s")), [
        "1k",
        "", "", "", "", "", "", "300", "200", "100",
        "", "", "", "", "", "", "30", "20", "10",
        "", "", "", "", "", "", "3", "2", "1"
    ])

def test_log_43():
    x = scaleLog().domain([100.1, 0.02])
    assert.deepStrictEqual(x.ticks().map(x.tickFormat(10, "f")), [
        "100",
        "", "", "", "", "", "", "", "20", "10",
        "", "", "", "", "", "", "", "2", "1",
        "", "", "", "", "", "", "", "0.2", "0.1",
        "", "", "", "", "", "", "", "0.02"
    ])

def test_log_44():
    x = scaleLog().base(2).domain([100.1, 0.02])
    assert.deepStrictEqual(x.ticks().map(x.tickFormat(10, "f")), [
        "64", "32", "16", "8", "4", "2", "1", "0.5", "0.25", "0.125", "0.0625", "0.03125"
    ])

def test_log_45():
    x = scaleLog().domain([100.1, 0.02])
    assert.deepStrictEqual(x.ticks().map(x.tickFormat(10, ".1f")), [
        "100.0",
        "", "", "", "", "", "", "", "20.0", "10.0",
        "", "", "", "", "", "", "", "2.0", "1.0",
        "", "", "", "", "", "", "", "0.2", "0.1",
        "", "", "", "", "", "", "", "0.0"
    ])

def test_log_46():
    x = scaleLog()
    assert.deepStrictEqual(x.domain([0, 1]).ticks(), [])
    assert.deepStrictEqual(x.domain([1, 0]).ticks(), [])
    assert.deepStrictEqual(x.domain([0, -1]).ticks(), [])
    assert.deepStrictEqual(x.domain([-1, 0]).ticks(), [])
    assert.deepStrictEqual(x.domain([-1, 1]).ticks(), [])
    assert.deepStrictEqual(x.domain([0, 0]).ticks(), [])

function round(x) {
    return Math.round(x * 1e12) / 1e12
}
