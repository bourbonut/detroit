from datetime import datetime, timedelta

from .interval import TimeInterval


class TimeMonth(TimeInterval):
    """
    Months in local time; ranges from 28 days to 31 days
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
        return date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

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
        return date + timedelta(days=step * 31)

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
        days = (end - start).days
        return days // 30 + bool(0 < days % 30 <= 15)

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
        return date.month - 1


time_month = TimeMonth()
time_months = time_month.range
