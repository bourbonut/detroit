import detroit as d3
import math
from datetime import datetime
import pytest
from functools import partial

def test_log_1():
    x = d3.scale_log()
    assert x.domain == [1, 10]
    assert x.range == [0, 1]
    assert x.clamp is False
    assert x.base == 10
    assert x.interpolate == d3.interpolate
    assert x.interpolate({"array": ["red"]}, {"array": ["blue"]})(0.5), {"array": ["rgb(128, 0, 128)"]}
    assert math.isclose(x(5), 0.69897, rel_tol=1e-6)
    assert math.isclose(x.invert(0.69897), 5, rel_tol=1e-6)
    assert math.isclose(x(3.162278), 0.5, rel_tol=1e-6)
    assert math.isclose(x.invert(0.5), 3.162278, rel_tol=1e-6)

def test_log_2():
    x = d3.scale_log().set_domain([datetime(1990, 1, 1), datetime(1991, 1, 1)])
    assert isinstance(x.domain[0], datetime)
    assert isinstance(x.domain[1], datetime)
    assert math.isclose(x(datetime(1989, 10, 20)), -0.2061048, rel_tol=1e-3)
    assert math.isclose(x(datetime(1990, 1, 1)),   0.0000000, rel_tol=1e-3)
    assert math.isclose(x(datetime(1990, 3, 15)),  0.2039385, rel_tol=1e-3)
    assert math.isclose(x(datetime(1990, 5, 27)),  0.4057544, rel_tol=1e-3)
    assert math.isclose(x(datetime(1991, 1,  1)),  1.0000000, rel_tol=1e-3)
    assert math.isclose(x(datetime(1991, 3, 15)),  1.1942797, rel_tol=1e-3)
    x.set_domain(["1", "10"])
    assert isinstance(x.domain[0], float)
    assert isinstance(x.domain[1], float)
    assert math.isclose(x(5), 0.69897, rel_tol=1e-3)
    x.set_domain([1, 10])
    assert isinstance(x.domain[0], int)
    assert isinstance(x.domain[1], int)
    assert math.isclose(x(5), 0.69897, rel_tol=1e-3)

def test_log_3():
    x = d3.scale_log().set_domain([-100, -1])
    assert list(map(x.tick_format(math.inf), x.ticks())) == [
        "-100", "-90", "-80", "-70", "-60", "-50", "-40", "-30", "-20",
        "-10", "-9", "-8", "-7", "-6", "-5", "-4", "-3", "-2", "-1"
    ]
    assert math.isclose(x(-50), 0.150515, rel_tol=1e-6)

def test_log_4():
    x = d3.scale_log().set_domain([0.1, 1, 100]).set_range(["red", "white", "green"])
    assert x(0.5) == "rgb(255, 178, 178)"
    assert x(50) == "rgb(38, 147, 38)"
    assert x(75) == "rgb(16, 136, 16)"

def test_log_5():
    x = d3.scale_log().set_domain([0.1, 1000])
    assert x.domain == [0.1, 1000]

def test_log_6():
    assert d3.scale_log().set_domain([0.15, 0.68]).ticks() == [0.2, 0.3, 0.4, 0.5, 0.6]
    assert d3.scale_log().set_domain([0.68, 0.15]).ticks() == [0.6, 0.5, 0.4, 0.3, 0.2]
    assert d3.scale_log().set_domain([-0.15, -0.68]).ticks() == [-0.2, -0.3, -0.4, -0.5, -0.6]
    assert d3.scale_log().set_domain([-0.68, -0.15]).ticks() == [-0.6, -0.5, -0.4, -0.3, -0.2]

def test_log_7():
    x = d3.scale_log().set_range(["0", "2"])
    assert isinstance(x.range[0], str)
    assert isinstance(x.range[1], str)

def test_log_8():
    x = d3.scale_log().set_range(["red", "blue"])
    assert x(5) == "rgb(77, 0, 178)"
    x.set_range(["#ff0000", "#0000ff"])
    assert x(5) == "rgb(77, 0, 178)"
    x.set_range(["#f00", "#00f"])
    assert x(5) == "rgb(77, 0, 178)"
    x.set_range([d3.rgb(255, 0, 0), d3.hsl(240, 1, 0.5)])
    assert x(5) == "rgb(77, 0, 178)"
    x.set_range(["hsl(0,100%,50%)", "hsl(240,100%,50%)"])
    assert x(5) == "rgb(77, 0, 178)"

