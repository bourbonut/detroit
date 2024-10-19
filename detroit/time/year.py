from .interval import TimeInterval
from datetime import timedelta

class TimeYear(TimeInterval):

    def floor(self, date):
        return date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    def offset(self, date, step):
        return date + timedelta(days=step * 365)

    def count(self, start, end):
        return (end - start).days // 365

    def field(self, date):
        return date.year

time_year = TimeYear()
time_years = time_year.range

# def every_time_year(k):
#     k = int(k)
#     if math.isinf(k) or not k > 0:
#         return None
#     return TimeInterval(
#         lambda date: date.replace(year=(date.year // k) * k, month=1, day=1, hour=0, minute=0, second=0, microsecond=0),
#         lambda date, step: date.replace(year=date.year + step * k)
#     )
