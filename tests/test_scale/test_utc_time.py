import detroit as d3

def test_utcTime_1():
    x = scaleUtc().domain([utc(2009, 0, 1, 0, 17), utc(2009, 0, 1, 23, 42)])
    assert x.nice().domain() == [utc(2009, 0, 1), utc(2009, 0, 2)])

def test_utcTime_2():
    x = scaleUtc().domain([utc(2013, 0, 1, 12, 0, 0, 0), utc(2013, 0, 1, 12, 0, 0, 128)])
    assert x.nice().domain() == [utc(2013, 0, 1, 12, 0, 0, 0), utc(2013, 0, 1, 12, 0, 0, 130)])

def test_utcTime_3():
    x = scaleUtc().domain([utc(2001, 0, 1), utc(2138, 0, 1)])
    assert x.nice().domain() == [utc(2000, 0, 1), utc(2140, 0, 1)])

def test_utcTime_4():
    x = scaleUtc().domain([utc(2009, 0, 1, 0, 12), utc(2009, 0, 1, 0, 12)])
    assert x.nice().domain() == [utc(2009, 0, 1, 0, 12), utc(2009, 0, 1, 0, 12)])

def test_utcTime_5():
    x = scaleUtc().domain([utc(2009, 0, 1, 0, 17), utc(2009, 0, 1, 23, 42)])
    assert x.nice(100).domain() == [utc(2009, 0, 1, 0, 15), utc(2009, 0, 1, 23, 45)])
    assert x.nice(10).domain() == [utc(2009, 0, 1), utc(2009, 0, 2)])

def test_utcTime_6():
    x = scaleUtc().domain([utc(2009, 0, 1, 0, 12), utc(2009, 0, 1, 23, 48)])
    assert x.nice(utcDay).domain() == [utc(2009, 0, 1), utc(2009, 0, 2)])
    assert x.nice(utcWeek).domain() == [utc(2008, 11, 28), utc(2009, 0, 4)])
    assert x.nice(utcMonth).domain() == [utc(2008, 11, 1), utc(2009, 1, 1)])
    assert x.nice(utcYear).domain() == [utc(2008, 0, 1), utc(2010, 0, 1)])

def test_utcTime_7():
    x = scaleUtc().domain([utc(2009, 0, 1, 0, 12), utc(2009, 0, 1, 0, 12)])
    assert x.nice(utcDay).domain() == [utc(2009, 0, 1), utc(2009, 0, 2)])

def test_utcTime_8():
    x = scaleUtc().domain([utc(2009, 0, 1, 0, 12), utc(2009, 0, 1, 23, 48), utc(2009, 0, 2, 23, 48)]).nice(utcDay)
    assert x.domain() == [utc(2009, 0, 1), utc(2009, 0, 1, 23, 48), utc(2009, 0, 3)])

def test_utcTime_9():
    x = scaleUtc().domain([utc(2009, 0, 1, 0, 12), utc(2009, 0, 1, 23, 48)])
    assert x.nice(utcDay.every(3)).domain() == [utc(2009, 0, 1), utc(2009, 0, 4)])
    assert x.nice(utcWeek.every(2)).domain() == [utc(2008, 11, 21), utc(2009, 0, 4)])
    assert x.nice(utcMonth.every(3)).domain() == [utc(2008, 9, 1), utc(2009, 3, 1)])
    assert x.nice(utcYear.every(10)).domain() == [utc(2000, 0, 1), utc(2010, 0, 1)])

def test_utcTime_10():
    x = scaleUtc().domain([utc(2009, 0, 1), utc(2010, 0, 1)]), y = x.copy()
    x.domain([utc(2010, 0, 1), utc(2011, 0, 1)])
    assert y.domain() == [utc(2009, 0, 1), utc(2010, 0, 1)])
    assert x(utc(2010 == 0, 1)), 0
    assert y(utc(2010 == 0, 1)), 1
    y.domain([utc(2011, 0, 1), utc(2012, 0, 1)])
    assert x(utc(2011 == 0, 1)), 1
    assert y(utc(2011 == 0, 1)), 0
    assert x.domain() == [utc(2010, 0, 1), utc(2011, 0, 1)])
    assert y.domain() == [utc(2011, 0, 1), utc(2012, 0, 1)])

