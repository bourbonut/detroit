import math
from bisect import bisect
from collections.abc import Callable, Iterable
from typing import Any, TypeVar

from .argpass import argpass
from .extent import extent
from .nice import nice
from .threshold import threshold_sturges
from .ticks import tick_increment, ticks

Tbin = TypeVar("Itself", bound="bin")


def identity(x, *args):
    return x


def constant(*obj):
    if len(obj) == 1:
        obj = obj[0]

    def wrapper(*args):
        return obj

    return wrapper


class Bin:
    """
    Bin quantitative values into consecutive, non-overlapping
    intervals, as in histograms
    """

    def __init__(self):
        self._list = []
        self.x0 = None
        self.x1 = None

    def __len__(self) -> int:
        return len(self._list)

    def __getitem__(self, index: int):
        return self._list[index]

    def __setitem__(self, index, item):
        self._list[index] = item

    def append(self, item: int | float):
        self._list.append(item)

    def __str__(self):
        return f"Bin({self._list}, x0={self.x0}, x1={self.x1})"

    def __repr__(self):
        return str(self)

    def __eq__(self, bin) -> bool:
        return self._list == bin._list and self.x0 == self.x0 and self.x1 == self.x1


class bin:
    """
    Bin generator with the default settings
    """

    def __init__(self):
        self._value = argpass(identity)
        self._domain = extent
        self._threshold = threshold_sturges

    def __call__(self, data: Iterable[int | float]) -> list[Bin]:
        """
        Returns an array of bins, where each bin is an array
        containing the associated elements from the input data.

        Parameters
        ----------
        data : Iterable[int | float]
            Data samples

        Returns
        -------
        list[Bin]
            Array of bins

        Examples
        --------

        >>> d3.bin()([0, 0, 0, 10, 20, 20])
        [Bin([0, 0, 0], x0=0, x1=5), Bin([], x0=5, x1=10), Bin([10], x0=10, x1=15), Bin([], x0=15, x1=20), Bin([20, 20], x0=20, x1=25)]
        """
        if not isinstance(data, list):
            data = list(data)

        n = len(data)
        step = math.nan
        values = [None] * n

        for i in range(n):
            values[i] = self._value(data[i], i, data)

        xz = self._domain(values)
        x0, x1 = xz[0], xz[1]
        tz = self._threshold(values, x0, x1)

        if not isinstance(tz, (list, tuple)):
            max_ = x1
            tn = int(tz)
            if self._domain == extent:
                x0, x1 = nice(x0, x1, tn)
            tz = ticks(x0, x1, tn)

            if tz[0] <= x0:
                step = tick_increment(x0, x1, tn)

            if tz[-1] >= x1:
                if max_ >= x1 and self._domain == extent:
                    step = tick_increment(x0, x1, tn)
                    if math.isfinite(step):
                        if step > 0:
                            x1 = (math.floor(x1 / step) + 1) * step
                        elif step < 0:
                            x1 = (math.ceil(x1 * -step) + 1) / -step
                else:
                    tz.pop()

        m = len(tz)
        a = 0
        b = m
        while a < len(tz) and tz[a] <= x0:
            a += 1
        while b >= 0 and tz[b - 1] > x1:
            b -= 1
        if a or b < m:
            tz = tz[a:b]
            m = b - a

        bins = [None] * (m + 1)

        for i in range(m + 1):
            bins[i] = Bin()
            bins[i].x0 = tz[i - 1] if i > 0 else x0
            bins[i].x1 = tz[i] if i < m else x1

        if math.isfinite(step):
            if step > 0:
                for i in range(n):
                    if (x := values[i]) is not None and x0 <= x <= x1:
                        bins[min(m, math.floor((x - x0) / step))].append(data[i])
            elif step < 0:
                for i in range(n):
                    if (x := values[i]) is not None and x0 <= x <= x1:
                        j = math.floor((x0 - x) * step)
                        if j < len(tz):
                            bins[min(m, j + (tz[j] <= x))].append(data[i])
                        else:
                            bins[m].append(data[i])
        else:
            for i in range(n):
                if (x := values[i]) is not None and x0 <= x <= x1:
                    bins[bisect(tz, x, 0, m)].append(data[i])

        return bins

    def set_value(
        self, value: Callable[[int | float, int, Iterable[int | float]], float] | Any
    ) -> Tbin:
        """
        Sets value

        Parameters
        ----------
        Value : Callable[[int | float, int, Iterable[int | float]], float] | Any
            Value function or constant object

        Returns
        -------
        bin
            Itself
        """
        self._value = argpass(value if callable(value) else constant(value))
        return self

    def set_domain(
        self, domain: Callable[[float], float] | tuple[float, float]
    ) -> Tbin:
        """
        Sets domain

        Parameters
        ----------
        obj : Callable[[float], float] | tuple[float, float]
            Domain function or domain tuple

        Returns
        -------
        bin
            Itself
        """
        self._domain = domain if callable(domain) else constant(domain[0], domain[1])
        return self

    def set_thresholds(
        self, thresholds: Callable[[list[float | None]], float] | Any
    ) -> Tbin:
        """
        Sets thresholds

        Parameters
        ----------
        thresholds : Callable[[list[float | None]], float] | Any
            Object or function

        Returns
        -------
        bin
            Itself
        """
        self._threshold = thresholds if callable(thresholds) else constant(thresholds)
        return self

    def get_value(self):
        return self._value

    def get_domain(self):
        return self._domain

    def get_thresholds(self):
        return self._threshold
