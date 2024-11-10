import detroit as d3

def test_precisionFixed_1():
    assert precisionFixed(8.9) == 0
    assert precisionFixed(1.1) == 0
    assert precisionFixed(0.89) == 1
    assert precisionFixed(0.11) == 1
    assert precisionFixed(0.089) == 2
    assert precisionFixed(0.011) == 2