def test_log_9():
    x = d3.scale_log().set_range([{"color": "red"}, {"color": "blue"}])
    assert x(5), {"color": "rgb(77, 0, 178)"}
    x.set_range([["red"], ["blue"]])
    assert x(5) == ["rgb(77, 0, 178)"]

def test_log_10():
    x = d3.scale_log().set_range(["red", "blue"])
    assert x.interpolate == d3.interpolate
    assert x(5) == "rgb(77, 0, 178)"
    x.set_interpolate(d3.interpolate_hsl)
    assert x(5) == "rgb(154, 0, 255)"

def test_log_11():
    x = d3.scale_log()
    assert x.clamp is False
    assert math.isclose(x(0.5), -0.3010299, rel_tol=1e-6)
    assert math.isclose(x(15), 1.1760913, rel_tol=1e-6)

def test_log_12():
    x = d3.scale_log().set_clamp(True)
    assert math.isclose(x(-1), 0, rel_tol=1e-6)
    assert math.isclose(x(5), 0.69897, rel_tol=1e-6)
    assert math.isclose(x(15), 1, rel_tol=1e-6)
    x.set_domain([10, 1])
    assert math.isclose(x(-1), 1, rel_tol=1e-6)
    assert math.isclose(x(5), 0.30103, rel_tol=1e-6)
    assert math.isclose(x(15), 0, rel_tol=1e-6)

def test_log_13():
    x = d3.scale_log().set_clamp(True)
    assert math.isclose(x.invert(-0.1), 1, rel_tol=1e-6)
    assert math.isclose(x.invert(0.69897), 5, rel_tol=1e-6)
    assert math.isclose(x.invert(1.5), 10, rel_tol=1e-6)
    x.set_domain([10, 1])
    assert math.isclose(x.invert(-0.1), 10, rel_tol=1e-6)
    assert math.isclose(x.invert(0.30103), 5, rel_tol=1e-6)
    assert math.isclose(x.invert(1.5), 1, rel_tol=1e-6)

def test_log_14():
    x = d3.scale_log().set_domain([1, 2])
    assert math.isclose(x(0.5),   -1.0000000, rel_tol=1e-6)
    assert math.isclose(x(1.0),    0.0000000, rel_tol=1e-6)
    assert math.isclose(x(1.5),    0.5849625, rel_tol=1e-6)
    assert math.isclose(x(2.0),    1.0000000, rel_tol=1e-6)
    assert math.isclose(x(2.5),    1.3219281, rel_tol=1e-6)

def test_log_15():
    x = d3.scale_log().set_domain([1, 2])
    assert math.isclose(x.invert(-1.0000000), 0.5, rel_tol=1e-6)
    assert math.isclose(x.invert( 0.0000000), 1.0, rel_tol=1e-6)
    assert math.isclose(x.invert( 0.5849625), 1.5, rel_tol=1e-6)
    assert math.isclose(x.invert( 1.0000000), 2.0, rel_tol=1e-6)
    assert math.isclose(x.invert( 1.3219281), 2.5, rel_tol=1e-6)

def test_log_16():
    x = d3.scale_log().set_range(["0", "2"])
    assert math.isclose(x.invert("1"), 3.1622777, rel_tol=1e-6)
    x.set_range([datetime(1990, 1, 1), datetime(1991, 1, 1)])
    assert math.isclose(x.invert(datetime(1990, 7, 2, 13)), 3.1622777, rel_tol=1e-6)
    x.set_range(["#000", "#fff"])
    with pytest.raises(ValueError):
        x.invert("#999")

def test_log_17():
    x = d3.scale_log().set_domain([1, 32])
    assert list(map(x.tick_format(), x.set_base(2).ticks())) == ["1", "2", "4", "8", "16", "32"]
    assert list(map(x.tick_format(), x.set_base(math.e).ticks())) == ["1", "2.71828182846", "7.38905609893", "20.0855369232"]

def test_log_18():
    x = d3.scale_log().set_domain([1.1, 10.9]).nice()
    assert x.domain == [1, 100]
    x.set_domain([10.9, 1.1]).nice()
    assert x.domain == [100, 1]
    x.set_domain([0.7, 11.001]).nice()
    assert x.domain == [0.1, 100]
    x.set_domain([123.1, 6.7]).nice()
    assert x.domain == [1000, 1]
    x.set_domain([0.01, 0.49]).nice()
    assert x.domain == [0.01, 1]
    x.set_domain([1.5, 50]).nice()
    assert x.domain == [1, 100]
    assert x(1) == 0
    assert x(100) == 1

