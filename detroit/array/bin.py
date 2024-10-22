import math
from bisect import bisect
from .extent import extent
from .nice import nice
from .ticks import ticks, tick_increment
from .threshold.sturges import sturges

def identity(x):
    return x

def constant(obj):
    def wrapper():
        return obj
    return wrapper

class Bin:

    def __init__(self):
        self.value = identity
        self.domain = extent
        self.threshold = sturges

    def __call__(self, data):
        if not isinstance(data, list):
            data = list(data)

        n = len(data)
        values = [0] * n

        for i in range(n):
            values[i] = value(data[i], i, data)

        xz = domain(values)
        x0, x1 = xz[0], xz[1]
        tz = threshold(values, x0, x1)

        if not isinstance(tz, list):
            max_ = x1
            tn = int(tz)
            if domain == extent:
                x0, x1 = nice(x0, x1, tn)
            tz = ticks(x0, x1, tn)

            if tz[0] <= x0:
                step = tick_increment(x0, x1, tn)

            if tz[-1] >= x1:
                if max_ >= x1 and domain == extent:
                    step = tick_increment(x0, x1, tn)
                    if step.is_finite():
                        if step > 0:
                            x1 = (math.floor(x1 / step) + 1) * step
                        elif step < 0:
                            x1 = (math.ceil(x1 * -step) + 1) / -step
                else:
                    tz.pop()

        m = len(tz)
        a = 0
        b = m
        while tz[a] <= x0:
            a += 1
        while tz[b - 1] > x1:
            b -= 1
        if a or b < m:
            tz = tz[a:b]
            m = b - a

        bins = [None] * (m + 1)

        for i in range(m + 1):
            bin_ = bins[i] = []
            bin_.x0 = tz[i - 1] if i > 0 else x0
            bin_.x1 = tz[i] if i < m else x1

        if step.is_finite():
            if step > 0:
                for i in range(n):
                    if (x := values[i]) is not None and x0 <= x <= x1:
                        bins[min(m, math.floor((x - x0) / step))].append(data[i])
            elif step < 0:
                for i in range(n):
                    if (x := values[i]) is not None and x0 <= x <= x1:
                        j = math.floor((x0 - x) * step)
                        bins[min(m, j + (tz[j] <= x))].append(data[i])
        else:
            for i in range(n):
                if (x := values[i]) is not None and x0 <= x <= x1:
                    bins[bisect(tz, x, 0, m)].append(data[i])

        return bins

    def value(self, obj=None):
        if obj is None:
            return self.value
        elif callable(obj):
            return obj
        else:
            self.value = constant(obj)
            return self.histogram

    def domain(self, obj=None):
        if f is None:
            return self.domain
        elif callable(obj):
            return obj
        else:
            self.domain = constant(obj[0], obj[1])
            return self

    def thresholds(self, f=None):
        if f is None:
            return self.threshold
        elif callable(obj):
            return obj
        else:
            self.threshold = constant(list(obj))
            return self
