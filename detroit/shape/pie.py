from dataclasses import dataclass
from .constant import constant

from math import pi

def identity(x):
    return x

@dataclass
class Arc:
    data: int
    index: int
    value: int
    start_angle: int
    end_angle: int
    pad_angle: int

class Pie:
    def __init__(self):
        self._value = identity
        self._sort_values = lambda x: sorted(x, key=lambda x: -x)
        self._sort = None
        self._start_angle = constant(0)
        self._end_angle = constant(2 * pi)
        self._pad_angle = constant(0)

    def __call__(self, data, *args):
        data = list(data)
        n = len(data)
        sum = 0
        index = [None] * n
        arcs = [None] * n
        a0 = self._start_angle(*args)
        da = min(2 * pi, max(-2 * pi, self._end_angle(*args) - a0))
        p = min(abs(da) / n, self._pad_angle(*args))
        pa = p * (-1 if da < 0 else 1)

        for i in range(n):
            d = data[i]
            v = self._value(d, i, data)
            index[i] = i
            arcs[i] = v
            if v > 0:
                sum += v

        if self._sort_values is not None:
            index = sorted(index, key=lambda i: self._sort_values(arcs[i]))
        elif self._sort is not None:
            index = sorted(index, key=lambda i: self._sort(data[i]))


        k = (da - n * pa) / sum if sum else 0
        a0 = None
        for i in range(n):
            j = index[i]
            v = arcs[j]
            a1 = a0 + (v * k if v > 0 else 0) + pa
            arcs[j] = Arc(data[j], i, v, a0, a1, p)

        return arcs

    def value(self, value):
        if callable(value):
            self._value = value
        else:
            self._value = constant(value)
        return self

    def sort_values(self, sort_values):
        self._sort_values = sort_values
        self._sort = None
        return self

    def sort(self, sort):
        self._sort = sort
        self._sort_values = None
        return self

    def start_angle(self, start_angle):
        if callable(start_angle):
            self._start_angle = start_angle
        else:
            self._start_angle = constant(start_angle)
        return self

    def end_angle(self, end_angle):
        if callable(end_angle):
            self._end_angle = end_angle
        else:
            self._end_angle = constant(end_angle)
        return self

    def pad_angle(self, pad_angle):
        if callable(pad_angle):
            self._pad_angle = pad_angle
        else:
            self._pad_angle = constant(pad_angle)
        return self
