import detroit as d3
from datetime import datetime
import pytest


def test_datetimeTime_1():
    x = d3.scale_time().domain(
        [datetime(2009, 1, 1, 0, 17), datetime(2009, 1, 1, 23, 42)]
    )
    assert x.nice().domain() == [datetime(2009, 1, 1), datetime(2009, 1, 2)]


def test_datetimeTime_2():
    x = d3.scale_time().domain(
        [datetime(2013, 1, 1, 12, 0, 0, 0), datetime(2013, 1, 1, 12, 0, 0, 128000)]
    )
    assert x.nice().domain() == [
        datetime(2013, 1, 1, 12, 0, 0, 0),
        datetime(2013, 1, 1, 12, 0, 0, 130000),
    ]


def test_datetimeTime_3():
    x = d3.scale_time().domain([datetime(2001, 1, 1), datetime(2138, 1, 1)])
    with pytest.raises(ValueError):
        assert x.nice().domain() == [datetime(2000, 1, 1), datetime(2140, 1, 1)]


def test_datetimeTime_4():
    x = d3.scale_time().domain(
        [datetime(2009, 1, 1, 0, 12), datetime(2009, 1, 1, 0, 12)]
    )
    assert x.nice().domain() == [
        datetime(2009, 1, 1, 0, 12),
        datetime(2009, 1, 1, 0, 12),
    ]


def test_datetimeTime_5():
    x = d3.scale_time().domain(
        [datetime(2009, 1, 1, 0, 17), datetime(2009, 1, 1, 23, 42)]
    )
    assert x.nice(100).domain() == [
        datetime(2009, 1, 1, 0, 15),
        datetime(2009, 1, 1, 23, 45),
    ]
    assert x.nice(10).domain() == [datetime(2009, 1, 1), datetime(2009, 1, 2)]


def test_datetimeTime_6():
    x = d3.scale_time().domain(
        [datetime(2009, 1, 1, 0, 12), datetime(2009, 1, 1, 23, 48)]
    )
    assert x.nice(d3.time_day).domain() == [datetime(2009, 1, 1), datetime(2009, 1, 2)]
    assert x.nice(d3.time_week).domain() == [
        datetime(2008, 12, 28),
        datetime(2009, 1, 4),
    ]
    assert x.nice(d3.time_month).domain() == [
        datetime(2008, 12, 1),
        datetime(2009, 2, 1),
    ]
    assert x.nice(d3.time_year).domain() == [datetime(2008, 1, 1), datetime(2010, 1, 1)]


def test_datetimeTime_7():
    x = d3.scale_time().domain(
        [datetime(2009, 1, 1, 0, 12), datetime(2009, 1, 1, 0, 12)]
    )
    assert x.nice(d3.time_day).domain() == [datetime(2009, 1, 1), datetime(2009, 1, 2)]


def test_datetimeTime_8():
    x = (
        d3.scale_time()
        .domain(
            [
                datetime(2009, 1, 1, 0, 12),
                datetime(2009, 1, 1, 23, 48),
                datetime(2009, 1, 2, 23, 48),
            ]
        )
        .nice(d3.time_day)
    )
    assert x.domain() == [
        datetime(2009, 1, 1),
        datetime(2009, 1, 1, 23, 48),
        datetime(2009, 1, 3),
    ]


def test_datetimeTime_9():
    x = d3.scale_time().domain(
        [datetime(2009, 1, 1, 0, 12), datetime(2009, 1, 1, 23, 48)]
    )
    assert x.nice(d3.time_day.every(3)).domain() == [
        datetime(2009, 1, 1),
        datetime(2009, 1, 4),
    ]
    # TODO: solve these tests
    # assert x.nice(d3.time_week.every(2)).domain() == [
    #     datetime(2008, 12, 21),
    #     datetime(2009, 1, 4),
    # ]
    # assert x.nice(d3.time_month.every(3)).domain() == [
    #     datetime(2008, 10, 1),
    #     datetime(2009, 4, 1),
    # ]
    assert x.nice(d3.time_year.every(10)).domain() == [
        datetime(2000, 1, 1),
        datetime(2010, 1, 1),
    ]


