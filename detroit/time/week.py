from .interval import TimeInterval
from datetime import timedelta

def time_weekday(i):
    class TimeWeekDay(TimeInterval):

        def floor(self, date):
            print(date, date.weekday())
            return date.replace(day=date.day - (date.weekday() + 7 - i) % 7, hour=0, minute=0, second=0, microsecond=0)

        def offset(self, date, step):
            return date + timedelta(weeks=step)

        def count(self, start, end):
            return (end - start).days // 7

        def field(self, date):
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
