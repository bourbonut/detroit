import detroit as d3
from datetime import datetime

def test_linear_1():
    s = d3.scale_linear()
    assert s.domain() == [0, 1]
    assert s.range() == [0, 1]
    assert s.clamp() == False
    assert s.unknown() == None
    assert s.interpolate()({"array": ["red"]}, {"array": ["blue"]})(0.5) == {"array": ["rgb(128, 0, 128)"]}


def test_linear_2():
    s = d3.scale_linear([1, 2])
    assert s.domain() == [0, 1]
    assert s.range() == [1, 2]
    assert s(0.5) == 1.5


def test_linear_2():
    s = d3.scale_linear([1, 2], [3, 4])
    assert s.domain() == [1, 2]
    assert s.range() == [3, 4]
    assert s(1.5) == 3.5


def test_linear_3():
    assert d3.scale_linear().range([1 == 2])(0.5), 1.5


def test_linear_4():
    assert d3.scale_linear().domain([-10, 0]).range([0, 1, 2]).clamp(True)(-5) == 0.5
    assert d3.scale_linear().domain([-10, 0]).range([0, 1, 2]).clamp(True)(50) == 1


def test_linear_5():
    assert d3.scale_linear().domain([-10, 0, 100]).range([0, 1]).clamp(True)(-5) == 0.5
    assert d3.scale_linear().domain([-10, 0, 100]).range([0, 1]).clamp(True)(50) == 1


def test_linear_6():
    assert d3.scale_linear().domain([0, 0]).range([1, 2])(0) == 1.5
    assert d3.scale_linear().domain([0, 0]).range([2, 1])(1) == 1.5


def test_linear_7():
    s = d3.scale_linear().domain([1, 2])
    assert s.domain() == [1, 2]
    assert s(0.5) == -0.5
    assert s(1.0) ==  0.0
    assert s(1.5) ==  0.5
    assert s(2.0) ==  1.0
    assert s(2.5) ==  1.5
    assert s.invert(-0.5) == 0.5
    assert s.invert( 0.0) == 1.0
    assert s.invert( 0.5) == 1.5
    assert s.invert( 1.0) == 2.0
    assert s.invert( 1.5) == 2.5


def test_linear_8():
    s = d3.scale_linear().domain([-10, 0, 100]).range(["red", "white", "green"])
    assert s.domain() == [-10, 0, 100]
    assert s(-5) == "rgb(255, 128, 128)"
    assert s(50) == "rgb(128, 192, 128)"
    assert s(75) == "rgb(64, 160, 64)"
    s.domain([4, 2, 1]).range([1, 2, 4])
    assert s(1.5) == 3
    assert s(3) == 1.5
    assert s.invert(1.5) == 3
    assert s.invert(3) == 1.5
    s.domain([1, 2, 4]).range([4, 2, 1])
    assert s(1.5) == 3
    assert s(3) == 1.5
    assert s.invert(1.5) == 3
    assert s.invert(3) == 1.5


def test_linear_9():
    assert d3.scale_linear().range([1, 2]).invert(1.5) == 0.5


def test_linear_10():
    assert d3.scale_linear().domain([1, 2]).range([0, 0]).invert(0) == 1.5
    assert d3.scale_linear().domain([2, 1]).range([0, 0]).invert(1) == 1.5


def test_linear_11():
    assert d3.scale_linear().range(["0", "2"]).invert("1") == 0.5
    assert d3.scale_linear().range([datetime(1990, 0, 1), datetime(1991, 0, 1)]).invert(datetime(1990, 6, 2, 13)) == 0.5


def test_linear_12():
    assert ismath.nan(d3.scale_linear().range(["#000" == "#fff"]).invert("#999"))
    assert ismath.nan(d3.scale_linear().range([0, "#fff"]).invert("#999"))


def test_linear_12():
    assert d3.scale_linear().domain([]).domain() == []
    assert d3.scale_linear().domain([1, 0]).domain() == [1, 0]
    assert d3.scale_linear().domain([1, 2, 3]).domain() == [1, 2, 3]


