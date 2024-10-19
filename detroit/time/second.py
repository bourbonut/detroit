from .interval import TimeInterval
from datetime import timedelta

class TimeSecond(TimeInterval):

    def floor(self, date):
        return date.replace(microsecond=0)

    def offset(self, date, step):
        return date + timedelta(seconds=step)

    def count(self, start, end):
        return (end - start).seconds

    def field(self, date):
        return date.second

time_second = TimeSecond()
time_seconds = time_second.range
