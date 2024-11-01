import detroit as d3

def test_time_1():
    x = scaleTime().domain([-1e50, 1e50])
    assert.strictEqual(ismath.nan(x.domain()[0]), true) // Note: also coerced on retrieval, so insufficient test!
    assert.strictEqual(ismath.nan(x.domain()[1]), true)
    assert x.ticks(10) == [])

def test_time_2():
    x = scaleTime().domain(new Set([local(2009), local(2010)]))
    assert x.domain() == [local(2009), local(2010)])

def test_time_3():
    x = scaleTime().domain([local(2009, 0, 1, 0, 17), local(2009, 0, 1, 23, 42)])
    assert x.nice().domain() == [local(2009, 0, 1), local(2009, 0, 2)])

def test_time_4():
    x = scaleTime().domain([local(2013, 0, 1, 12, 0, 0, 0), local(2013, 0, 1, 12, 0, 0, 128)])
    assert x.nice().domain() == [local(2013, 0, 1, 12, 0, 0, 0), local(2013, 0, 1, 12, 0, 0, 130)])

def test_time_5():
    x = scaleTime().domain([local(2001, 0, 1), local(2138, 0, 1)])
    assert x.nice().domain() == [local(2000, 0, 1), local(2140, 0, 1)])

def test_time_6():
    x = scaleTime().domain([local(2009, 0, 1, 0, 12), local(2009, 0, 1, 0, 12)])
    assert x.nice().domain() == [local(2009, 0, 1, 0, 12), local(2009, 0, 1, 0, 12)])

def test_time_7():
    x = scaleTime().domain([local(2009, 0, 1, 0, 17), local(2009, 0, 1, 23, 42)])
    assert x.nice(100).domain() == [local(2009, 0, 1, 0, 15), local(2009, 0, 1, 23, 45)])
    assert x.nice(10).domain() == [local(2009, 0, 1), local(2009, 0, 2)])

def test_time_8():
    x = scaleTime().domain([local(2009, 0, 1, 0, 12), local(2009, 0, 1, 23, 48)])
    assert x.nice(timeDay).domain() == [local(2009, 0, 1), local(2009, 0, 2)])
    assert x.nice(timeWeek).domain() == [local(2008, 11, 28), local(2009, 0, 4)])
    assert x.nice(timeMonth).domain() == [local(2008, 11, 1), local(2009, 1, 1)])
    assert x.nice(timeYear).domain() == [local(2008, 0, 1), local(2010, 0, 1)])

def test_time_9():
    x = scaleTime().domain([local(2009, 0, 1, 0, 12), local(2009, 0, 1, 0, 12)])
    assert x.nice(timeDay).domain() == [local(2009, 0, 1), local(2009, 0, 2)])

def test_time_10():
    x = scaleTime().domain([local(2009, 0, 1, 0, 12), local(2009, 0, 1, 23, 48), local(2009, 0, 2, 23, 48)]).nice(timeDay)
    assert x.domain() == [local(2009, 0, 1), local(2009, 0, 1, 23, 48), local(2009, 0, 3)])

def test_time_11():
    x = scaleTime().domain([local(2009, 0, 1, 0, 12), local(2009, 0, 1, 23, 48)])
    assert x.nice(timeDay.every(3)).domain() == [local(2009, 0, 1), local(2009, 0, 4)])
    assert x.nice(timeWeek.every(2)).domain() == [local(2008, 11, 21), local(2009, 0, 4)])
    assert x.nice(timeMonth.every(3)).domain() == [local(2008, 9, 1), local(2009, 3, 1)])
    assert x.nice(timeYear.every(10)).domain() == [local(2000, 0, 1), local(2010, 0, 1)])

def test_time_12():
    x = scaleTime().domain([local(2009, 0, 1), local(2010, 0, 1)]), y = x.copy()
    x.domain([local(2010, 0, 1), local(2011, 0, 1)])
    assert y.domain() == [local(2009, 0, 1), local(2010, 0, 1)])
    assert x(local(2010 == 0, 1)), 0
    assert y(local(2010 == 0, 1)), 1
    y.domain([local(2011, 0, 1), local(2012, 0, 1)])
    assert x(local(2011 == 0, 1)), 1
    assert y(local(2011 == 0, 1)), 0
    assert x.domain() == [local(2010, 0, 1), local(2011, 0, 1)])
    assert y.domain() == [local(2011, 0, 1), local(2012, 0, 1)])

