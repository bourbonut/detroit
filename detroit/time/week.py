from datetime import datetime, timedelta

from .interval import TimeInterval


def time_weekday(i: int):
    class TimeWeekDay(TimeInterval):
        """
        Weeks in local time; typically 7 days
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
            return date.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(
                days=(date.weekday() + 7 - (i - 1)) % 7
            )

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
            return date + timedelta(weeks=step)

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
            index = (i + 6) % 7
            a = start.weekday()
            b = end.weekday()
            days = (
                list(range(a, b + 1))
                if a < b
                else list(range(a, 7)) + list(range(b + 1))
            )
            return (end - start).days // 7 + bool(
                index in days and (a != b or index == a)
            )

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
            return date.weekday()

    return TimeWeekDay()


time_sunday = time_week = time_weekday(0)
time_monday = time_weekday(1)
time_tuesday = time_weekday(2)
time_wednesday = time_weekday(3)
time_thursday = time_weekday(4)
time_friday = time_weekday(5)
time_saturday = time_weekday(6)

time_sundays = time_weeks = time_sunday.range
time_mondays = time_monday.range
time_tuesdays = time_tuesday.range
time_wednesdays = time_wednesday.range
time_thursdays = time_thursday.range
time_fridays = time_friday.range
time_saturdays = time_saturday.range
