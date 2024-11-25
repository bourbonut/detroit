from datetime import datetime, timedelta

from .interval import TimeInterval


class TimeMillisecond(TimeInterval):
    """
    Milliseconds in local time
    """

    def floor(self, date: datetime) -> datetime:
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
        return date.replace(microsecond=(date.microsecond // 1000) * 1000)

    def offset(self, date: datetime, step: int) -> datetime:
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
        return date + timedelta(milliseconds=step)

    def count(self, start: datetime, end: datetime) -> int:
        """
        Returns the number of interval boundaries after start
        (exclusive) and before or equal to end (inclusive).

        Parameters
        ----------
        start : datetime
            Start date
        end : datetime
            End date

        Returns
        -------
        int
            Count
        """
        return (end - start).milliseconds

    def field(self, date: datetime) -> int:
        """
        Returns the field value of the specified date, corresponding to the
        number of boundaries between this date (exclusive) and the latest
        previous parent boundary.

        Parameters
        ----------
        date : datetime
            Floored date

        Returns
        -------
        int
            Field value
        """
        return date.microsecond // 1000


time_millisecond = TimeMillisecond()
time_milliseconds = time_millisecond.range
