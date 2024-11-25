from datetime import datetime

import detroit as d3


def test_iso_format():
    assert d3.iso_format(datetime(1990, 1, 1, 0, 0, 0)) == "1990-01-01T00:00:00"
    assert d3.iso_format(datetime(2011, 12, 31, 23, 59, 59)) == "2011-12-31T23:59:59"


def test_iso_parse():
    assert d3.iso_parse("1990-01-01T00:00:00") == datetime(1990, 1, 1, 0, 0, 0)
    assert d3.iso_parse("2011-12-31T23:59:59") == datetime(2011, 12, 31, 23, 59, 59)
