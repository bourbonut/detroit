from __future__ import annotations

import math
from datetime import datetime
from typing import overload

from ..array import ticks
from ..format import format_specifier, locale_format
from .continuous import Transformer, copy
from .init import init_range
from .nice import nice


def transform_log(x):
    if isinstance(x, datetime):
        x = x.timestamp()
    return math.log(x)


def transform_exp(x):
    if isinstance(x, datetime):
        x = x.timestamp()
    return math.exp(x)


def transform_logn(x):
    if isinstance(x, datetime):
        x = x.timestamp()
    return -math.log(-x)


def transform_expn(x):
    if isinstance(x, datetime):
        x = x.timestamp()
    return -math.exp(-x)


def pow10(x):
    if isinstance(x, datetime):
        x = x.timestamp()
    return 10**x if math.isfinite(x) else 0 if x < 0 else x


def powp(base):
    if base == 10:
        return pow10
    elif base == math.e:
        return math.exp
    else:
        return lambda x: math.pow(base, x)


def logp(base):
    if base == math.e:
        return math.log
    elif base == 10:
        return math.log10
    elif base == 2:
        return math.log2
    else:
        return lambda x: math.log(x, base)


def reflect(f):
    def local_reflect(x):
        return -f(-x)

    return local_reflect


class LogBase:
    """
    Logarithmic ("log") scales are like linear scales except that
    a logarithmic transform is applied to the input domain value
    before the output range value is computed. The mapping to the
    range value y can be expressed as a function of the domain value x:
    :math:`y = m \\cdot \\log(x) + b`.
    """

    def __init__(self):
        self._base = 10
        self._logs = None
        self._pows = None

    def set_base(self, base: int | float) -> ScaleLog:
        """
        Sets the scale's base value

        Parameters
        ----------
        base : int | float
            Base value

        Returns
        -------
        ScaleLog
            Itself
        """
        self._base = float(base)
        return self._rescale()

    @property
    def base(self) -> int | float:
        return self._base

    def ticks(self, count: int | None = None) -> ScaleLog:
        """
        Like :code:`ScaleLinear.ticks`, but customized for a log scale.

        Parameters
        ----------
        count : int | None
            Count. If specified, the scale may return more or fewer
            values depending on the domain

        Returns
        -------
        ScaleLog
            Itself
        """
        d = self.domain
        u = d[0]
        v = d[-1]
        r = v < u

        if r:
            u, v = v, u

        i = self._logs(u)
        j = self._logs(v)
        k = None
        t = None
        n = count if count is not None else 10
        z = []

        if not (self._base % 1) and j - i < n:
            i = math.floor(i)
            j = math.ceil(j)
            if u > 0:
                for i in range(i, j + 1):
                    for k in range(1, int(self._base)):
                        t = k / self._pows(-i) if i < 0 else k * self._pows(i)
                        if t < u:
                            continue
                        if t > v:
                            break
                        z.append(t)
            else:
                for i in range(i, j + 1):
                    for k in range(int(self._base) - 1, 0, -1):
                        t = k / self._pows(-i) if i > 0 else k * self._pows(i)
                        if t < u:
                            continue
                        if t > v:
                            break
                        z.append(t)
            if len(z) * 2 < n:
                z = ticks(u, v, n)
        else:
            z = list(map(self._pows, ticks(i, j, min(j - i, n))))
        return z[::-1] if r else z

    def tick_format(
        self, count: int | None = None, specifier: str | None = None
    ) -> ScaleLog:
        """
        Like :code:`ScaleLinear.tick_format`, but customized for a log scale.
        The specified count typically has the same value as the count
        that is used to generate the tick values.

        Parameters
        ----------
        count : int | None
            Count. It should have the same value as the count
            that is used to generate the tick values.
        specifier : str | None
            Specifier


        Returns
        -------
        ScaleLog
            Itself
        """
        if count is None:
            count = 10
        if specifier is None:
            specifier = "s" if self._base == 10 else ","
        if not callable(specifier):
            specifier_obj = format_specifier(specifier)
            if (
                not (self._base % 1)
                and specifier_obj is not None
                and specifier_obj.precision is None
            ):
                specifier_obj.trim = True
            specifier = locale_format(specifier_obj or specifier)
        if math.isinf(count):
            return specifier
        k = max(1, self._base * count / len(self.ticks()))

        def f(d):
            i = d / self._pows(round(self._logs(d)))
            if i * self._base < self._base - 0.5:
                i *= self._base
            return specifier(d) if i <= k else ""

        return f

    def nice(self) -> ScaleLog:
        """
        Like :code:`ScaleLinear.nice`, except extends the domain
        to integer powers of base.

        Returns
        -------
        ScaleLog
            Itself
        """

        class Interval:
            @staticmethod
            def floor(x):
                if x == 0:
                    return 0
                return self._pows(math.floor(self._logs(x)))

            @staticmethod
            def ceil(x):
                if x == 0:
                    return 0
                return self._pows(math.ceil(self._logs(x)))

        return self.set_domain(nice(self.domain, Interval))


class ScaleLog(Transformer, LogBase):
    def __init__(self):
        Transformer.__init__(self, transform_log, transform_exp)
        LogBase.__init__(self)

    def _rescale(self):
        self._logs = logp(self._base)
        self._pows = powp(self._base)
        d = self.domain[0]
        if isinstance(d, datetime):
            d = d.timestamp()
        if d < 0:
            self._logs = reflect(self._logs)
            self._pows = reflect(self._pows)
            self.transform = transform_logn
            self.untransform = transform_expn
            super().rescale()
        else:
            self.transform = transform_log
            self.untransform = transform_exp
            super().rescale()
        return self

    def set_domain(self, domain):
        super().set_domain(domain)
        return self._rescale()

    def copy(self):
        return copy(self, ScaleLog()).set_base(self.base)


@overload
def scale_log() -> ScaleLog: ...


@overload
def scale_log(range_vals: list[int | float]) -> ScaleLog: ...


@overload
def scale_log(domain: list[int | float], range_vals: list[int | float]) -> ScaleLog: ...


def scale_log(*args):
    """
    Builds a new log scale with the specified domain and range,
    the base 10, the default interpolator and clamping disabled.

    Parameters
    ----------
    domain : list[int | float]
        Array of numbers
    range_vals : list[int | float]
        Array of values

    Returns
    -------
    ScaleLog
        Scale object

    Examples
    --------

    >>> d3.scale_log([1, 10], [0, 960])
    """
    scale = ScaleLog().set_domain([1, 10])
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