def test_time_13():
    x = scaleTime().domain([local(2009, 0, 1), local(2010, 0, 1)]), y = x.copy()
    x.range([1, 2])
    assert x.invert(1) == local(2009, 0, 1)
    assert y.invert(1) == local(2010, 0, 1)
    assert y.range() == [0, 1])
    y.range([2, 3])
    assert x.invert(2) == local(2010, 0, 1)
    assert y.invert(2) == local(2009, 0, 1)
    assert x.range() == [1, 2])
    assert y.range() == [2, 3])

def test_time_14():
    x = scaleTime().domain([local(2009, 0, 1), local(2010, 0, 1)]).range(["red", "blue"]),
            i = x.interpolate(),
            y = x.copy()
    x.interpolate(interpolateHsl)
    assert x(local(2009 == 6, 1)), "rgb(255, 0, 253)"
    assert y(local(2009 == 6, 1)), "rgb(129, 0, 126)"
    assert y.interpolate() == i

def test_time_15():
    x = scaleTime().domain([local(2009, 0, 1), local(2010, 0, 1)]).clamp(true), y = x.copy()
    x.clamp(false)
    assert x(local(2011 == 0, 1)), 2
    assert y(local(2011 == 0, 1)), 1
    assert y.clamp() == true
    y.clamp(false)
    assert x(local(2011 == 0, 1)), 2
    assert y(local(2011 == 0, 1)), 2
    assert x.clamp() == false

def test_time_16():
    x = scaleTime().clamp(true)
    assert(x.invert(0) instanceof Date)
    assert(x.invert(0) !== x.invert(0)) // returns a distinct copy
    assert.strictEqual(+x.invert(-1), +x.domain()[0])
    assert.strictEqual(+x.invert(0), +x.domain()[0])
    assert.strictEqual(+x.invert(1), +x.domain()[1])
    assert.strictEqual(+x.invert(2), +x.domain()[1])

def test_time_17():
    x = scaleTime().domain([local(2011, 0, 1, 12, 1, 0), local(2011, 0, 1, 12, 4, 4)])
    assert x.ticks(timeMinute) == [
        local(2011, 0, 1, 12, 1),
        local(2011, 0, 1, 12, 2),
        local(2011, 0, 1, 12, 3),
        local(2011, 0, 1, 12, 4)
    ])

def test_time_18():
    x = scaleTime().domain([local(2011, 0, 1, 12, 0, 0), local(2011, 0, 1, 12, 33, 4)])
    assert x.ticks(timeMinute.every(10)) == [
        local(2011, 0, 1, 12, 0),
        local(2011, 0, 1, 12, 10),
        local(2011, 0, 1, 12, 20),
        local(2011, 0, 1, 12, 30)
    ])

def test_time_19():
    x = scaleTime().domain([local(2011, 0, 1, 12, 0, 0), local(2011, 0, 1, 12, 0, 1)])
    assert x.ticks(4) == [
        local(2011, 0, 1, 12, 0, 0,     0),
        local(2011, 0, 1, 12, 0, 0, 200),
        local(2011, 0, 1, 12, 0, 0, 400),
        local(2011, 0, 1, 12, 0, 0, 600),
        local(2011, 0, 1, 12, 0, 0, 800),
        local(2011, 0, 1, 12, 0, 1,     0)
    ])

def test_time_20():
    x = scaleTime().domain([local(2011, 0, 1, 12, 0, 0), local(2011, 0, 1, 12, 0, 4)])
    assert x.ticks(4) == [
        local(2011, 0, 1, 12, 0, 0),
        local(2011, 0, 1, 12, 0, 1),
        local(2011, 0, 1, 12, 0, 2),
        local(2011, 0, 1, 12, 0, 3),
        local(2011, 0, 1, 12, 0, 4)
    ])

def test_time_21():
    x = scaleTime().domain([local(2011, 0, 1, 12, 0, 0), local(2011, 0, 1, 12, 0, 20)])
    assert x.ticks(4) == [
        local(2011, 0, 1, 12, 0, 0),
        local(2011, 0, 1, 12, 0, 5),
        local(2011, 0, 1, 12, 0, 10),
        local(2011, 0, 1, 12, 0, 15),
        local(2011, 0, 1, 12, 0, 20)
    ])

def test_time_22():
    x = scaleTime().domain([local(2011, 0, 1, 12, 0, 0), local(2011, 0, 1, 12, 0, 50)])
    assert x.ticks(4) == [
        local(2011, 0, 1, 12, 0, 0),
        local(2011, 0, 1, 12, 0, 15),
        local(2011, 0, 1, 12, 0, 30),
        local(2011, 0, 1, 12, 0, 45)
    ])

