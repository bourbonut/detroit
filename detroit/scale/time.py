from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import TypeVar, overload

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

T = TypeVar("T")


def number(t):
    return (
        t.timestamp()
        if isinstance(t, datetime)
        else datetime.fromtimestamp(t).timestamp()
    )


class Calendar(Transformer):
    """
    Time scales are a variant of linear scales that have a temporal domain:
    domain values are coerced to dates rather than numbers, and invert
    likewise returns a date. Time scales implement ticks based on calendar
    intervals, taking the pain out of generating axes for temporal domains.

    Parameters
    ----------
    ticks : Callable
        Ticks function
    tick_interval : Callable
        Tick interval function
    year : Callable
        Year time function
    month : Callable
        Month time function
    week : Callable
        Week time function
    day : Callable
        Day time function
    hour : Callable
        Hour time function
    minute : Callable
        Minute time function
    second : Callable
        Second time function
    """

    def __init__(
        self,
        ticks: Callable,
        tick_interval: Callable,
        year: Callable,
        month: Callable,
        week: Callable,
        day: Callable,
        hour: Callable,
        minute: Callable,
        second: Callable,
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

    def invert(self, y: T) -> datetime:
        """
        Given a value from the range, returns the corresponding value
        from the domain. Inversion is useful for interaction, say to
        determine the data value corresponding to the position of the mouse.

        Parameters
        ----------
        y : T
            Input value

        Returns
        -------
        Datetime
            Corresponding value from the domain
        """
        return datetime.fromtimestamp(super().invert(y))

    def ticks(self, count: int | None = None):
        """
        Returns representative dates from the scale’s domain.

        Parameters
        ----------
        count : int | None
            Count may be specified to affect how many ticks
            are generated. If count is not specified, it
            defaults to 10.

        Returns
        -------
        list[int | float]
            The returned tick values are uniformly-spaced (mostly),
            have sensible values (such as every day at midnight),
            and are guaranteed to be within the extent of the domain.
            Ticks are often used to display reference lines, or tick
            marks, in conjunction with the visualized data.
        """
        d = self.domain
        return self._ticks(d[0], d[-1], count if count is not None else 10)

    def tick_format(self, specifier: str | None = None) -> Callable[[datetime], str]:
        """
        Returns a number format function suitable for displaying
        a tick value, automatically computing the appropriate
        precision based on the fixed interval between tick values.
        The specified count should have the same value as the count
        that is used to generate the tick values.

        Parameters
        ----------
        specifier : str | None
            Specifier

        Returns
        -------
        Callable[[datetime], str]
            Tick format function
        """
        return self._tick_format if specifier is None else self._format(specifier)

    def nice(self, interval: Callable | list[datetime] | None = None) -> Calendar:
        """
        This method typically modifies the scale’s domain,
        and may only extend the bounds to the nearest round
        value.

        Parameters
        ----------
        interval : Callable | list[datetime] | None
            Argument which allows greater control over the step size used
            to extend the bounds, guaranteeing that the returned ticks
            will exactly cover the domain.

        Returns
        -------
        Calendar
            Itself
        """
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


@overload
def scale_time() -> Calendar: ...


@overload
def scale_time(range_vals: list[T]) -> Calendar: ...


@overload
def scale_time(domain: list[datetime], range_vals: list[T]) -> Calendar: ...


def scale_time(*args) -> Calendar:
    """
    Builds a new time scale with the specified domain and range,
    the default interpolator and clamping disabled

    Parameters
    ----------
    domain : list[datetime]
        Array of datetime
    range_vals : list[T]
        Array of values


    Returns
    -------
    Calendar
        Scale object

    Examples
    --------

    >>> from datetime import datetime
    >>> d3.scale_time([datetime(2000, 1, 1), datetime(2000, 1, 2)], [0, 960])
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
    if len(args) == 1:
        return init_range(calendar, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(calendar, domain=domain, range_vals=range_vals)
    return init_range(calendar)
