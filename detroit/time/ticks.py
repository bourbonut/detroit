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

class Ticker:

    def __init__(self, year, month, week, day, hour, minute):
        self.tick_intervals = [
            (time_second, 1, duration_second),
            (time_second, 5, 5 * duration_second),
            (time_second, 15, 15 * duration_second),
            (time_second, 30, 30 * duration_second),
            (time_minute, 1, duration_minute),
            (time_minute, 5, 5 * duration_minute),
            (time_minute, 15, 15 * duration_minute),
            (time_minute, 30, 30 * duration_minute),
            (time_hour, 1, duration_hour),
            (time_hour, 3, 3 * duration_hour),
            (time_hour, 6, 6 * duration_hour),
            (time_hour, 12, 12 * duration_hour),
            (time_day, 1, duration_day),
            (time_day, 2, 2 * duration_day),
            (time_week, 1, duration_week),
            (time_month, 1, duration_month),
            (time_month, 3, 3 * duration_month),
            (time_year, 1, duration_year)
        ]

    def ticks(self, start, stop, count):
        reverse = stop < start
        if reverse:
            start, stop = stop, start
        interval = count if hasattr(count, 'range') else self.tick_interval(start, stop, count)
        ticks = interval.range(start, stop + 1) if interval else []
        return ticks[::-1] if reverse else ticks

    def tick_interval(self, start, stop, count):
        target = abs(stop - start) / count
        i = bisect_right([step for _, _, step in self.tick_intervals], target)
        if i == len(self.tick_intervals):
            return year.every(tick_step(start / duration_year, stop / duration_year, count))
        if i == 0:
            return millisecond.every(max(tick_step(start, stop, count), 1))
        t, step = self.tick_intervals[
            i - 1
            if target / self.tick_intervals[i - 1][2] < self.tick_intervals[i][2] / target
            else i
        ]
        return t.every(step)

time = Ticker(time_year, time_month, time_sunday, time_day, time_hour, time_minute)
time_ticks, time_tick_interval = time.ticks, time.tick_intervals