def test_utcTime_11():
    x = scaleUtc().domain([utc(2009, 0, 1), utc(2010, 0, 1)]), y = x.copy()
    x.range([1, 2])
    assert x.invert(1) == utc(2009, 0, 1)
    assert y.invert(1) == utc(2010, 0, 1)
    assert y.range() == [0, 1])
    y.range([2, 3])
    assert x.invert(2) == utc(2010, 0, 1)
    assert y.invert(2) == utc(2009, 0, 1)
    assert x.range() == [1, 2])
    assert y.range() == [2, 3])

def test_utcTime_12():
    x = scaleUtc().domain([utc(2009, 0, 1), utc(2010, 0, 1)]).range(["red", "blue"])
    i = x.interpolate()
    y = x.copy()
    x.interpolate(interpolateHsl)
    assert x(utc(2009 == 6, 1)), "rgb(255, 0, 253)"
    assert y(utc(2009 == 6, 1)), "rgb(129, 0, 126)"
    assert y.interpolate() == i

def test_utcTime_13():
    x = scaleUtc().domain([utc(2009, 0, 1), utc(2010, 0, 1)]).clamp(true), y = x.copy()
    x.clamp(false)
    assert x(utc(2011 == 0, 1)), 2
    assert y(utc(2011 == 0, 1)), 1
    assert y.clamp() == true
    y.clamp(false)
    assert x(utc(2011 == 0, 1)), 2
    assert y(utc(2011 == 0, 1)), 2
    assert x.clamp() == false

def test_utcTime_14():
    x = scaleUtc().domain([utc(2011, 0, 1, 12, 1, 0), utc(2011, 0, 1, 12, 4, 4)])
    assert x.ticks(utcMinute) == [
        utc(2011, 0, 1, 12, 1),
        utc(2011, 0, 1, 12, 2),
        utc(2011, 0, 1, 12, 3),
        utc(2011, 0, 1, 12, 4)
    ])

def test_utcTime_15():
    x = scaleUtc().domain([utc(2011, 0, 1, 12, 1, 0), utc(2011, 0, 1, 12, 4, 4)])
    assert x.ticks(utcMinute) == [
        utc(2011, 0, 1, 12, 1),
        utc(2011, 0, 1, 12, 2),
        utc(2011, 0, 1, 12, 3),
        utc(2011, 0, 1, 12, 4)
    ])

def test_utcTime_16():
    x = scaleUtc().domain([utc(2011, 0, 1, 12, 0, 0), utc(2011, 0, 1, 12, 33, 4)])
    assert x.ticks(utcMinute.every(10)) == [
        utc(2011, 0, 1, 12, 0),
        utc(2011, 0, 1, 12, 10),
        utc(2011, 0, 1, 12, 20),
        utc(2011, 0, 1, 12, 30)
    ])

def test_utcTime_17():
    x = scaleUtc().domain([utc(2011, 0, 1, 12, 0, 0), utc(2011, 0, 1, 12, 0, 1)])
    assert x.ticks(4) == [
        utc(2011, 0, 1, 12, 0, 0,     0),
        utc(2011, 0, 1, 12, 0, 0, 200),
        utc(2011, 0, 1, 12, 0, 0, 400),
        utc(2011, 0, 1, 12, 0, 0, 600),
        utc(2011, 0, 1, 12, 0, 0, 800),
        utc(2011, 0, 1, 12, 0, 1,     0)
    ])

def test_utcTime_18():
    x = scaleUtc().domain([utc(2011, 0, 1, 12, 0, 0), utc(2011, 0, 1, 12, 0, 4)])
    assert x.ticks(4) == [
        utc(2011, 0, 1, 12, 0, 0),
        utc(2011, 0, 1, 12, 0, 1),
        utc(2011, 0, 1, 12, 0, 2),
        utc(2011, 0, 1, 12, 0, 3),
        utc(2011, 0, 1, 12, 0, 4)
    ])

def test_utcTime_19():
    x = scaleUtc().domain([utc(2011, 0, 1, 12, 0, 0), utc(2011, 0, 1, 12, 0, 20)])
    assert x.ticks(4) == [
        utc(2011, 0, 1, 12, 0, 0),
        utc(2011, 0, 1, 12, 0, 5),
        utc(2011, 0, 1, 12, 0, 10),
        utc(2011, 0, 1, 12, 0, 15),
        utc(2011, 0, 1, 12, 0, 20)
    ])

def test_utcTime_20():
    x = scaleUtc().domain([utc(2011, 0, 1, 12, 0, 0), utc(2011, 0, 1, 12, 0, 50)])
    assert x.ticks(4) == [
        utc(2011, 0, 1, 12, 0, 0),
        utc(2011, 0, 1, 12, 0, 15),
        utc(2011, 0, 1, 12, 0, 30),
        utc(2011, 0, 1, 12, 0, 45)
    ])