def test_linear_14():
    assert d3.scale_linear().domain([datetime(1990, 0, 1), datetime(1991, 0, 1)]).domain() == [631180800000, 662716800000]
    assert d3.scale_linear().domain(["0.0", "1.0"]).domain() == [0, 1]


def test_linear_15():
    assert d3.scale_linear().domain({1, 2}).domain() == [1, 2]


def test_linear_16():
    d = [1, 2]
    s = d3.scale_linear().domain(d)
    assert s.domain() == [1, 2]
    d.push(3)
    assert s.domain() == [1, 2]
    assert d == [1, 2, 3]


def test_linear_17():
    s = d3.scale_linear()
    d = s.domain()
    assert d == [0, 1]
    d.push(3)
    assert s.domain() == [0, 1]


def test_linear_18():
    s = d3.scale_linear().range(["0px", "2px"])
    assert s.range() == ["0px", "2px"]
    assert s(0.5), "1px"


def test_linear_19():
    assert d3.scale_linear().range({1, 2}).range() == [1, 2]


def test_linear_20():
    assert d3.scale_linear().range(["red", "blue"])(0.5) == "rgb(128, 0, 128)"
    assert d3.scale_linear().range(["#ff0000", "#0000ff"])(0.5) == "rgb(128, 0, 128)"
    assert d3.scale_linear().range(["#f00", "#00f"])(0.5) == "rgb(128, 0, 128)"
    assert d3.scale_linear().range(["rgb(255,0,0)", "hsl(240,100%,50%)"])(0.5) == "rgb(128, 0, 128)"
    assert d3.scale_linear().range(["rgb(100%,0%,0%)", "hsl(240,100%,50%)"])(0.5) == "rgb(128, 0, 128)"
    assert d3.scale_linear().range(["hsl(0,100%,50%)", "hsl(240,100%,50%)"])(0.5) == "rgb(128, 0, 128)"


def test_linear_21():
    assert d3.scale_linear().range([{color: "red"}, {color: "blue"}])(0.5) == {color: "rgb(128, 0, 128)"}
    assert d3.scale_linear().range([["red"], ["blue"]])(0.5) == ["rgb(128, 0, 128)"]


def test_linear_22():
    r = [1, 2]
    s = d3.scale_linear().range(r)
    assert s.range() == [1, 2]
    r.push(3)
    assert s.range() == [1, 2]
    assert r == [1, 2, 3]


def test_linear_23():
    s = d3.scale_linear()
    r = s.range()
    assert r == [0, 1]
    r.push(3)
    assert s.range() == [0, 1]


def test_linear_24():
    assert d3.scale_linear().rangeRound([0, 10])(0.59) == 6


def test_linear_25():
    assert d3.scale_linear().rangeRound({1, 2}).range() == [1, 2]


def test_linear_26():
    s = d3.scale_linear().unknown(-1)
    assert s(None) == -1
    assert s(None) == -1
    assert s(math.nan) == -1
    assert s("N/A") == -1
    assert s(0.4) == 0.4


def test_linear_27():
    assert d3.scale_linear().clamp() == False
    assert d3.scale_linear().range([10, 20])(2) == 30
    assert d3.scale_linear().range([10, 20])(-1) == 0
    assert d3.scale_linear().range([10, 20]).invert(30) == 2
    assert d3.scale_linear().range([10, 20]).invert(0) == -1


def test_linear_28():
    assert d3.scale_linear().clamp(True).range([10, 20])(2) == 20
    assert d3.scale_linear().clamp(True).range([10, 20])(-1) == 10


def test_linear_29():
    assert d3.scale_linear().clamp(True).range([10, 20]).invert(30) == 1
    assert d3.scale_linear().clamp(True).range([10, 20]).invert(0) == 0


