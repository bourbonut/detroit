from .interval import TimeInterval
from datetime import timedelta

class TimeDay(TimeInterval):

    def floor(self, date):
        return date.replace(hour=0, minute=0, second=0, microsecond=0)

    def offset(self, date, step):
        return date + timedelta(days=step)

    def count(self, start, end):
        return (end - start).days

    def field(self, date):
        return date.day

time_day = TimeDay()
time_days = time_day.range
