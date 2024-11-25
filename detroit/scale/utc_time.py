from ..time import (
    utcYear,
    utcMonth,
    utcWeek,
    utcDay,
    utcHour,
    utcMinute,
    utcSecond,
    utcTicks,
    utcTickInterval,
)
from ..time_format import utcFormat
from .time import calendar
from .init import init_range


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
