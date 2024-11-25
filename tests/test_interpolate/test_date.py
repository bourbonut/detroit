from datetime import datetime

import detroit as d3


def test_date_1():
    i = d3.interpolate_date(datetime(2000, 1, 1), datetime(2000, 1, 2))
    assert isinstance(i(0.0), datetime)
    assert isinstance(i(0.5), datetime)
    assert isinstance(i(1.0), datetime)
    assert i(0.2) == datetime(2000, 1, 1, 4, 48)
    assert i(0.4) == datetime(2000, 1, 1, 9, 36)