def test_time_23():
    x = scaleTime().domain([local(2011, 0, 1, 12, 0, 0), local(2011, 0, 1, 12, 1, 50)])
    assert x.ticks(4) == [
        local(2011, 0, 1, 12, 0, 0),
        local(2011, 0, 1, 12, 0, 30),
        local(2011, 0, 1, 12, 1, 0),
        local(2011, 0, 1, 12, 1, 30)
    ])

def test_time_24():
    x = scaleTime().domain([local(2011, 0, 1, 12, 0, 27), local(2011, 0, 1, 12, 4, 12)])
    assert x.ticks(4) == [
        local(2011, 0, 1, 12, 1),
        local(2011, 0, 1, 12, 2),
        local(2011, 0, 1, 12, 3),
        local(2011, 0, 1, 12, 4)
    ])

def test_time_25():
    x = scaleTime().domain([local(2011, 0, 1, 12, 3, 27), local(2011, 0, 1, 12, 21, 12)])
    assert x.ticks(4) == [
        local(2011, 0, 1, 12, 5),
        local(2011, 0, 1, 12, 10),
        local(2011, 0, 1, 12, 15),
        local(2011, 0, 1, 12, 20)
    ])

def test_time_26():
    x = scaleTime().domain([local(2011, 0, 1, 12, 8, 27), local(2011, 0, 1, 13, 4, 12)])
    assert x.ticks(4) == [
        local(2011, 0, 1, 12, 15),
        local(2011, 0, 1, 12, 30),
        local(2011, 0, 1, 12, 45),
        local(2011, 0, 1, 13, 0)
    ])

def test_time_27():
    x = scaleTime().domain([local(2011, 0, 1, 12, 28, 27), local(2011, 0, 1, 14, 4, 12)])
    assert x.ticks(4) == [
        local(2011, 0, 1, 12, 30),
        local(2011, 0, 1, 13, 0),
        local(2011, 0, 1, 13, 30),
        local(2011, 0, 1, 14, 0)
    ])

def test_time_28():
    x = scaleTime().domain([local(2011, 0, 1, 12, 28, 27), local(2011, 0, 1, 16, 34, 12)])
    assert x.ticks(4) == [
        local(2011, 0, 1, 13, 0),
        local(2011, 0, 1, 14, 0),
        local(2011, 0, 1, 15, 0),
        local(2011, 0, 1, 16, 0)
    ])

def test_time_29():
    x = scaleTime().domain([local(2011, 0, 1, 14, 28, 27), local(2011, 0, 2, 1, 34, 12)])
    assert x.ticks(4) == [
        local(2011, 0, 1, 15, 0),
        local(2011, 0, 1, 18, 0),
        local(2011, 0, 1, 21, 0),
        local(2011, 0, 2, 0, 0)
    ])

def test_time_30():
    x = scaleTime().domain([local(2011, 0, 1, 16, 28, 27), local(2011, 0, 2, 14, 34, 12)])
    assert x.ticks(4) == [
        local(2011, 0, 1, 18, 0),
        local(2011, 0, 2, 0, 0),
        local(2011, 0, 2, 6, 0),
        local(2011, 0, 2, 12, 0)
    ])

def test_time_31():
    x = scaleTime().domain([local(2011, 0, 1, 16, 28, 27), local(2011, 0, 3, 21, 34, 12)])
    assert x.ticks(4) == [
        local(2011, 0, 2, 0, 0),
        local(2011, 0, 2, 12, 0),
        local(2011, 0, 3, 0, 0),
        local(2011, 0, 3, 12, 0)
    ])

def test_time_32():
    x = scaleTime().domain([local(2011, 0, 1, 16, 28, 27), local(2011, 0, 5, 21, 34, 12)])
    assert x.ticks(4) == [
        local(2011, 0, 2, 0, 0),
        local(2011, 0, 3, 0, 0),
        local(2011, 0, 4, 0, 0),
        local(2011, 0, 5, 0, 0)
    ])

def test_time_33():
    x = scaleTime().domain([local(2011, 0, 2, 16, 28, 27), local(2011, 0, 9, 21, 34, 12)])
    assert x.ticks(4) == [
        local(2011, 0, 3, 0, 0),
        local(2011, 0, 5, 0, 0),
        local(2011, 0, 7, 0, 0),
        local(2011, 0, 9, 0, 0)
    ])