def test_log_19():
    x = d3.scale_log().set_domain([0, 0]).nice()
    assert x.domain == [0, 0]
    x.set_domain([0.5, 0.5]).nice()
    assert x.domain == [0.1, 1]

def test_log_20():
    x = d3.scale_log().set_domain([1.1, 1.5, 10.9]).nice()
    assert x.domain == [1, 1.5, 100]
    x.set_domain([-123.1, -1.5, -0.5]).nice()
    assert x.domain == [-1000, -1.5, -0.1]

def test_log_21():
    x = d3.scale_log()
    y = x.copy()
    x.set_domain([10, 100])
    assert y.domain == [1, 10]
    assert x(10) == 0
    assert y(1) == 0
    y.set_domain([100, 1000])
    assert x(100) == 1
    assert y(100) == 0
    assert x.domain == [10, 100]
    assert y.domain == [100, 1000]

def test_log_22():
    x = d3.scale_log().set_domain([1.5, 50])
    y = x.copy().nice()
    assert x.domain == [1.5, 50]
    assert x(1.5) == 0
    assert x(50) == 1
    assert x.invert(0) == 1.5
    assert math.isclose(x.invert(1), 50, rel_tol=1e-6)
    assert y.domain == [1, 100]
    assert y(1) == 0
    assert y(100) == 1
    assert y.invert(0) == 1
    assert math.isclose(y.invert(1), 100, rel_tol=1e-6)

def test_log_23():
    x = d3.scale_log()
    y = x.copy()
    x.set_range([1, 2])
    assert x.invert(1) == 1
    assert math.isclose(y.invert(1), 10, rel_tol=1e-6)
    assert y.range == [0, 1]
    y.set_range([2, 3])
    assert math.isclose(x.invert(2), 10, rel_tol=1e-6)
    assert y.invert(2) == 1
    assert x.range == [1, 2]
    assert y.range == [2, 3]

def test_log_24():
    x = d3.scale_log().set_range(["red", "blue"])
    y = x.copy()
    x.set_interpolate(d3.interpolate_hsl)
    assert x(5) == "rgb(154, 0, 255)"
    assert y(5) == "rgb(77, 0, 178)"
    assert y.interpolate == d3.interpolate

def test_log_25():
    x = d3.scale_log().set_clamp(True)
    y = x.copy()
    x.set_clamp(False)
    assert math.isclose(x(0.5), -0.30103, rel_tol=1e-6)
    assert y(0.5) == 0
    assert y.clamp is True
    y.set_clamp(False)
    assert math.isclose(x(20), 1.30103, rel_tol=1e-6)
    assert math.isclose(y(20), 1.30103, rel_tol=1e-6)
    assert x.clamp is False

