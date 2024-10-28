import detroit as d3

def test_cubehelix_1():
    c = cubehelix("steelblue")
    assert(c instanceof cubehelix)
    assert(c instanceof color)