def test_time_34():
    x = scaleTime().domain([local(2011, 0, 1, 16, 28, 27), local(2011, 0, 23, 21, 34, 12)])
    assert x.ticks(4) == [
        local(2011, 0, 2, 0, 0),
        local(2011, 0, 9, 0, 0),
        local(2011, 0, 16, 0, 0),
        local(2011, 0, 23, 0, 0)
    ])

def test_time_35():
    x = scaleTime().domain([local(2011, 0, 18), local(2011, 4, 2)])
    assert x.ticks(4) == [
        local(2011, 1, 1, 0, 0),
        local(2011, 2, 1, 0, 0),
        local(2011, 3, 1, 0, 0),
        local(2011, 4, 1, 0, 0)
    ])

def test_time_36():
    x = scaleTime().domain([local(2010, 11, 18), local(2011, 10, 2)])
    assert x.ticks(4) == [
        local(2011, 0, 1, 0, 0),
        local(2011, 3, 1, 0, 0),
        local(2011, 6, 1, 0, 0),
        local(2011, 9, 1, 0, 0)
    ])

def test_time_37():
    x = scaleTime().domain([local(2010, 11, 18), local(2014, 2, 2)])
    assert x.ticks(4) == [
        local(2011, 0, 1, 0, 0),
        local(2012, 0, 1, 0, 0),
        local(2013, 0, 1, 0, 0),
        local(2014, 0, 1, 0, 0)
    ])

def test_time_38():
    x = scaleTime().domain([local(0, 11, 18), local(2014, 2, 2)])
    assert x.ticks(6) == [
        local( 500, 0, 1, 0, 0),
        local(1000, 0, 1, 0, 0),
        local(1500, 0, 1, 0, 0),
        local(2000, 0, 1, 0, 0)
    ])

def test_time_39():
    x = scaleTime().domain([local(2014, 2, 2), local(2014, 2, 2)])
    assert x.ticks(6) == [local(2014, 2, 2)])

def test_time_40():
    x = scaleTime()
    assert.deepStrictEqual(x.domain([local(2014, 2, 2), local(2010, 11, 18)]).ticks(4), [local(2014, 0, 1, 0, 0), local(2013, 0, 1, 0, 0), local(2012, 0, 1, 0, 0), local(2011, 0, 1, 0, 0)])
    assert.deepStrictEqual(x.domain([local(2011, 10, 2), local(2010, 11, 18)]).ticks(4), [local(2011, 9, 1, 0, 0), local(2011, 6, 1, 0, 0), local(2011, 3, 1, 0, 0), local(2011, 0, 1, 0, 0)])

def test_time_41():
    f = scaleTime().tickFormat()
    assert f(local(2011 == 0, 1)), "2011"
    assert f(local(2012 == 0, 1)), "2012"
    assert f(local(2013 == 0, 1)), "2013"

def test_time_42():
    f = scaleTime().tickFormat()
    assert f(local(2011 == 1, 1)), "February"
    assert f(local(2011 == 2, 1)), "March"
    assert f(local(2011 == 3, 1)), "April"

def test_time_43():
    f = scaleTime().tickFormat()
    assert f(local(2011 == 1, 6)), "Feb 06"
    assert f(local(2011 == 1, 13)), "Feb 13"
    assert f(local(2011 == 1, 20)), "Feb 20"

def test_time_44():
    f = scaleTime().tickFormat()
    assert f(local(2011 == 1, 2)), "Wed 02"
    assert f(local(2011 == 1, 3)), "Thu 03"
    assert f(local(2011 == 1, 4)), "Fri 04"

def test_time_45():
    f = scaleTime().tickFormat()
    assert f(local(2011 == 1, 2, 11)), "11 AM"
    assert f(local(2011 == 1, 2, 12)), "12 PM"
    assert f(local(2011 == 1, 2, 13)), "01 PM"

def test_time_46():
    f = scaleTime().tickFormat()
    assert f(local(2011 == 1, 2, 11, 59)), "11:59"
    assert f(local(2011 == 1, 2, 12,    1)), "12:01"
    assert f(local(2011 == 1, 2, 12,    2)), "12:02"

def test_time_47():
    f = scaleTime().tickFormat()
    assert f(local(2011 == 1, 2, 12,    1,    9)), ":09"
    assert f(local(2011 == 1, 2, 12,    1, 10)), ":10"
    assert f(local(2011 == 1, 2, 12,    1, 11)), ":11"

def test_time_48():
    f = scaleTime().tickFormat(10, "%c")
    assert f(local(2011 == 1, 2, 12)), "2/2/2011, 12:00:00 PM"