def test_log_26():
    s = d3.scale_log()
    assert list(map(partial(round, ndigits=1), s.set_domain([1e-1, 1e1]).ticks())) == [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert list(map(partial(round, ndigits=1), s.set_domain([1e-1, 1e0]).ticks())) == [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    assert list(map(partial(round, ndigits=1), s.set_domain([-1e0, -1e-1]).ticks())) == [-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1]


def test_log_27():
    s = d3.scale_log()
    assert list(map(partial(round, ndigits=1), s.set_domain([-1e-1, -1e1]).ticks())) == [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1][::-1]
    assert list(map(partial(round, ndigits=1), s.set_domain([-1e-1, -1e0]).ticks())) == [-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1][::-1]
    assert list(map(partial(round, ndigits=1), s.set_domain([1e0, 1e-1]).ticks())) == [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1][::-1]

def test_log_28():
    s = d3.scale_log()
    assert s.set_domain([1, 5]).ticks() == [1, 2, 3, 4, 5]
    assert s.set_domain([5, 1]).ticks() == [5, 4, 3, 2, 1]
    assert s.set_domain([-1, -5]).ticks() == [-1, -2, -3, -4, -5]
    assert s.set_domain([-5, -1]).ticks() == [-5, -4, -3, -2, -1]
    assert s.set_domain([286.9252014, 329.4978332]).ticks(1) == [300]
    assert s.set_domain([286.9252014, 329.4978332]).ticks(2) == [300]
    assert s.set_domain([286.9252014, 329.4978332]).ticks(3) == [300, 320]
    assert s.set_domain([286.9252014, 329.4978332]).ticks(4) == [290, 300, 310, 320]
    assert s.set_domain([286.9252014, 329.4978332]).ticks() == [290, 295, 300, 305, 310, 315, 320, 325]

def test_log_29():
    s = d3.scale_log()
    assert s.set_domain([41, 42]).ticks() == [41, 41.1, 41.2, 41.3, 41.4, 41.5, 41.6, 41.7, 41.8, 41.9, 42]
    assert s.set_domain([42, 41]).ticks() == [42, 41.9, 41.8, 41.7, 41.6, 41.5, 41.4, 41.3, 41.2, 41.1, 41]
    assert s.set_domain([1600, 1400]).ticks() == [1600, 1580, 1560, 1540, 1520, 1500, 1480, 1460, 1440, 1420, 1400]

def test_log_30():
    s = d3.scale_log().set_base(math.e)
    assert list(map(partial(round, ndigits=12), s.set_domain([0.1, 100]).ticks())) == [0.135335283237, 0.367879441171, 1, 2.718281828459, 7.389056098931, 20.085536923188, 54.598150033144]

def test_log_31():
    s = d3.scale_log()
    assert list(map(s.tick_format(), s.set_domain([1e-1, 1e1]).ticks())) == ["100m", "200m", "300m", "400m", "500m", "600m", "700m", "800m", "900m", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

def test_log_32():
    s = d3.scale_log()
    t = s.set_domain([1e-1, 1e1]).ticks()
    assert list(map(s.tick_format(10), t)) == ["100m", "200m", "300m", "400m", "500m", "", "", "", "", "1", "2", "3", "4", "5", "", "", "", "", "10"]
    assert list(map(s.tick_format(5), t)) == ["100m", "200m", "", "", "", "", "", "", "", "1", "2", "", "", "", "", "", "", "", "10"]
    assert list(map(s.tick_format(1), t)) == ["100m", "", "", "", "", "", "", "", "", "1", "", "", "", "", "", "", "", "", "10"]
    assert list(map(s.tick_format(0), t)) == ["100m", "", "", "", "", "", "", "", "", "1", "", "", "", "", "", "", "", "", "10"]

def test_log_33():
    s = d3.scale_log()
    t = s.set_domain([1e-1, 1e1]).ticks()
    assert list(map(s.tick_format(10, "+"), t)) == ["+0.1", "+0.2", "+0.3", "+0.4", "+0.5", "", "", "", "", "+1", "+2", "+3", "+4", "+5", "", "", "", "", "+10"]

def test_log_34():
    s = d3.scale_log().set_base(math.e)
    assert list(map(s.tick_format(), s.set_domain([1e-1, 1e1]).ticks())) == ["0.135335283237", "0.367879441171", "1", "2.71828182846", "7.38905609893"]

def test_log_35():
    s = d3.scale_log().set_base(16)
    t = s.set_domain([1e-1, 1e1]).ticks()
    assert list(map(s.tick_format(10), t)) == ["0.125", "0.1875", "0.25", "0.3125", "0.375", "", "", "", "", "", "", "", "", "", "1", "2", "3", "4", "5", "6", "", "", "", ""]
    assert list(map(s.tick_format(5), t)) == ["0.125", "0.1875", "", "", "", "", "", "", "", "", "", "", "", "", "1", "2", "3", "", "", "", "", "", "", ""]
    assert list(map(s.tick_format(1), t)) == ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "1", "", "", "", "", "", "", "", "", ""]

def test_log_36():
    x = d3.scale_log()
    assert list(map(x.tick_format(math.inf), x.ticks())) == [
        "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "10"
    ]
    x.set_domain([100, 1])
    assert list(map(x.tick_format(math.inf), x.ticks())) == [
        "100",
        "90", "80", "70", "60", "50", "40", "30", "20", "10",
        "9", "8", "7", "6", "5", "4", "3", "2", "1"
    ]
    x.set_domain([0.49999, 0.006029505943610648])
    assert list(map(x.tick_format(math.inf), x.ticks())) == [
        "400m", "300m", "200m", "100m",
        "90m", "80m", "70m", "60m", "50m", "40m", "30m", "20m", "10m",
        "9m", "8m", "7m"
    ]
    x.set_domain([0.95, 1.05e8])
    assert list(filter(lambda x: len(x) > 0, map(x.tick_format(8), x.ticks()))) == [
        "1", "10", "100", "1k", "10k", "100k", "1M", "10M", "100M"
    ]

def test_log_37():
    x = d3.scale_log()
    assert list(map(x.tick_format(5), x.ticks())) == [
        "1", "2", "3", "4", "5", "", "", "", "",
        "10"
    ]
    x.set_domain([100, 1])
    assert list(map(x.tick_format(10), x.ticks())) == [
        "100",
        "", "", "", "", "50", "40", "30", "20", "10",
        "", "", "", "", "5", "4", "3", "2", "1"
    ]

def test_log_38():
    x = d3.scale_log().set_domain([1e10, 1])
    assert list(map(x.tick_format(), x.ticks())) == ["10G", "1G", "100M", "10M", "1M", "100k", "10k", "1k", "100", "10", "1"]
    x.set_domain([1e-29, 1e-1])
    assert list(map(x.tick_format(), x.ticks())) == ["0.0001y", "0.01y", "1y", "100y", "10z", "1a", "100a", "10f", "1p", "100p", "10n", "1µ", "100µ", "10m"]

def test_log_39():
    x = d3.scale_log().set_domain([0.01, 10000])
    assert list(map(x.tick_format(20), x.ticks(20))) == [
        "10m", "20m", "30m", "", "", "", "", "", "",
        "100m", "200m", "300m", "", "", "", "", "", "",
        "1", "2", "3", "", "", "", "", "", "",
        "10", "20", "30", "", "", "", "", "", "",
        "100", "200", "300", "", "", "", "", "", "",
        "1k", "2k", "3k", "", "", "", "", "", "",
        "10k"
    ]

def test_log_40():
    x = d3.scale_log().set_domain([0.0124123, 1230.4]).nice()
    assert list(map(x.tick_format(20), x.ticks(20))) == [
        "10m", "20m", "30m", "", "", "", "", "", "",
        "100m", "200m", "300m", "", "", "", "", "", "",
        "1", "2", "3", "", "", "", "", "", "",
        "10", "20", "30", "", "", "", "", "", "",
        "100", "200", "300", "", "", "", "", "", "",
        "1k", "2k", "3k", "", "", "", "", "", "",
        "10k"
    ]

def test_log_41():
    x = d3.scale_log().set_domain([1000.1, 1])
    assert list(map(x.tick_format(10, format("+,d")), x.ticks())) == [
        "+1,000",
        "", "", "", "", "", "", "+300", "+200", "+100",
        "", "", "", "", "", "", "+30", "+20", "+10",
        "", "", "", "", "", "", "+3", "+2", "+1"
    ]

def test_log_42():
    x = d3.scale_log().set_domain([1000.1, 1])
    assert list(map(x.tick_format(10, "s"), x.ticks())) == [
        "1k",
        "", "", "", "", "", "", "300", "200", "100",
        "", "", "", "", "", "", "30", "20", "10",
        "", "", "", "", "", "", "3", "2", "1"
    ]

def test_log_43():
    x = d3.scale_log().set_domain([100.1, 0.02])
    assert list(map(x.tick_format(10, "f"), x.ticks())) == [
        "100",
        "", "", "", "", "", "", "", "20", "10",
        "", "", "", "", "", "", "", "2", "1",
        "", "", "", "", "", "", "", "0.2", "0.1",
        "", "", "", "", "", "", "", "0.02"
    ]

def test_log_44():
    x = d3.scale_log().set_base(2).set_domain([100.1, 0.02])
    assert list(map(x.tick_format(10, "f"), x.ticks())) == [
        "64", "32", "16", "8", "4", "2", "1", "0.5", "0.25", "0.125", "0.0625", "0.03125"
    ]

def test_log_45():
    x = d3.scale_log().set_domain([100.1, 0.02])
    assert list(map(x.tick_format(10, ".1f"), x.ticks())) == [
        "100.0",
        "", "", "", "", "", "", "", "20.0", "10.0",
        "", "", "", "", "", "", "", "2.0", "1.0",
        "", "", "", "", "", "", "", "0.2", "0.1",
        "", "", "", "", "", "", "", "0.0"
    ]

def test_log_46():
    x = d3.scale_log()
    with pytest.raises(ValueError):
        assert x.set_domain([0, 1]).ticks() == []
    with pytest.raises(ValueError):
        assert x.set_domain([1, 0]).ticks() == []
    with pytest.raises(ValueError):
        assert x.set_domain([0, -1]).ticks() == []
    with pytest.raises(ValueError):
        assert x.set_domain([-1, 0]).ticks() == []
    with pytest.raises(ValueError):
        assert x.set_domain([-1, 1]).ticks() == []
    with pytest.raises(ValueError):
        assert x.set_domain([0, 0]).ticks() == []
