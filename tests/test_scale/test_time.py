from datetime import datetime

import pytest

import detroit as d3


def test_time_1():
    x = d3.scale_time().set_domain({datetime(2009, 1, 1), datetime(2010, 1, 1)})
    assert sorted(x.get_domain()) == sorted([datetime(2009, 1, 1), datetime(2010, 1, 1)])


def test_time_2():
    x = d3.scale_time().set_domain(
        [datetime(2009, 1, 1, 0, 17), datetime(2009, 1, 1, 23, 42)]
    )
    assert x.nice().get_domain() == [datetime(2009, 1, 1), datetime(2009, 1, 2)]


def test_time_3():
    x = d3.scale_time().set_domain(
        [datetime(2013, 1, 1, 12, 0, 0, 0), datetime(2013, 1, 1, 12, 0, 0, 128000)]
    )
    assert x.nice().get_domain() == [
        datetime(2013, 1, 1, 12, 0, 0, 0),
        datetime(2013, 1, 1, 12, 0, 0, 130000),
    ]


def test_time_4():
    x = d3.scale_time().set_domain([datetime(2001, 1, 1), datetime(2138, 1, 1)])
    assert x.nice().get_domain() == [datetime(2000, 1, 1), datetime(2140, 1, 1)]


def test_time_5():
    x = d3.scale_time().set_domain(
        [datetime(2009, 1, 1, 0, 12), datetime(2009, 1, 1, 0, 12)]
    )
    assert x.nice().get_domain() == [
        datetime(2009, 1, 1, 0, 12),
        datetime(2009, 1, 1, 0, 12),
    ]


def test_time_6():
    x = d3.scale_time().set_domain(
        [datetime(2009, 1, 1, 0, 17), datetime(2009, 1, 1, 23, 42)]
    )
    assert x.nice(100).get_domain() == [
        datetime(2009, 1, 1, 0, 15),
        datetime(2009, 1, 1, 23, 45),
    ]
    assert x.nice(10).get_domain() == [datetime(2009, 1, 1), datetime(2009, 1, 2)]


def test_time_7():
    x = d3.scale_time().set_domain(
        [datetime(2009, 1, 1, 0, 12), datetime(2009, 1, 1, 23, 48)]
    )
    assert x.nice(d3.time_day).get_domain() == [datetime(2009, 1, 1), datetime(2009, 1, 2)]
    assert x.nice(d3.time_week).get_domain() == [
        datetime(2008, 12, 28),
        datetime(2009, 1, 4),
    ]
    assert x.nice(d3.time_month).get_domain() == [
        datetime(2008, 12, 1),
        datetime(2009, 2, 1),
    ]
    assert x.nice(d3.time_year).get_domain() == [datetime(2008, 1, 1), datetime(2010, 1, 1)]


def test_time_8():
    x = d3.scale_time().set_domain(
        [datetime(2009, 1, 1, 0, 12), datetime(2009, 1, 1, 0, 12)]
    )
    assert x.nice(d3.time_day).get_domain() == [datetime(2009, 1, 1), datetime(2009, 1, 2)]


def test_time_9():
    x = (
        d3.scale_time()
        .set_domain(
            [
                datetime(2009, 1, 1, 0, 12),
                datetime(2009, 1, 1, 23, 48),
                datetime(2009, 1, 2, 23, 48),
            ]
        )
        .nice(d3.time_day)
    )
    assert x.get_domain() == [
        datetime(2009, 1, 1),
        datetime(2009, 1, 1, 23, 48),
        datetime(2009, 1, 3),
    ]


def test_time_10():
    x = d3.scale_time().set_domain(
        [datetime(2009, 1, 1, 0, 12), datetime(2009, 1, 1, 23, 48)]
    )
    assert x.nice(d3.time_day.every(3)).get_domain() == [
        datetime(2009, 1, 1),
        datetime(2009, 1, 4),
    ]
    assert x.nice(d3.time_week.every(2)).get_domain() == [
        datetime(2008, 12, 28),  # maybe 2008, 12, 21
        datetime(2009, 1, 4),
    ]
    assert x.nice(d3.time_month.every(3)).get_domain() == [
        datetime(2008, 10, 1),
        datetime(2009, 4, 1),
    ]
    assert x.nice(d3.time_year.every(10)).get_domain() == [
        datetime(2000, 1, 1),
        datetime(2010, 1, 1),
    ]


