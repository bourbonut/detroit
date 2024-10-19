from .interval import TimeInterval
from datetime import timedelta

class TimeHour(TimeInterval):

    def floor(self, date):
        return date.replace(minute=0, second=0, microsecond=0)

    def offset(self, date, step):
        return date + timedelta(hours=step)

    def count(self, start, end):
        return (end - start).hours

    def field(self, date):
        return date.hour

time_hour = TimeHour()
time_hours = time_hour.range
