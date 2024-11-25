import math
from datetime import datetime

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
    def __init__(self):
        self._base = 10
        self._logs = None
        self._pows = None

    def set_base(self, base):
        self._base = float(base)
        return self._rescale()

    @property
    def base(self):
        return self._base

    def ticks(self, count=None):
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

    def tick_format(self, count=None, specifier=None):
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

    def nice(self):
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


def scale_log():
    scale = ScaleLog().set_domain([1, 10])
    return init_range(scale)