def test_time_11():
    x = d3.scale_time().set_domain([datetime(2009, 1, 1), datetime(2010, 1, 1)])
    y = x.copy()
    x.set_domain([datetime(2010, 1, 1), datetime(2011, 1, 1)])
    assert y.get_domain() == [datetime(2009, 1, 1), datetime(2010, 1, 1)]
    assert x(datetime(2010, 1, 1)) == 0
    assert y(datetime(2010, 1, 1)) == 1
    y.set_domain([datetime(2011, 1, 1), datetime(2012, 1, 1)])
    assert x(datetime(2011, 1, 1)) == 1
    assert y(datetime(2011, 1, 1)) == 0
    assert x.get_domain() == [datetime(2010, 1, 1), datetime(2011, 1, 1)]
    assert y.get_domain() == [datetime(2011, 1, 1), datetime(2012, 1, 1)]


def test_time_12():
    x = d3.scale_time().set_domain([datetime(2009, 1, 1), datetime(2010, 1, 1)])
    y = x.copy()
    x.set_range([1, 2])
    assert x.invert(1) == datetime(2009, 1, 1)
    assert y.invert(1) == datetime(2010, 1, 1)
    assert y.get_range() == [0, 1]
    y.set_range([2, 3])
    assert x.invert(2) == datetime(2010, 1, 1)
    assert y.invert(2) == datetime(2009, 1, 1)
    assert x.get_range() == [1, 2]
    assert y.get_range() == [2, 3]


def test_time_13():
    x = (
        d3.scale_time()
        .set_domain([datetime(2009, 1, 1), datetime(2010, 1, 1)])
        .set_range(["red", "blue"])
    )
    i = x.get_interpolate()
    y = x.copy()
    x.set_interpolate(d3.interpolate_hsl)
    assert x(datetime(2009, 7, 1)) == "rgb(255, 0, 253)"
    assert y(datetime(2009, 7, 1)) == "rgb(129, 0, 126)"
    assert y.get_interpolate() == i


def test_time_14():
    x = (
        d3.scale_time()
        .set_domain([datetime(2009, 1, 1), datetime(2010, 1, 1)])
        .set_clamp(True)
    )
    y = x.copy()
    x.set_clamp(False)
    assert x(datetime(2011, 1, 1)) == 2
    assert y(datetime(2011, 1, 1)) == 1
    assert y.get_clamp() is True
    y.set_clamp(False)
    assert x(datetime(2011, 1, 1)) == 2
    assert y(datetime(2011, 1, 1)) == 2
    assert x.get_clamp() is False


def test_time_15():
    x = d3.scale_time().set_clamp(True)
    assert isinstance(x.invert(0), datetime)
    assert x.invert(-1) == x.get_domain()[0]
    assert x.invert(0) == x.get_domain()[0]
    assert x.invert(1) == x.get_domain()[1]
    assert x.invert(2) == x.get_domain()[1]


def test_time_16():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 12, 1, 0), datetime(2011, 1, 1, 12, 4, 4)]
    )
    assert x.ticks(d3.time_minute) == [
        datetime(2011, 1, 1, 12, 1),
        datetime(2011, 1, 1, 12, 2),
        datetime(2011, 1, 1, 12, 3),
        datetime(2011, 1, 1, 12, 4),
    ]


def test_time_17():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 33, 4)]
    )
    assert x.ticks(d3.time_minute.every(10)) == [
        datetime(2011, 1, 1, 12, 0),
        datetime(2011, 1, 1, 12, 10),
        datetime(2011, 1, 1, 12, 20),
        datetime(2011, 1, 1, 12, 30),
    ]


def test_time_18():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 0, 1)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 0, 0, 0),
        datetime(2011, 1, 1, 12, 0, 0, 200000),
        datetime(2011, 1, 1, 12, 0, 0, 400000),
        datetime(2011, 1, 1, 12, 0, 0, 600000),
        datetime(2011, 1, 1, 12, 0, 0, 800000),
        datetime(2011, 1, 1, 12, 0, 1, 0),
    ]


