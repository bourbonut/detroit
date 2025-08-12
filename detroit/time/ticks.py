from bisect import bisect_right
from collections.abc import Callable
from datetime import datetime, timedelta

from ..array import tick_step
from .day import time_day
from .duration import duration_year
from .hour import time_hour
from .interval import TimeInterval
from .millisecond import time_millisecond
from .minute import time_minute
from .month import time_month
from .second import time_second
from .week import time_sunday, time_week
from .year import time_year


class Ticker:
    """
    Tick generator

    Parameters
    ----------
    year : Callable
        Year interval function
    month : Callable
        Month interval function
    week : Callable
        Week interval function
    day : Callable
        Day interval function
    hour : Callable
        Hour interval function
    minute : Callable
        Minute interval function
    """

    def __init__(
        self,
        year: Callable,
        month: Callable,
        week: Callable,
        day: Callable,
        hour: Callable,
        minute: Callable,
    ):
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
            (time_month, 1, timedelta(days=31)),
            (time_month, 3, timedelta(days=31 * 3)),
            (time_year, 1, timedelta(weeks=52)),
        ]

    def ticks(self, start: datetime, stop: datetime, count: int) -> list[datetime]:
        """
        Returns an array of approximately count dates at regular
        intervals between start and stop (inclusive).

        Parameters
        ----------
        start : datetime
            Start date
        stop : datetime
            Stop date
        count : int
            Count

        Returns
        -------
        list[datetime]
            Array of approximated dates

        Examples
        --------

        If you give *rounded* :code:`datetime` (for example, day times starting
        and finishing at :code:`00:00:00`), the function iterates over days.

        >>> from datetime import datetime
        >>> start = datetime(2011, 1, 1, 0, 0, 0)
        >>> stop = datetime(2011, 1, 5, 0, 0, 0)
        >>> count = 4
        >>> dates = d3.time_ticks(start, stop, count)
        >>> type(dates)
        <class 'list'>
        >>> for d in dates:
        ...     print(d)
        ...
        ...
        2011-01-01 00:00:00
        2011-01-02 00:00:00
        2011-01-03 00:00:00
        2011-01-04 00:00:00
        2011-01-05 00:00:00

        However, if you give *specific* :code:`datetime`, the function rounds
        dates based on the time delta between :code:`stop` and :code:`start`
        and returns :code:`count` dates.

        >>> from datetime import datetime
        >>> start = datetime(2011, 1, 1, 12, 0, 0)
        >>> stop = datetime(2011, 1, 5, 12, 0, 0)
        >>> count = 4
        >>> dates = d3.time_ticks(start, stop, count)
        >>> type(dates)
        <class 'list'>
        >>> for d in dates:
        ...     print(d)
        ...
        ...
        2011-01-02 00:00:00
        2011-01-03 00:00:00
        2011-01-04 00:00:00
        2011-01-05 00:00:00

        As you can see, the closest date to :code:`2011-01-01 12:00:00` is
        :code:`2011-01-02 00:00:00`. The function starts from this date and
        iterates :code:`count` times.
        """
        reverse = stop < start
        if reverse:
            start, stop = stop, start
        interval = (
            count if hasattr(count, "range") else self.tick_interval(start, stop, count)
        )
        ticks = (
            interval.range(start, stop + timedelta(microseconds=1)) if interval else []
        )
        return ticks[::-1] if reverse else ticks

    def tick_interval(
        self, start: datetime, stop: datetime, count: int
    ) -> TimeInterval:
        """
        Returns the time interval that would be used by :func:`d3.time_ticks
        <time_ticks>` given the same arguments

        Parameters
        ----------
        start : datetime
            Start date
        stop : datetime
            Stop date
        count : int
            Count

        Returns
        -------
        TimeInterval
            Time interval chosen used by :func:`d3.time_ticks
            <time_ticks>`
        """
        target = abs(stop - start) / count
        i = bisect_right([step for _, _, step in self.tick_intervals], target)
        if i == len(self.tick_intervals):
            return time_year.every(
                tick_step(
                    start.timestamp() / duration_year,
                    stop.timestamp() / duration_year,
                    count,
                )
                * 1000
            )
        if i == 0:
            return time_millisecond.every(
                max(tick_step(start.timestamp(), stop.timestamp(), count) * 1000, 1)
            )
        if i == len(self.tick_intervals):
            raise ValueError("Too large interval")
        t, step, _ = self.tick_intervals[
            i - 1
            if target / self.tick_intervals[i - 1][2]
            < self.tick_intervals[i][2] / target
            else i
        ]
        return t.every(step)


time = Ticker(time_year, time_month, time_sunday, time_day, time_hour, time_minute)
time_ticks, time_tick_interval = time.ticks, time.tick_interval