def test_datetimeTime_10():
    x = d3.scale_time().domain([datetime(2009, 1, 1), datetime(2010, 1, 1)])
    y = x.copy()
    x.domain([datetime(2010, 1, 1), datetime(2011, 1, 1)])
    assert y.domain() == [datetime(2009, 1, 1), datetime(2010, 1, 1)]
    assert x(datetime(2010, 1, 2)) == 0
    assert y(datetime(2010, 1, 2)) == 1
    y.domain([datetime(2011, 1, 1), datetime(2012, 1, 1)])
    assert x(datetime(2011, 1, 2)) == 1
    assert y(datetime(2011, 1, 2)) == 0
    assert x.domain() == [datetime(2010, 1, 1), datetime(2011, 1, 1)]
    assert y.domain() == [datetime(2011, 1, 1), datetime(2012, 1, 1)]


def test_datetimeTime_11():
    x = d3.scale_time().domain([datetime(2009, 1, 1), datetime(2010, 1, 1)])
    y = x.copy()
    x.range([1, 2])
    assert x.invert(1) == datetime(2009, 1, 1)
    assert y.invert(1) == datetime(2010, 1, 1)
    assert y.range() == [0, 1]
    y.range([2, 3])
    assert x.invert(2) == datetime(2010, 1, 1)
    assert y.invert(2) == datetime(2009, 1, 1)
    assert x.range() == [1, 2]
    assert y.range() == [2, 3]


def test_datetimeTime_12():
    x = (
        d3.scale_time()
        .domain([datetime(2009, 1, 1), datetime(2010, 1, 1)])
        .range(["red", "blue"])
    )
    i = x.interpolate()
    y = x.copy()
    x.interpolate(d3.interpolate_hsl)
    assert x(datetime(2009, 6, 2)) == "rgb(255, 0, 253)"
    assert y(datetime(2009, 6, 2)) == "rgb(129, 0, 126)"
    assert y.interpolate() == i


def test_datetimeTime_13():
    x = d3.scale_time().domain([datetime(2009, 1, 1), datetime(2010, 1, 1)]).clamp(True)
    y = x.copy()
    x.clamp(False)
    assert y.clamp() is True
    assert x(datetime(2011, 1, 2)) == 2
    assert y(datetime(2011, 1, 2)) == 1
    y.clamp(False)
    assert x.clamp() is False
    assert x(datetime(2011, 1, 2)) == 2
    assert y(datetime(2011, 1, 2)) == 2


def test_datetimeTime_14():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 12, 1, 0), datetime(2011, 1, 1, 12, 4, 4)]
    )
    assert x.ticks(d3.time_minute) == [
        datetime(2011, 1, 1, 12, 1),
        datetime(2011, 1, 1, 12, 2),
        datetime(2011, 1, 1, 12, 3),
        datetime(2011, 1, 1, 12, 4),
    ]


def test_datetimeTime_15():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 12, 1, 0), datetime(2011, 1, 1, 12, 4, 4)]
    )
    assert x.ticks(d3.time_minute) == [
        datetime(2011, 1, 1, 12, 1),
        datetime(2011, 1, 1, 12, 2),
        datetime(2011, 1, 1, 12, 3),
        datetime(2011, 1, 1, 12, 4),
    ]


def test_datetimeTime_16():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 33, 4)]
    )
    assert x.ticks(d3.time_minute.every(10)) == [
        datetime(2011, 1, 1, 12, 0),
        datetime(2011, 1, 1, 12, 10),
        datetime(2011, 1, 1, 12, 20),
        datetime(2011, 1, 1, 12, 30),
    ]


def test_datetimeTime_17():
    x = d3.scale_time().domain(
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


def test_datetimeTime_18():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 0, 4)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 0, 0),
        datetime(2011, 1, 1, 12, 0, 1),
        datetime(2011, 1, 1, 12, 0, 2),
        datetime(2011, 1, 1, 12, 0, 3),
        datetime(2011, 1, 1, 12, 0, 4),
    ]


