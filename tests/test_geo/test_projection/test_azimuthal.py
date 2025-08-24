import detroit as d3
from math import inf

def test_azimuthal_1():
    for p in [
        d3.geo_azimuthal_equal_area()([180, 0]),
        d3.geo_azimuthal_equal_area()([-180, 0]),
        d3.geo_azimuthal_equidistant()([180, 0]),
    ]:
        assert(abs(p[0]) < inf)
        assert(abs(p[1]) < inf)