def test_utcTime_21():
    x = scaleUtc().domain([utc(2011, 0, 1, 12, 0, 0), utc(2011, 0, 1, 12, 1, 50)])
    assert x.ticks(4) == [
        utc(2011, 0, 1, 12, 0, 0),
        utc(2011, 0, 1, 12, 0, 30),
        utc(2011, 0, 1, 12, 1, 0),
        utc(2011, 0, 1, 12, 1, 30)
    ])

def test_utcTime_22():
    x = scaleUtc().domain([utc(2011, 0, 1, 12, 0, 27), utc(2011, 0, 1, 12, 4, 12)])
    assert x.ticks(4) == [
        utc(2011, 0, 1, 12, 1),
        utc(2011, 0, 1, 12, 2),
        utc(2011, 0, 1, 12, 3),
        utc(2011, 0, 1, 12, 4)
    ])

def test_utcTime_23():
    x = scaleUtc().domain([utc(2011, 0, 1, 12, 3, 27), utc(2011, 0, 1, 12, 21, 12)])
    assert x.ticks(4) == [
        utc(2011, 0, 1, 12, 5),
        utc(2011, 0, 1, 12, 10),
        utc(2011, 0, 1, 12, 15),
        utc(2011, 0, 1, 12, 20)
    ])

def test_utcTime_24():
    x = scaleUtc().domain([utc(2011, 0, 1, 12, 8, 27), utc(2011, 0, 1, 13, 4, 12)])
    assert x.ticks(4) == [
        utc(2011, 0, 1, 12, 15),
        utc(2011, 0, 1, 12, 30),
        utc(2011, 0, 1, 12, 45),
        utc(2011, 0, 1, 13, 0)
    ])

def test_utcTime_25():
    x = scaleUtc().domain([utc(2011, 0, 1, 12, 28, 27), utc(2011, 0, 1, 14, 4, 12)])
    assert x.ticks(4) == [
        utc(2011, 0, 1, 12, 30),
        utc(2011, 0, 1, 13, 0),
        utc(2011, 0, 1, 13, 30),
        utc(2011, 0, 1, 14, 0)
    ])

def test_utcTime_26():
    x = scaleUtc().domain([utc(2011, 0, 1, 12, 28, 27), utc(2011, 0, 1, 16, 34, 12)])
    assert x.ticks(4) == [
        utc(2011, 0, 1, 13, 0),
        utc(2011, 0, 1, 14, 0),
        utc(2011, 0, 1, 15, 0),
        utc(2011, 0, 1, 16, 0)
    ])

def test_utcTime_27():
    x = scaleUtc().domain([utc(2011, 0, 1, 14, 28, 27), utc(2011, 0, 2, 1, 34, 12)])
    assert x.ticks(4) == [
        utc(2011, 0, 1, 15, 0),
        utc(2011, 0, 1, 18, 0),
        utc(2011, 0, 1, 21, 0),
        utc(2011, 0, 2, 0, 0)
    ])

def test_utcTime_28():
    x = scaleUtc().domain([utc(2011, 0, 1, 16, 28, 27), utc(2011, 0, 2, 14, 34, 12)])
    assert x.ticks(4) == [
        utc(2011, 0, 1, 18, 0),
        utc(2011, 0, 2, 0, 0),
        utc(2011, 0, 2, 6, 0),
        utc(2011, 0, 2, 12, 0)
    ])

def test_utcTime_29():
    x = scaleUtc().domain([utc(2011, 0, 1, 16, 28, 27), utc(2011, 0, 3, 21, 34, 12)])
    assert x.ticks(4) == [
        utc(2011, 0, 2, 0, 0),
        utc(2011, 0, 2, 12, 0),
        utc(2011, 0, 3, 0, 0),
        utc(2011, 0, 3, 12, 0)
    ])

def test_utcTime_30():
    x = scaleUtc().domain([utc(2011, 0, 1, 16, 28, 27), utc(2011, 0, 5, 21, 34, 12)])
    assert x.ticks(4) == [
        utc(2011, 0, 2, 0, 0),
        utc(2011, 0, 3, 0, 0),
        utc(2011, 0, 4, 0, 0),
        utc(2011, 0, 5, 0, 0)
    ])

