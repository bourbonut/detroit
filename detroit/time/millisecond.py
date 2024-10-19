from .interval import TimeInterval
from datetime import timedelta

class TimeMillisecond(TimeInterval):

    def floor(self, date):
        return date

    def offset(self, date, step):
        return date + timedelta(milliseconds=step)

    def count(self, start, end):
        return (end - start).milliseconds

    def field(self, date):
        return date.millisecond

time_millisecond = TimeMillisecond()
time_milliseconds = time_millisecond.range
