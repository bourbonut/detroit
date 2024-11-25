from calendar import isleap
from datetime import datetime, timedelta

from .interval import TimeInterval


class TimeYear(TimeInterval):
    """
    Years in local time; ranges from 365 days to 366 days
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
        return date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

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
        sign = -1 if step < 0 else 1
        return date + timedelta(days=step * 365 + sign * isleap(date.year))

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
        return (end - start).days // 365

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
        return date.year


time_year = TimeYear()
time_years = time_year.range