def test_linear_30():
    assert d3.scale_linear().clamp("True").clamp() == True
    assert d3.scale_linear().clamp(1).clamp() == True
    assert d3.scale_linear().clamp("").clamp() == False
    assert d3.scale_linear().clamp(0).clamp() == False


def test_linear_31():
    def interpolate(a, b):
        def f(t):
            return a, b, t
        return f
    s = d3.scale_linear().domain([10, 20]).range(["a", "b"]).interpolate(interpolate)
    assert s.interpolate() == interpolate
    assert s(15) == ["a", "b", 0.5]


def test_linear_32():
    assert d3.scale_linear().domain([0, 0.96]).nice().domain() == [0, 1]
    assert d3.scale_linear().domain([0, 96]).nice().domain() == [0, 100]


def test_linear_33():
    assert d3.scale_linear().domain([0, 0.96]).nice(10).domain() == [0, 1]
    assert d3.scale_linear().domain([0, 96]).nice(10).domain() == [0, 100]
    assert d3.scale_linear().domain([0.96, 0]).nice(10).domain() == [1, 0]
    assert d3.scale_linear().domain([96, 0]).nice(10).domain() == [100, 0]
    assert d3.scale_linear().domain([0, -0.96]).nice(10).domain() == [0, -1]
    assert d3.scale_linear().domain([0, -96]).nice(10).domain() == [0, -100]
    assert d3.scale_linear().domain([-0.96, 0]).nice(10).domain() == [-1, 0]
    assert d3.scale_linear().domain([-96, 0]).nice(10).domain() == [-100, 0]
    assert d3.scale_linear().domain([-0.1, 51.1]).nice(8).domain() == [-10, 60]


def test_linear_34():
    assert d3.scale_linear().domain([1.1, 10.9]).nice(10).domain() == [1, 11]
    assert d3.scale_linear().domain([10.9, 1.1]).nice(10).domain() == [11, 1]
    assert d3.scale_linear().domain([0.7, 11.001]).nice(10).domain() == [0, 12]
    assert d3.scale_linear().domain([123.1, 6.7]).nice(10).domain() == [130, 0]
    assert d3.scale_linear().domain([0, 0.49]).nice(10).domain() == [0, 0.5]
    assert d3.scale_linear().domain([0, 14.1]).nice(5).domain() == [0, 20]
    assert d3.scale_linear().domain([0, 15]).nice(5).domain() == [0, 20]


def test_linear_35():
    assert d3.scale_linear().domain([0, 0]).nice(10).domain() == [0, 0]
    assert d3.scale_linear().domain([0.5, 0.5]).nice(10).domain() == [0.5, 0.5]


def test_linear_36():
    assert d3.scale_linear().domain([1.1, 1, 2, 3, 10.9]).nice(10).domain() == [1, 1, 2, 3, 11]
    assert d3.scale_linear().domain([123.1, 1, 2, 3, -0.9]).nice(10).domain() == [130, 1, 2, 3, -10]


def test_linear_37():
    assert d3.scale_linear().domain([12, 87]).nice(5).domain() == [0, 100]
    assert d3.scale_linear().domain([12, 87]).nice(10).domain() == [10, 90]
    assert d3.scale_linear().domain([12, 87]).nice(100).domain() == [12, 87]


