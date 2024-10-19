from .interval import TimeInterval
from datetime import timedelta

class TimeMinute(TimeInterval):

    def floor(self, date):
        return date.replace(second=0, microsecond=0)

    def offset(self, date, step):
        return date + timedelta(minutes=step)

    def count(self, start, end):
        return (end - start).minutes

    def field(self, date):
        return date.minute

time_minute = TimeMinute()
time_minutes = time_minute.range
