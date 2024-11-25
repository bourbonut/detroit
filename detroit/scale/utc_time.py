from ..time import (
    utcDay,
    utcHour,
    utcMinute,
    utcMonth,
    utcSecond,
    utcTickInterval,
    utcTicks,
    utcWeek,
    utcYear,
)
from ..time_format import utcFormat
from .init import init_range
from .time import calendar


def utc_time():
    return init_range(
        calendar(
            utcTicks,
            utcTickInterval,
            utcYear,
            utcMonth,
            utcWeek,
            utcDay,
            utcHour,
            utcMinute,
            utcSecond,
            utcFormat,
        ).domain([datetime.datetime(2000, 1, 1), datetime.datetime(2000, 1, 2)])
    )