def test_datetimeTime_19():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 0, 20)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 0, 0),
        datetime(2011, 1, 1, 12, 0, 5),
        datetime(2011, 1, 1, 12, 0, 10),
        datetime(2011, 1, 1, 12, 0, 15),
        datetime(2011, 1, 1, 12, 0, 20),
    ]


def test_datetimeTime_20():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 0, 50)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 0, 0),
        datetime(2011, 1, 1, 12, 0, 15),
        datetime(2011, 1, 1, 12, 0, 30),
        datetime(2011, 1, 1, 12, 0, 45),
    ]


def test_datetimeTime_21():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 12, 0, 0), datetime(2011, 1, 1, 12, 1, 50)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 0, 0),
        datetime(2011, 1, 1, 12, 0, 30),
        datetime(2011, 1, 1, 12, 1, 0),
        datetime(2011, 1, 1, 12, 1, 30),
    ]


def test_datetimeTime_22():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 12, 0, 27), datetime(2011, 1, 1, 12, 4, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 1),
        datetime(2011, 1, 1, 12, 2),
        datetime(2011, 1, 1, 12, 3),
        datetime(2011, 1, 1, 12, 4),
    ]


def test_datetimeTime_23():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 12, 3, 27), datetime(2011, 1, 1, 12, 21, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 5),
        datetime(2011, 1, 1, 12, 10),
        datetime(2011, 1, 1, 12, 15),
        datetime(2011, 1, 1, 12, 20),
    ]


def test_datetimeTime_24():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 12, 8, 27), datetime(2011, 1, 1, 13, 4, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 15),
        datetime(2011, 1, 1, 12, 30),
        datetime(2011, 1, 1, 12, 45),
        datetime(2011, 1, 1, 13, 0),
    ]


def test_datetimeTime_25():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 12, 28, 27), datetime(2011, 1, 1, 14, 4, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 12, 30),
        datetime(2011, 1, 1, 13, 0),
        datetime(2011, 1, 1, 13, 30),
        datetime(2011, 1, 1, 14, 0),
    ]


def test_datetimeTime_26():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 12, 28, 27), datetime(2011, 1, 1, 16, 34, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 13, 0),
        datetime(2011, 1, 1, 14, 0),
        datetime(2011, 1, 1, 15, 0),
        datetime(2011, 1, 1, 16, 0),
    ]


def test_datetimeTime_27():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 14, 28, 27), datetime(2011, 1, 2, 1, 34, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 15, 0),
        datetime(2011, 1, 1, 18, 0),
        datetime(2011, 1, 1, 21, 0),
        datetime(2011, 1, 2, 0, 0),
    ]


def test_datetimeTime_28():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 16, 28, 27), datetime(2011, 1, 2, 14, 34, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 18, 0),
        datetime(2011, 1, 2, 0, 0),
        datetime(2011, 1, 2, 6, 0),
        datetime(2011, 1, 2, 12, 0),
    ]


def test_datetimeTime_29():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 16, 28, 27), datetime(2011, 1, 3, 21, 34, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 2, 0, 0),
        datetime(2011, 1, 2, 12, 0),
        datetime(2011, 1, 3, 0, 0),
        datetime(2011, 1, 3, 12, 0),
    ]


def test_datetimeTime_30():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 16, 28, 27), datetime(2011, 1, 5, 21, 34, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 2, 0, 0),
        datetime(2011, 1, 3, 0, 0),
        datetime(2011, 1, 4, 0, 0),
        datetime(2011, 1, 5, 0, 0),
    ]


def test_datetimeTime_31():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 2, 16, 28, 27), datetime(2011, 1, 9, 21, 34, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 3, 0, 0),
        datetime(2011, 1, 5, 0, 0),
        datetime(2011, 1, 7, 0, 0),
        datetime(2011, 1, 9, 0, 0),
    ]


def test_datetimeTime_32():
    x = d3.scale_time().domain(
        [datetime(2011, 1, 1, 16, 28, 27), datetime(2011, 1, 23, 21, 34, 12)]
    )
    assert x.ticks(4) == [
        datetime(2011, 1, 2, 0, 0),
        datetime(2011, 1, 9, 0, 0),
        datetime(2011, 1, 16, 0, 0),
        datetime(2011, 1, 23, 0, 0),
    ]


