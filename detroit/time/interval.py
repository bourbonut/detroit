import math
from collections.abc import Callable
from datetime import datetime, timedelta
from typing import TypeVar

TTimeInterval = TypeVar("TimeInterval", bound="TimeInterval")


class TimeInterval:
    def __call__(self, date: datetime | None = None) -> datetime:
        """
        Applies a *floor* operation on the input. If the input is :code:`None`,
        the input is replaced by the current date.

        Parameters
        ----------
        date : datetime | None
            Date

        Returns
        -------
        datetime
            Date

        Examples
        --------

        >>> from datetime import datetime
        >>> d3.time_day(datetime(2010, 1, 1, 12, 0))
        datetime.datetime(2010, 1, 1, 0, 0)
        """
        date = datetime.now() if date is None else date
        return self.floor(date)

    def interval(self, date: datetime | None = None) -> datetime:
        """
        Same as :code:`__call__`

        Parameters
        ----------
        date : datetime | None
            Date

        Returns
        -------
        datetime
            Date

        Examples
        --------

        >>> from datetime import datetime
        >>> d3.time_day.interval(datetime(2010, 1, 1, 12, 0))
        datetime.datetime(2010, 1, 1, 0, 0)
        """
        return self(date)

    def every(self, step: int) -> TTimeInterval:
        """
        Returns a filtered view of this interval representing
        every stepth date. The meaning of step is dependent on this
        interval's parent interval as defined by the field function.

        Parameters
        ----------
        step : int
            Step

        Returns
        -------
        TimeFilter
            Modified class with new :code:`floor` and :code:`offset` methods

        Examples
        --------
        >>> from datetime import datetime
        >>> every = d3.time_day.every(3)
        >>> r = every.range(datetime(2010, 1, 1), datetime(2010, 1, 8))
        >>> for d in r:
        ...     print(d)
        ...
        ...
        2010-01-01 00:00:00
        2010-01-04 00:00:00
        2010-01-07 00:00:00
        """
        step = int(step)
        if math.isinf(step) or not step > 0:
            return None
        if not step > 1:
            return self
        return self.filter(
            (lambda d: self.field(d) % step == 0)
            if self.field is not None
            else (lambda d: self.count(0, d) % step == 0)
        )

    def ceil(self, date: datetime) -> datetime:
        """
        Returns a new date representing the earliest interval
        boundary date after or equal to date.

        Parameters
        ----------
        date : datetime
            Date

        Returns
        -------
        datetime
            Ceiled date

        Examples
        --------

        >>> from datetime import datetime
        >>> d3.time_day.ceil(datetime(2010, 1, 1, 12, 0))
        datetime.datetime(2010, 1, 2, 0, 0)
        """
        return self.floor(self.offset(self.floor(date + timedelta(microseconds=-1)), 1))

    def round(self, date: datetime) -> datetime:
        """
        Returns a new date representing the closest interval
        boundary date to date.

        Parameters
        ----------
        date : datetime
            Date

        Returns
        -------
        datetime
            Rounded date

        Examples
        --------

        >>> from datetime import datetime
        >>> d3.time_day.round(datetime(2010, 1, 1, 12, 0))
        datetime.datetime(2010, 1, 2, 0, 0)
        >>> d3.time_day.round(datetime(2010, 1, 1, 1, 0))
        datetime.datetime(2010, 1, 1, 0, 0)
        """
        d0 = self.interval(date)
        d1 = self.ceil(date)
        return d0 if date - d0 < d1 - date else d1

    def range(self, start: datetime, stop: datetime, step: int = 1) -> list[datetime]:
        """
        Returns an array of dates representing every interval boundary after or
        equal to start (inclusive) and before stop (exclusive).

        Parameters
        ----------
        start : datetime
            Start date
        stop : datetime
            Stop date
        step : int
            Step

        Returns
        -------
        list[datetime]
            Range of dates

        Examples
        --------
        >>> from datetime import datetime
        >>> r = d3.time_day.range(datetime(2010, 1, 1), datetime(2010, 1, 5), step=1)
        >>> for d in r:
        ...     print(d)
        ...
        ...
        2010-01-01 00:00:00
        2010-01-02 00:00:00
        2010-01-03 00:00:00
        2010-01-04 00:00:00
        >>> r = d3.time_day.range(datetime(2010, 1, 1), datetime(2010, 1, 5), step=2)
        >>> for d in r:
        ...     print(d)
        ...
        ...
        2010-01-01 00:00:00
        2010-01-03 00:00:00
        """
        range_list = []
        start = self.ceil(start)
        if not (start < stop) or not (step > 0):
            return range_list

        previous = None
        while previous is None or (previous < start and start < stop):
            previous = start
            range_list.append(previous)
            start = self.floor(self.offset(start, step))

        return range_list

    @classmethod
    def filter(cls, test: Callable[[datetime], bool]) -> TTimeInterval:
        """
        Returns a new interval that is a filtered subset of this interval using
        the specified test function.

        Parameters
        ----------
        test : Callable[[datetime], bool]
            Function which returns :code:`True` if and only if the specified
            date should be considered part of the interval

        Returns
        -------
        TimeFilter
            Modified class with new :code:`floor` and :code`offset` function.
        """

        class TimeFilter(cls):
            """
            Modified class which calls several times :code:`floor`
            and :code:`offset` in order to achieve :code:`every(step)`
            function.
            """

            def floor(self, date: datetime):
                """
                Returns a new date representing the latest interval
                boundary date before or equal to date.

                Parameters
                ----------
                date : datetime
                    Date

                Returns
                -------
                datetime
                    Floored date
                """
                date = cls.floor(self, date)
                while not test(date):
                    date = cls.floor(self, date - timedelta(microseconds=1))
                return date

            def offset(self, date: datetime, step: int):
                """
                Returns a new date equal to date plus step intervals.

                Parameters
                ----------
                date : datetime
                    Date
                step : int
                    Step to add or substitute

                Returns
                -------
                datetime
                    Date
                """
                if step < 0:
                    step += 1
                    while step <= 0:
                        date = cls.offset(self, date, -1)
                        while not test(date):
                            date = cls.offset(self, date, -1)
                        step += 1
                else:
                    step -= 1
                    while step >= 0:
                        date = cls.offset(self, date, 1)
                        while not test(date):
                            date = cls.offset(self, date, 1)
                        step -= 1
                return date

        return TimeFilter()
