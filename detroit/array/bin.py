from __future__ import annotations

import math
from bisect import bisect
from collections.abc import Callable, Iterable
from inspect import signature
from typing import Any

from .extent import extent
from .nice import nice
from .threshold import threshold_sturges
from .ticks import tick_increment, ticks


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

    def __len__(self):
        return len(self._list)

    def __getitem__(self, key):
        return self._list[key]

    def __setitem__(self, key, item):
        self._list[key] = item

    def append(self, item):
        self._list.append(item)

    def __str__(self):
        return f"Bin({self._list}, x0={self.x0}, x1={self.x1})"

    def __repr__(self):
        return str(self)

    def __eq__(self, bin):
        return self._list == bin._list and self.x0 == self.x0 and self.x1 == self.x1


class bin:
    """
    Bin generator with the default settings
    """

    def __init__(self):
        self._value = identity
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
        """
        if not isinstance(data, list):
            data = list(data)

        n = len(data)
        step = math.nan
        values = [None] * n

        nargs = len(signature(self._value).parameters)
        for i in range(n):
            args = [data[i], i, data][:nargs]
            values[i] = self._value(*args)

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

    def value(self, obj: Callable | Any | None = None) -> Callable | bin:
        """
        Set value to the given object or return the current value

        Parameters
        ----------
        obj : Callable | Any | None
            Object or function

        Returns
        -------
        Callable | bin
            Current value or updated self
        """
        if obj is None:
            return self._value
        elif callable(obj):
            self._value = obj
            return self
        else:
            self._value = constant(obj)
            return self

    def domain(self, obj: Callable | Any | None = None) -> Callable | bin:
        """
        Set domain to the given object or return the current domain

        Parameters
        ----------
        obj : Callable | Any | None
            Object or function

        Returns
        -------
        Callable | bin
            Current domain or updated self
        """
        if obj is None:
            return self._domain
        elif callable(obj):
            self._domain = obj
            return self
        else:
            self._domain = constant(obj[0], obj[1])
            return self

    def thresholds(self, obj: Callable | Any | None = None) -> Callable | bin:
        """
        Set thresholds to the given object or return the current thresholds

        Parameters
        ----------
        obj : Callable | Any | None
            Object or function

        Returns
        -------
        Callable | bin
            Current thresholds or updated self
        """
        if obj is None:
            return self._threshold
        elif callable(obj):
            self._threshold = obj
            return self
        else:
            self._threshold = constant(obj)
            return self