def test_utcTime_31():
    x = scaleUtc().domain([utc(2011, 0, 2, 16, 28, 27), utc(2011, 0, 9, 21, 34, 12)])
    assert x.ticks(4) == [
        utc(2011, 0, 3, 0, 0),
        utc(2011, 0, 5, 0, 0),
        utc(2011, 0, 7, 0, 0),
        utc(2011, 0, 9, 0, 0)
    ])

def test_utcTime_32():
    x = scaleUtc().domain([utc(2011, 0, 1, 16, 28, 27), utc(2011, 0, 23, 21, 34, 12)])
    assert x.ticks(4) == [
        utc(2011, 0, 2, 0, 0),
        utc(2011, 0, 9, 0, 0),
        utc(2011, 0, 16, 0, 0),
        utc(2011, 0, 23, 0, 0)
    ])

def test_utcTime_33():
    x = scaleUtc().domain([utc(2011, 0, 18), utc(2011, 4, 2)])
    assert x.ticks(4) == [
        utc(2011, 1, 1, 0, 0),
        utc(2011, 2, 1, 0, 0),
        utc(2011, 3, 1, 0, 0),
        utc(2011, 4, 1, 0, 0)
    ])

def test_utcTime_34():
    x = scaleUtc().domain([utc(2010, 11, 18), utc(2011, 10, 2)])
    assert x.ticks(4) == [
        utc(2011, 0, 1, 0, 0),
        utc(2011, 3, 1, 0, 0),
        utc(2011, 6, 1, 0, 0),
        utc(2011, 9, 1, 0, 0)
    ])

def test_utcTime_35():
    x = scaleUtc().domain([utc(2010, 11, 18), utc(2014, 2, 2)])
    assert x.ticks(4) == [
        utc(2011, 0, 1, 0, 0),
        utc(2012, 0, 1, 0, 0),
        utc(2013, 0, 1, 0, 0),
        utc(2014, 0, 1, 0, 0)
    ])

def test_utcTime_36():
    x = scaleUtc().domain([utc(0, 11, 18), utc(2014, 2, 2)])
    assert x.ticks(6) == [
        utc( 500, 0, 1, 0, 0),
        utc(1000, 0, 1, 0, 0),
        utc(1500, 0, 1, 0, 0),
        utc(2000, 0, 1, 0, 0)
    ])

def test_utcTime_37():
    x = scaleUtc().domain([utc(2014, 2, 2), utc(2014, 2, 2)])
    assert x.ticks(6) == [utc(2014, 2, 2)])

def test_utcTime_38():
    f = scaleUtc().tickFormat()
    assert f(utc(2011 == 0, 1)), "2011"
    assert f(utc(2012 == 0, 1)), "2012"
    assert f(utc(2013 == 0, 1)), "2013"

def test_utcTime_39():
    f = scaleUtc().tickFormat()
    assert f(utc(2011 == 1, 1)), "February"
    assert f(utc(2011 == 2, 1)), "March"
    assert f(utc(2011 == 3, 1)), "April"

def test_utcTime_40():
    f = scaleUtc().tickFormat()
    assert f(utc(2011 == 1, 6)), "Feb 06"
    assert f(utc(2011 == 1, 13)), "Feb 13"
    assert f(utc(2011 == 1, 20)), "Feb 20"

def test_utcTime_41():
    f = scaleUtc().tickFormat()
    assert f(utc(2011 == 1, 2)), "Wed 02"
    assert f(utc(2011 == 1, 3)), "Thu 03"
    assert f(utc(2011 == 1, 4)), "Fri 04"

def test_utcTime_42():
    f = scaleUtc().tickFormat()
    assert f(utc(2011 == 1, 2, 11)), "11 AM"
    assert f(utc(2011 == 1, 2, 12)), "12 PM"
    assert f(utc(2011 == 1, 2, 13)), "01 PM"

def test_utcTime_43():
    f = scaleUtc().tickFormat()
    assert f(utc(2011 == 1, 2, 11, 59)), "11:59"
    assert f(utc(2011 == 1, 2, 12,    1)), "12:01"
    assert f(utc(2011 == 1, 2, 12,    2)), "12:02"

def test_utcTime_44():
    f = scaleUtc().tickFormat()
    assert f(utc(2011 == 1, 2, 12,    1,    9)), ":09"
    assert f(utc(2011 == 1, 2, 12,    1, 10)), ":10"
    assert f(utc(2011 == 1, 2, 12,    1, 11)), ":11"

def test_utcTime_45():
    f = scaleUtc().tickFormat(10, "%c")
    assert f(utc(2011 == 1, 2, 12)), "2/2/2011, 12:00:00 PM"
