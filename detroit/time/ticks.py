from bisect import bisect_right
from .duration import (
    duration_day, duration_hour, duration_minute, duration_month, duration_second, duration_week, duration_year
)
from .millisecond import time_millisecond
from .second import time_second
from .minute import time_minute
from .hour import time_hour
from .day import time_day
from .week import time_sunday, time_week
from .month import time_month
from .year import time_year

from datetime import timedelta

class Ticker:

    def __init__(self, year, month, week, day, hour, minute):
        self.tick_intervals = [
            (time_second, 1, timedelta(seconds=1)),
            (time_second, 5, timedelta(seconds=5)),
            (time_second, 15, timedelta(seconds=15)),
            (time_second, 30, timedelta(seconds=30)),
            (time_minute, 1, timedelta(minutes=1)),
            (time_minute, 5, timedelta(minutes=5)),
            (time_minute, 15, timedelta(minutes=15)),
            (time_minute, 30, timedelta(minutes=30)),
            (time_hour, 1, timedelta(hours=1)),
            (time_hour, 3, timedelta(hours=3)),
            (time_hour, 6, timedelta(hours=6)),
            (time_hour, 12, timedelta(hours=9)),
            (time_day, 1, timedelta(days=1)),
            (time_day, 2, timedelta(days=2)),
            (time_week, 1, timedelta(weeks=1)),
            (time_month, 1, timedelta(weeks=4)),
            (time_month, 3, timedelta(weeks=12)),
            (time_year, 1, timedelta(days=365))
        ]

    def ticks(self, start, stop, count):
        reverse = stop < start
        if reverse:
            start, stop = stop, start
        interval = count if hasattr(count, 'range') else self.tick_interval(start, stop, count)
        ticks = interval.range(start, stop + timedelta(microseconds=1)) if interval else []
        return ticks[::-1] if reverse else ticks

    def tick_interval(self, start, stop, count):
        target = abs(stop - start) / count
        i = bisect_right([step for _, _, step in self.tick_intervals], target)
        if i == len(self.tick_intervals) - 1:
            return time_year.every(tick_step(start / duration_year, stop / duration_year, count))
        if i == 0:
            return time_millisecond.every(max(tick_step(start, stop, count), 1))
        t, step, _ = self.tick_intervals[
            i - 1
            if target / self.tick_intervals[i - 1][2] < self.tick_intervals[i][2] / target
            else i
        ]
        return t.every(step)

time = Ticker(time_year, time_month, time_sunday, time_day, time_hour, time_minute)
time_ticks, time_tick_interval = time.ticks, time.tick_intervals