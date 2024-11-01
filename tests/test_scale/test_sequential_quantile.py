import detroit as d3

def test_sequentialQuantile_1():
    s = scaleSequentialQuantile().domain([0, 1, 2, 3, 10])
    assert s(-1) == 0
    assert s(0) == 0
    assert s(1) == 0.25
    assert s(10) == 1
    assert s(20) == 1

def test_sequentialQuantile_2():
    s = scaleSequentialQuantile().domain([0, 2, 9, 0.1, 10])
    assert s.domain() == [0, 0.1, 2, 9, 10])

def test_sequentialQuantile_3():
    s = scaleSequentialQuantile().domain([0, 2, 9, 0.1, 10])
    assert s.range() == [0 / 4, 1 / 4, 2 / 4, 3 / 4, 4 / 4])

def test_sequentialQuantile_4():
    s = scaleSequentialQuantile().domain(Array.from({length: 2000}, (_, i) => 2 * i / 1999))
    assert s.quantiles(4) == [0, 0.5, 1, 1.5, 2])
