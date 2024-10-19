from .continuous import Transformer, identity, copy
from .init import init_range
from ..time import (
    time_ticks,
    time_tick_interval,
    time_year,
    time_month,
    time_week,
    time_month,
    time_hour,
    time_minute,
    time_second,
)
from ..time_format import time_format
from datetime import datetime


def number(t):
    return (
        t.timestamp()
        if isinstance(t, datetime)
        else datetime.fromtimestamp(t).timestamp()
    )


class Calendar:
    def __init__(
        self, ticks, tick_interval, year, month, week, day, hour, minute, second
    ):
        self._scale = Transformer(identity, identity)
        self._invert = scale.invert
        self._domain = scale.domain

        self._ticks = ticks
        self._tick_interval = tick_interval
        self._year = year
        self._month = month
        self._week = week
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second
        self._format = format

        self._format_millisecond = time_format(".%L")
        self._format_second = time_format(":%S")
        self._format_minute = time_format("%I:%M")
        self._format_hour = time_format("%I %p")
        self._format_day = time_format("%a %d")
        self._format_week = time_format("%b %d")
        self._format_month = time_format("%B")
        self._format_year = time_format("%Y")

    def tick_format(date):
        return (
            self._format_millisecond
            if self.second(date) < date
            else self._format_second
            if self.minute(date) < date
            else self._format_minute
            if self.hour(date) < date
            else self._format_hour
            if self.day(date) < date
            else self._format_week
            if self.month(date) < date
            else self._format_month
            if self.year(date) < date
            else self._format_year
        )(date)

    def invert(self, y):
        return datetime.datetime.fromtimestamp(self._invert(y))

    def domain(self, array):
        return (
            self._domain([number(x) for x in array])
            if array is not None
            else [datetime(x) for x in self._domain()]
        )

    def ticks_func(self, interval):
        d = self._domain()
        return self._ticks(d[0], d[-1], interval if interval is not None else 10)

    def tick_format_func(self, count, specifier=None):
        return specifier is None and self._tick_format or self._format(specifier)

    def nice(self, interval=None):
        d = self._domain()
        if not interval or not hasattr(interval, "range"):
            interval = self._tick_interval(
                d[0], d[-1], interval if interval is not None else 10
            )
        return interval and self._domain(self.nice(d, interval)) or self.scale

    def copy(self):
        return copy(
            self._scale,
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
                self._format,
            ),
        )


def time(*args):
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
    ).domain([datetime(2000, 0, 1), datetime(2000, 0, 2)])
    return init_range(calendar, *args)