def test_time_19():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 0, 4)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 0, 0),
        datetime(2011, 1, 1, 12, 0, 1),
        datetime(2011, 1, 1, 12, 0, 2),
        datetime(2011, 1, 1, 12, 0, 3),
        datetime(2011, 1, 1, 12, 0, 4),
    ]


def test_time_20():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 0, 20)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 0, 0),
        datetime(2011, 1, 1, 12, 0, 5),
        datetime(2011, 1, 1, 12, 0, 10),
        datetime(2011, 1, 1, 12, 0, 15),
        datetime(2011, 1, 1, 12, 0, 20),
    ]


def test_time_21():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 0, 50)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 0, 0),
        datetime(2011, 1, 1, 12, 0, 15),
        datetime(2011, 1, 1, 12, 0, 30),
        datetime(2011, 1, 1, 12, 0, 45),
    ]


def test_time_22():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 1, 50)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 0, 0),
        datetime(2011, 1, 1, 12, 0, 30),
        datetime(2011, 1, 1, 12, 1, 0),
        datetime(2011, 1, 1, 12, 1, 30),
    ]


def test_time_23():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 12, 0, 27), datetime(2011, 1, 1, 12, 4, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 1),
        datetime(2011, 1, 1, 12, 2),
        datetime(2011, 1, 1, 12, 3),
        datetime(2011, 1, 1, 12, 4),
    ]


def test_time_24():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 12, 3, 27), datetime(2011, 1, 1, 12, 21, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 5),
        datetime(2011, 1, 1, 12, 10),
        datetime(2011, 1, 1, 12, 15),
        datetime(2011, 1, 1, 12, 20),
    ]


def test_time_25():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 12, 8, 27), datetime(2011, 1, 1, 13, 4, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 15),
        datetime(2011, 1, 1, 12, 30),
        datetime(2011, 1, 1, 12, 45),
        datetime(2011, 1, 1, 13, 0),
    ]


def test_time_26():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 12, 28, 27), datetime(2011, 1, 1, 14, 4, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 30),
        datetime(2011, 1, 1, 13, 0),
        datetime(2011, 1, 1, 13, 30),
        datetime(2011, 1, 1, 14, 0),
    ]


def test_time_27():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 12, 28, 27), datetime(2011, 1, 1, 16, 34, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 13, 0),
        datetime(2011, 1, 1, 14, 0),
        datetime(2011, 1, 1, 15, 0),
        datetime(2011, 1, 1, 16, 0),
    ]


def test_time_28():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 14, 28, 27), datetime(2011, 1, 2, 1, 34, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 15, 0),
        datetime(2011, 1, 1, 18, 0),
        datetime(2011, 1, 1, 21, 0),
        datetime(2011, 1, 2, 0, 0),
    ]


def test_time_29():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 16, 28, 27), datetime(2011, 1, 2, 14, 34, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 18, 0),
        datetime(2011, 1, 2, 0, 0),
        datetime(2011, 1, 2, 6, 0),
        datetime(2011, 1, 2, 12, 0),
    ]


def test_time_30():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 16, 28, 27), datetime(2011, 1, 3, 21, 34, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 2, 0, 0),
        datetime(2011, 1, 2, 12, 0),
        datetime(2011, 1, 3, 0, 0),
        datetime(2011, 1, 3, 12, 0),
    ]


def test_time_31():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 16, 28, 27), datetime(2011, 1, 5, 21, 34, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 2, 0, 0),
        datetime(2011, 1, 3, 0, 0),
        datetime(2011, 1, 4, 0, 0),
        datetime(2011, 1, 5, 0, 0),
    ]


def test_time_32():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 2, 16, 28, 27), datetime(2011, 1, 9, 21, 34, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 3, 0, 0),
        datetime(2011, 1, 5, 0, 0),
        datetime(2011, 1, 7, 0, 0),
        datetime(2011, 1, 9, 0, 0),
    ]


