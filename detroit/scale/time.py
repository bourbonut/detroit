from datetime import datetime

from ..time import (
    time_day,
    time_hour,
    time_minute,
    time_month,
    time_second,
    time_tick_interval,
    time_ticks,
    time_week,
    time_year,
)
from ..time_format import time_format
from .continuous import Transformer, copy, identity
from .init import init_range
from .nice import nice


def number(t):
    return (
        t.timestamp()
        if isinstance(t, datetime)
        else datetime.fromtimestamp(t).timestamp()
    )


class Calendar(Transformer):
    def __init__(
        self, ticks, tick_interval, year, month, week, day, hour, minute, second
    ):
        super().__init__(identity, identity)

        self._ticks = ticks
        self._tick_interval = tick_interval
        self._year = year
        self._month = month
        self._week = week
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second
        self._format = time_format

        self._format_millisecond = time_format(".%L")
        self._format_second = time_format(":%S")
        self._format_minute = time_format("%I:%M")
        self._format_hour = time_format("%I %p")
        self._format_day = time_format("%a %d")
        self._format_week = time_format("%b %d")
        self._format_month = time_format("%B")
        self._format_year = time_format("%Y")

    def _tick_format(self, date):
        if self._second(date) < date:
            return self._format_millisecond(date)
        elif self._minute(date) < date:
            return self._format_second(date)
        elif self._hour(date) < date:
            return self._format_minute(date)
        elif self._day(date) < date:
            return self._format_hour(date)
        elif self._month(date) < date:
            if self._week(date) < date:
                return self._format_day(date)
            else:
                return self._format_week(date)
        elif self._year(date) < date:
            return self._format_month(date)
        else:
            return self._format_year(date)

    def invert(self, y):
        return datetime.fromtimestamp(super().invert(y))

    def ticks(self, interval):
        d = self.domain
        return self._ticks(d[0], d[-1], interval if interval is not None else 10)

    def tick_format(self, specifier=None):
        return self._tick_format if specifier is None else self._format(specifier)

    def nice(self, interval=None):
        d = self.domain
        if not interval or not hasattr(interval, "range"):
            interval = self._tick_interval(
                d[0], d[-1], interval if interval is not None else 10
            )
        return self.set_domain(nice(d, interval)) if interval else self

    def copy(self):
        return copy(
            self,
            Calendar(
                self._ticks,
                self._tick_interval,
                self._year,
                self._month,
                self._week,
                self._day,
                self._hour,
                self._minute,
                self._second,
            ),
        )


def scale_time(*args) -> Calendar:
    """
    Builds a new time scale with the specified domain and range,
    the default interpolator and clamping disabled

    Returns
    -------
    Calendar
        Scale object
    """
    calendar = Calendar(
        time_ticks,
        time_tick_interval,
        time_year,
        time_month,
        time_week,
        time_day,
        time_hour,
        time_minute,
        time_second,
    ).set_domain([datetime(2000, 1, 1), datetime(2000, 1, 2)])
    return init_range(calendar, *args)
