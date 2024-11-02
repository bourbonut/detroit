from ..array import ticks
# from ..format import format, format_specifier
from .nice import nice
from .continuous import copy, Transformer
from .init import init_range
import math

def transform_log(x):
    return math.log(x)

def transform_exp(x):
    return math.exp(x)

def transform_logn(x):
    return -math.log(-x)

def transform_expn(x):
    return -math.exp(-x)

def pow10(x):
    return 10 ** x if math.isfinite(x) else 0 if x < 0 else x

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
    elif base == 10 and hasattr(math, 'log10'):
        return math.log10
    elif base == 2 and hasattr(math, 'log2'):
        return math.log2
    else:
        base = math.log(base)
        return lambda x: math.log(x) / base

def reflect(f):
    return lambda x, k: -f(-x, k)

class ScaleLog(Transformer):
    def __init__(self):
        super().__init__(transform_log, transform_exp)
        self._base = 10
        self._logs = None
        self._pows = None

    def rescale(self):
        logs = logp(self.base)
        pows = powp(self.base)
        if self.domain()[0] < 0:
            self._logs = reflect(logs)
            self._pows = reflect(pows)
            self.transform(transform_logn, transform_expn)
        else:
            self.transform(transform_log, transform_exp)
        return self

    def base(self, *args):
        if args:
            self._base = float(args[0])
            return self.rescale()
        return self._base

    def ticks(self, count):
        d = self.domain()
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
                    for k in range(1, self._base):
                        t = k / self._pows(-i) if i < 0 else k * self._pows(i)
                        if t < u:
                            continue
                        if t > v:
                            break
                        z.append(t)
            else:
                for i in range(i, j + 1):
                    for k in range(self._base - 1, 0, -1):
                        t = k / self._pows(-i) if i > 0 else k * self._pows(i)
                        if t < u:
                            continue
                        if t > v:
                            break
                        z.append(t)
            if len(z) * 2 < n:
                z = ticks(u, v, n)
        else:
            z = ticks(i, j, min(j - i, n)).map(self._pows)
        return z[::-1] if r else z

    def tick_format(self, count=None, specifier=None):
        if count is None:
            count = 10
        if specifier is None:
            specifier = "s" if self._base == 10 else ","
        if not callable(specifier):
            if not (self._base % 1) and (specifier := format_specifier(specifier)).precision is None:
                specifier.trim = True
            specifier = format(specifier)
        if count == float('inf'):
            return specifier
        k = max(1, self._base * count / len(self.ticks()))
        def f(d):
            i = d / self._pows(round(self._logs(d)))
            if i * self._base < self._base - 0.5:
                i *= self._base
            return specifier(d) if i <= k else ""
        return f

    def nice(self):
        return self.domain(nice(self.domain(), {
            'floor': lambda x: self._pows(math.floor(self._logs(x))),
            'ceil': lambda x: self._pows(math.ceil(self._logs(x)))
        }))

    def copy(self):
        return copy(self, self.log()).base(self.base())

def scale_log():
    scale = ScaleLog().domain([1, 10])
    return init_range(scale)
