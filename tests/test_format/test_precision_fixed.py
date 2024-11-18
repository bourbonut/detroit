import detroit as d3

def test_precisionFixed_1():
    assert d3.precision_fixed(8.9) == 0
    assert d3.precision_fixed(1.1) == 0
    assert d3.precision_fixed(0.89) == 1
    assert d3.precision_fixed(0.11) == 1
    assert d3.precision_fixed(0.089) == 2
    assert d3.precision_fixed(0.011) == 2
