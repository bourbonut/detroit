import detroit as d3
from datetime import datetime


def test_time_format_locale():
    f = d3.time_format_locale("en_US.UTF-8")("%c")
    assert f(datetime(2000, 1, 1, 1, 1)) == "Sat 01 Jan 2000 01:01:00 AM "