def test_time_33():
    x = d3.scale_time().set_domain(
        [datetime(2011, 1, 1, 16, 28, 27), datetime(2011, 1, 23, 21, 34, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 2, 0, 0),
        datetime(2011, 1, 9, 0, 0),
        datetime(2011, 1, 16, 0, 0),
        datetime(2011, 1, 23, 0, 0),
    ]


def test_time_34():
    x = d3.scale_time().set_domain([datetime(2011, 1, 18), datetime(2011, 5, 2)])
    assert x.ticks(4) == [
        datetime(2011, 2, 1, 0, 0),
        datetime(2011, 3, 1, 0, 0),
        datetime(2011, 4, 1, 0, 0),
        datetime(2011, 5, 1, 0, 0),
    ]


def test_time_35():
    x = d3.scale_time().set_domain([datetime(2010, 12, 18), datetime(2011, 11, 2)])
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 0, 0),
        datetime(2011, 4, 1, 0, 0),
        datetime(2011, 7, 1, 0, 0),
        datetime(2011, 10, 1, 0, 0),
    ]


def test_time_36():
    x = d3.scale_time().set_domain([datetime(2010, 12, 18), datetime(2014, 3, 2)])
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 0, 0),
        datetime(2012, 1, 1, 0, 0),
        datetime(2013, 1, 1, 0, 0),
        datetime(2014, 1, 1, 0, 0),
    ]


def test_time_37():
    # OverflowError : if all values (year, month, day, ...) are minimized
    # Thus datetime(1, 12, 18) raises an overflow error
    x = d3.scale_time().set_domain([datetime(501, 12, 18), datetime(2014, 3, 2)])
    assert x.ticks(4) == [
        datetime(1000, 1, 1, 0, 0),
        datetime(1500, 1, 1, 0, 0),
        datetime(2000, 1, 1, 0, 0),
    ]


def test_time_38():
    x = d3.scale_time().set_domain([datetime(2014, 3, 2), datetime(2014, 3, 2)])
    assert x.ticks(6) == [datetime(2014, 3, 2)]


def test_time_39():
    x = d3.scale_time()
    assert x.set_domain([datetime(2014, 3, 2), datetime(2010, 12, 18)]).ticks(4) == [
        datetime(2014, 1, 1, 0, 0),
        datetime(2013, 1, 1, 0, 0),
        datetime(2012, 1, 1, 0, 0),
        datetime(2011, 1, 1, 0, 0),
    ]
    assert x.set_domain([datetime(2011, 11, 2), datetime(2010, 12, 18)]).ticks(4) == [
        datetime(2011, 10, 1, 0, 0),
        datetime(2011, 7, 1, 0, 0),
        datetime(2011, 4, 1, 0, 0),
        datetime(2011, 1, 1, 0, 0),
    ]


def test_time_40():
    f = d3.scale_time().tick_format()
    assert f(datetime(2011, 1, 1)) == "2011"
    assert f(datetime(2012, 1, 1)) == "2012"
    assert f(datetime(2013, 1, 1)) == "2013"


def test_time_41():
    f = d3.scale_time().tick_format()
    assert f(datetime(2011, 2, 1)) == "February"
    assert f(datetime(2011, 3, 1)) == "March"
    assert f(datetime(2011, 4, 1)) == "April"


def test_time_42():
    f = d3.scale_time().tick_format()
    assert f(datetime(2011, 2, 6)) == "Feb 06"
    assert f(datetime(2011, 2, 13)) == "Feb 13"
    assert f(datetime(2011, 2, 20)) == "Feb 20"


def test_time_43():
    f = d3.scale_time().tick_format()
    assert f(datetime(2011, 2, 2)) == "Wed 02"
    assert f(datetime(2011, 2, 3)) == "Thu 03"
    assert f(datetime(2011, 2, 4)) == "Fri 04"


def test_time_44():
    f = d3.scale_time().tick_format()
    assert f(datetime(2011, 2, 2, 11)) == "11 AM"
    assert f(datetime(2011, 2, 2, 12)) == "12 PM"
    assert f(datetime(2011, 2, 2, 13)) == "01 PM"


def test_time_45():
    f = d3.scale_time().tick_format()
    assert f(datetime(2011, 2, 2, 11, 59)) == "11:59"
    assert f(datetime(2011, 2, 2, 12, 1)) == "12:01"
    assert f(datetime(2011, 2, 2, 12, 2)) == "12:02"


def test_time_46():
    f = d3.scale_time().tick_format()
    assert f(datetime(2011, 2, 2, 12, 1, 9)) == ":09"
    assert f(datetime(2011, 2, 2, 12, 1, 10)) == ":10"
    assert f(datetime(2011, 2, 2, 12, 1, 11)) == ":11"
