from .interval import TimeInterval
from datetime import timedelta

class TimeMonth(TimeInterval):

    def floor(self, date):
        return date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    def offset(self, date, step):
        return date + timedelta(days=step * 30)

    def count(self, start, end):
        return end.timedelta(start).days // 30

    def field(self, date):
        return date.day

time_month = TimeMonth()
time_months = time_month.range
