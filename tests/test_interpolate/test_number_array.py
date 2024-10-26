import detroit as d3

def test_number_array_1():
    assert d3.interpolate_number_array([2, 12], [4, 24])(0.5), [3, 18]

def test_number_array_2():
    assert d3.interpolate_number_array([2, 12, 12], [4, 24])(0.5), [3, 18]

def test_number_array_3():
    assert d3.interpolate_number_array([2, 12], [4, 24, 12])(0.5), [3, 18, 12]

def test_number_array_4():
    assert d3.interpolate_number_array(None, [2, 12])(0.5) == [2, 12]
    assert d3.interpolate_number_array([2, 12], None)(0.5) == []
    assert d3.interpolate_number_array(None, None)(0.5) == []

def test_number_array_5():
    assert isinstance(d3.interpolate_number_array([2, 12], [4, 24, 12])(0.5), list)
    assert isinstance(d3.interpolate_number_array([2, 12], [4, 24, 12])(0.5), list)
    assert isinstance(d3.interpolate_number_array([2, 12], [4, 24, 12])(0.5), list)
    assert isinstance(d3.interpolate_number_array([2, 12], [4, 24, 12])(0.5), list)

def test_number_array_6():
    assert d3.interpolate_number_array([1, 12], [255, 0])(0.5) == [128, 6]

def test_number_array_7():
    i = d3.interpolate_number_array([2e42], [355])
    assert i(0) == [2e42]
    assert i(1) == [355]