def test_datetimeTime_33():
    x = d3.scale_time().domain([datetime(2011, 1, 18), datetime(2011, 5, 2)])
    assert x.ticks(4) == [
        datetime(2011, 2, 1, 0, 0),
        datetime(2011, 3, 1, 0, 0),
        datetime(2011, 4, 1, 0, 0),
        datetime(2011, 5, 1, 0, 0),
    ]


def test_datetimeTime_34():
    x = d3.scale_time().domain([datetime(2010, 12, 18), datetime(2011, 11, 2)])
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 0, 0),
        datetime(2011, 4, 1, 0, 0),
        datetime(2011, 7, 1, 0, 0),
        datetime(2011, 10, 1, 0, 0),
    ]


def test_datetimeTime_35():
    x = d3.scale_time().domain([datetime(2010, 12, 18), datetime(2014, 3, 2)])
    assert x.ticks(4) == [
        datetime(2011, 1, 1, 0, 0),
        datetime(2012, 1, 1, 0, 0),
        datetime(2013, 1, 1, 0, 0),
        datetime(2014, 1, 1, 0, 0),
    ]


def test_datetimeTime_36():
    with pytest.raises(ValueError):
        x = d3.scale_time().domain([datetime(1, 12, 18), datetime(2014, 3, 2)])
        assert x.ticks(6) == [
            datetime(500, 1, 1, 0, 0),
            datetime(1000, 1, 1, 0, 0),
            datetime(1500, 1, 1, 0, 0),
            datetime(2000, 1, 1, 0, 0),
        ]


def test_datetimeTime_37():
    x = d3.scale_time().domain([datetime(2014, 3, 2), datetime(2014, 3, 2)])
    assert x.ticks(6) == [datetime(2014, 3, 2)]


def test_datetimeTime_38():
    f = d3.scale_time().tick_format()
    assert f(datetime(2011, 1, 1)) == "2011"
    assert f(datetime(2012, 1, 1)) == "2012"
    assert f(datetime(2013, 1, 1)) == "2013"


def test_datetimeTime_39():
    f = d3.scale_time().tick_format()
    assert f(datetime(2011, 2, 1)) == "February"
    assert f(datetime(2011, 3, 1)) == "March"
    assert f(datetime(2011, 4, 1)) == "April"


def test_datetimeTime_40():
    f = d3.scale_time().tick_format()
    assert f(datetime(2011, 2, 6)) == "Feb 06"
    assert f(datetime(2011, 2, 13)) == "Feb 13"
    assert f(datetime(2011, 2, 20)) == "Feb 20"


def test_datetimeTime_41():
    f = d3.scale_time().tick_format()
    assert f(datetime(2011, 2, 2)) == "Wed 02"
    assert f(datetime(2011, 2, 3)) == "Thu 03"
    assert f(datetime(2011, 2, 4)) == "Fri 04"


def test_datetimeTime_42():
    f = d3.scale_time().tick_format()
    assert f(datetime(2011, 2, 2, 11)) == "11 AM"
    assert f(datetime(2011, 2, 2, 12)) == "12 PM"
    assert f(datetime(2011, 2, 2, 13)) == "01 PM"


def test_datetimeTime_43():
    f = d3.scale_time().tick_format()
    assert f(datetime(2011, 2, 2, 11, 59)) == "11:59"
    assert f(datetime(2011, 2, 2, 12, 1)) == "12:01"
    assert f(datetime(2011, 2, 2, 12, 2)) == "12:02"


def test_datetimeTime_44():
    f = d3.scale_time().tick_format()
    assert f(datetime(2011, 2, 2, 12, 1, 9)) == ":09"
    assert f(datetime(2011, 2, 2, 12, 1, 10)) == ":10"
    assert f(datetime(2011, 2, 2, 12, 1, 11)) == ":11"


def test_datetimeTime_45():
    f = d3.scale_time().tick_format("%c")
    assert f(datetime(2011, 2, 2, 12)) == "Wed Feb  2 12:00:00 2011"
