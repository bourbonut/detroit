from datetime import datetime, timedelta
import math


class TimeInterval:

    def interval(self, date=None):
        date = datetime.now() if date is None else date
        return self.floor(date)

    def every(self, step):
        step = int(step)
        if math.isinf(step) or not step > 0:
            return None
        if not step > 1:
            return self
        return self.filter(
            lambda d: self.field(d) % step == 0 if self.field is not None else lambda d: self.count(0, d) % step == 0
        )

    def ceil(self, date):
        return self.floor(self.offset(self.floor(date + timedelta(microseconds=-1)), 1))

    def round(self, date):
        d0 = self.interval(date)
        d1 = self.ceil(date)
        return d0 if date - d0 < d1 - date else d1

    def range(self, start, stop, step=1):
        range_list = []
        start = self.ceil(start)
        if not (start < stop) or not (step > 0):
            return range_list

        previous = None
        while previous is None or (previous < start and start < stop):
            previous = start
            range_list.append(previous)
            start = self.floor(self.offset(start, step))

        return range_list

    @classmethod
    def filter(cls, test):
        class TimeFilter(cls):
            def floor(self, date):
                date = cls.floor(self, date)
                while not test(date):
                    date = cls.floor(self, cls.offset(self, date, 1))
                return date

            def offset(self, date, step):
                if step < 0:
                    step += 1
                    while step <= 0:
                        date = cls.offset(self, date, -1)
                        while not test(date):
                            date = cls.offset(self, date, -1)
                        step += 1
                else:
                    step -= 1
                    while step >= 0:
                        date = cls.offset(self, date, 1)
                        while not test(date):
                            date = cls.offset(self, date, 1)
                        step -= 1
                return date

        return TimeFilter()