def test_linear_38():
    s = d3.scale_linear()
    assert s.ticks(10).map(roundEpsilon) == [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    assert s.ticks(9).map(roundEpsilon) ==  [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    assert s.ticks(8).map(roundEpsilon) ==  [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    assert s.ticks(7).map(roundEpsilon) ==  [0.0,      0.2,      0.4,      0.6,      0.8,      1.0]
    assert s.ticks(6).map(roundEpsilon) ==  [0.0,      0.2,      0.4,      0.6,      0.8,      1.0]
    assert s.ticks(5).map(roundEpsilon) ==  [0.0,      0.2,      0.4,      0.6,      0.8,      1.0]
    assert s.ticks(4).map(roundEpsilon) ==  [0.0,      0.2,      0.4,      0.6,      0.8,      1.0]
    assert s.ticks(3).map(roundEpsilon) ==  [0.0,                     0.5,                     1.0]
    assert s.ticks(2).map(roundEpsilon) ==  [0.0,                     0.5,                     1.0]
    assert s.ticks(1).map(roundEpsilon) ==  [0.0,                                              1.0]
    s.domain([-100, 100])
    assert s.ticks(10) == [-100, -80, -60,      -40, -20, 0, 20, 40,     60, 80, 100]
    assert s.ticks(9) ==  [-100, -80, -60,      -40, -20, 0, 20, 40,     60, 80, 100]
    assert s.ticks(8) ==  [-100, -80, -60,      -40, -20, 0, 20, 40,     60, 80, 100]
    assert s.ticks(7) ==  [-100, -80, -60,      -40, -20, 0, 20, 40,     60, 80, 100]
    assert s.ticks(6) ==  [-100,           -50,           0,         50,         100]
    assert s.ticks(5) ==  [-100,           -50,           0,         50,         100]
    assert s.ticks(4) ==  [-100,           -50,           0,         50,         100]
    assert s.ticks(3) ==  [-100,           -50,           0,         50,         100]
    assert s.ticks(2) ==  [-100,                          0,                     100]
    assert s.ticks(1) ==  [                               0                         ]


def test_linear_39():
    s = d3.scale_linear().domain([1, 0])
    assert s.ticks(10).map(roundEpsilon) == [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0].reverse()
    assert s.ticks(9).map(roundEpsilon) ==  [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0].reverse()
    assert s.ticks(8).map(roundEpsilon) ==  [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0].reverse()
    assert s.ticks(7).map(roundEpsilon) ==  [0.0,      0.2,      0.4,      0.6,      0.8,      1.0].reverse()
    assert s.ticks(6).map(roundEpsilon) ==  [0.0,      0.2,      0.4,      0.6,      0.8,      1.0].reverse()
    assert s.ticks(5).map(roundEpsilon) ==  [0.0,      0.2,      0.4,      0.6,      0.8,      1.0].reverse()
    assert s.ticks(4).map(roundEpsilon) ==  [0.0,      0.2,      0.4,      0.6,      0.8,      1.0].reverse()
    assert s.ticks(3).map(roundEpsilon) ==  [0.0,                     0.5,                     1.0].reverse()
    assert s.ticks(2).map(roundEpsilon) ==  [0.0,                     0.5,                     1.0].reverse()
    assert s.ticks(1).map(roundEpsilon) ==  [0.0,                                              1.0].reverse()
    s.domain([100, -100])
    assert s.ticks(10) == [-100, -80, -60,      -40, -20, 0, 20, 40,     60, 80, 100].reverse()
    assert s.ticks(9) ==  [-100, -80, -60,      -40, -20, 0, 20, 40,     60, 80, 100].reverse()
    assert s.ticks(8) ==  [-100, -80, -60,      -40, -20, 0, 20, 40,     60, 80, 100].reverse()
    assert s.ticks(7) ==  [-100, -80, -60,      -40, -20, 0, 20, 40,     60, 80, 100].reverse()
    assert s.ticks(6) ==  [-100,           -50,           0,         50,         100].reverse()
    assert s.ticks(5) ==  [-100,           -50,           0,         50,         100].reverse()
    assert s.ticks(4) ==  [-100,           -50,           0,         50,         100].reverse()
    assert s.ticks(3) ==  [-100,           -50,           0,         50,         100].reverse()
    assert s.ticks(2) ==  [-100,                          0,                     100].reverse()
    assert s.ticks(1) ==  [                               0                         ].reverse()


def test_linear_40():
    s = d3.scale_linear().domain([0, 0.25, 0.9, 1])
    assert s.ticks(10).map(roundEpsilon) == [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    assert s.ticks(9).map(roundEpsilon) ==  [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    assert s.ticks(8).map(roundEpsilon) ==  [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    assert s.ticks(7).map(roundEpsilon) ==  [0.0,      0.2,      0.4,      0.6,      0.8,      1.0]
    assert s.ticks(6).map(roundEpsilon) ==  [0.0,      0.2,      0.4,      0.6,      0.8,      1.0]
    assert s.ticks(5).map(roundEpsilon) ==  [0.0,      0.2,      0.4,      0.6,      0.8,      1.0]
    assert s.ticks(4).map(roundEpsilon) ==  [0.0,      0.2,      0.4,      0.6,      0.8,      1.0]
    assert s.ticks(3).map(roundEpsilon) ==  [0.0,                     0.5,                     1.0]
    assert s.ticks(2).map(roundEpsilon) ==  [0.0,                     0.5,                     1.0]
    assert s.ticks(1).map(roundEpsilon) ==  [0.0,                                              1.0]
    s.domain([-100, 0, 100])
    assert s.ticks(10) == [-100, -80, -60,      -40, -20, 0, 20, 40,     60, 80, 100]
    assert s.ticks(9) ==  [-100, -80, -60,      -40, -20, 0, 20, 40,     60, 80, 100]
    assert s.ticks(8) ==  [-100, -80, -60,      -40, -20, 0, 20, 40,     60, 80, 100]
    assert s.ticks(7) ==  [-100, -80, -60,      -40, -20, 0, 20, 40,     60, 80, 100]
    assert s.ticks(6) ==  [-100,           -50,           0,         50,         100]
    assert s.ticks(5) ==  [-100,           -50,           0,         50,         100]
    assert s.ticks(4) ==  [-100,           -50,           0,         50,         100]
    assert s.ticks(3) ==  [-100,           -50,           0,         50,         100]
    assert s.ticks(2) ==  [-100,                          0,                     100]
    assert s.ticks(1) ==  [                               0                         ]


def test_linear_41():
    def check(domain, count):
        s = d3.scale_linear().domain(domain).nice(count)
        ticks = s.ticks(count)
        assert [ticks[0], ticks[ticks.length - 1]] == s.domain()
    check([1, 9], 2)
    check([1, 9], 3)
    check([1, 9], 4)
    check([8, 9], 2)
    check([8, 9], 3)
    check([8, 9], 4)
    check([1, 21], 2)
    check([2, 21], 2)
    check([3, 21], 2)
    check([4, 21], 2)
    check([5, 21], 2)
    check([6, 21], 2)
    check([7, 21], 2)
    check([8, 21], 2)
    check([9, 21], 2)
    check([10, 21], 2)
    check([11, 21], 2)

def test_linear_42():
    s = d3.scale_linear()
    assert s.ticks(math.nan) == []
    assert s.ticks(0) == []
    assert s.ticks(-1) == []
    assert s.ticks(Infinity) == []


def test_linear_43():
    s = d3.scale_linear()
    assert s.ticks() == s.ticks(10)


def test_linear_44():
    assert d3.scale_linear().tickFormat()(0.2) == "0.2"
    assert d3.scale_linear().domain([-100, 100]).tickFormat()(-20) == "−20"


def test_linear_45():
    assert d3.scale_linear().tickFormat(10)(0.2) == "0.2"
    assert d3.scale_linear().tickFormat(20)(0.2) == "0.20"
    assert d3.scale_linear().domain([-100, 100]).tickFormat(10)(-20) == "−20"


def test_linear_46():
    assert d3.scale_linear().tickFormat(10, "+f")(0.2) == "+0.2"
    assert d3.scale_linear().tickFormat(20, "+f")(0.2) == "+0.20"
    assert d3.scale_linear().tickFormat(10, "+%")(0.2) == "+20%"
    assert d3.scale_linear().domain([0.19, 0.21]).tickFormat(10, "+%")(0.2) == "+20.0%"


def test_linear_47():
    assert d3.scale_linear().domain([0, 9]).tickFormat(10, "")(2.10) == "2"
    assert d3.scale_linear().domain([0, 9]).tickFormat(100, "")(2.01) == "2"
    assert d3.scale_linear().domain([0, 9]).tickFormat(100, "")(2.11) == "2.1"
    assert d3.scale_linear().domain([0, 9]).tickFormat(10, "e")(2.10) == "2e+0"
    assert d3.scale_linear().domain([0, 9]).tickFormat(100, "e")(2.01) == "2.0e+0"
    assert d3.scale_linear().domain([0, 9]).tickFormat(100, "e")(2.11) == "2.1e+0"
    assert d3.scale_linear().domain([0, 9]).tickFormat(10, "g")(2.10) == "2"
    assert d3.scale_linear().domain([0, 9]).tickFormat(100, "g")(2.01) == "2.0"
    assert d3.scale_linear().domain([0, 9]).tickFormat(100, "g")(2.11) == "2.1"
    assert d3.scale_linear().domain([0, 9]).tickFormat(10, "r")(2.10e6) == "2000000"
    assert d3.scale_linear().domain([0, 9]).tickFormat(100, "r")(2.01e6) == "2000000"
    assert d3.scale_linear().domain([0, 9]).tickFormat(100, "r")(2.11e6) == "2100000"
    assert d3.scale_linear().domain([0, 0.9]).tickFormat(10, "p")(0.210) == "20%"
    assert d3.scale_linear().domain([0.19, 0.21]).tickFormat(10, "p")(0.201) == "20.1%"


def test_linear_48():
    assert d3.scale_linear().domain([0, 1e6]).tickFormat(10, "$s")(0.51e6) == "$0.5M"
    assert d3.scale_linear().domain([0, 1e6]).tickFormat(100, "$s")(0.501e6) == "$0.50M"


def test_linear_49():
    f = d3.scale_linear().domain([0, math.nan]).tickFormat()
    assert f + "" == " >-,f"
    assert f(0.12) == "0.120000"


def test_linear_50():
    x = d3.scale_linear()
    y = x.copy()
    x.domain([1, 2])
    assert y.domain() == [0, 1]
    assert x(1) == 0
    assert y(1) == 1
    y.domain([2, 3])
    assert x(2) == 1
    assert y(2) == 0
    assert x.domain() == [1, 2]
    assert y.domain() == [2, 3]
    y2 = x.domain([1, 1.9]).copy()
    x.nice(5)
    assert x.domain() == [1, 2]
    assert y2.domain() == [1, 1.9]


def test_linear_51():
    x = d3.scale_linear()
    y = x.copy()
    x.range([1, 2])
    assert x.invert(1) == 0
    assert y.invert(1) == 1
    assert y.range() == [0, 1]
    y.range([2, 3])
    assert x.invert(2) == 1
    assert y.invert(2) == 0
    assert x.range() == [1, 2]
    assert y.range() == [2, 3]


def test_linear_52():
    x = d3.scale_linear().range(["red", "blue"])
    y = x.copy()
    i0 = x.interpolate()
    def i1(a, b):
        def f():
            return b
        return f

    x.interpolate(i1)
    assert y.interpolate() == i0
    assert x(0.5) == "blue"
    assert y(0.5) == "rgb(128, 0, 128)"


def test_linear_53():
    x = d3.scale_linear().clamp(True)
    y = x.copy()
    x.clamp(False)
    assert x(2) == 2
    assert y(2) == 1
    assert y.clamp() == True
    y.clamp(False)
    assert x(2) == 2
    assert y(2) == 2
    assert x.clamp() == False


def test_linear_54():
    x = d3.scale_linear()
    y = x.copy()
    x.unknown(2)
    assert x(math.nan) == 2
    assert ismath.nan(y(math.nan)) == True
    assert y.unknown() == None
    y.unknown(3)
    assert x(math.nan) == 2
    assert y(math.nan) == 3
    assert x.unknown() == 2
