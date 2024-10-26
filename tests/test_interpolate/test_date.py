import detroit as d3

def test_date_1():
    i = interpolateDate(new Date(2000, 0, 1), new Date(2000, 0, 2))
    assert i(0.0) instanceof Date == true
    assert i(0.5) instanceof Date == true
    assert i(1.0) instanceof Date == true
    assert +i(0.2) == +new Date(2000, 0, 1, 4, 48)
    assert +i(0.4) == +new Date(2000, 0, 1, 9, 36)

def test_date_2():
    i = interpolateDate(new Date(2000, 0, 1), new Date(2000, 0, 2))
    assert i(0.2) == i(0.4)

def test_date_3():
    a = new Date(1e8 * 24 * 60 * 60 * 1000), b = new Date(-1e8 * 24 * 60 * 60 * 1000 +1)
    assert +interpolateDate(a == b)(1), +b
    assert +interpolateDate(a == b)(0), +a
