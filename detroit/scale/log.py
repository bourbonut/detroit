import math
from collections.abc import Callable
from datetime import datetime
from typing import TypeVar, overload

from ..array import ticks
from ..format import format_specifier, locale_format
from ..types import Number
from .continuous import Transformer, copy
from .init import init_range
from .nice import nice

TLogBase = TypeVar("Itself", bound="LogBase")
TScaleLog = TypeVar("Itself", bound="ScaleLog")


def transform_log(x: datetime | float) -> float:
    if isinstance(x, datetime):
        x = x.timestamp()
    return math.log(x)


def transform_exp(x: datetime | float) -> float:
    if isinstance(x, datetime):
        x = x.timestamp()
    return math.exp(x)


def transform_logn(x: datetime | float) -> float:
    if isinstance(x, datetime):
        x = x.timestamp()
    return -math.log(-x)


def transform_expn(x: datetime | float) -> float:
    if isinstance(x, datetime):
        x = x.timestamp()
    return -math.exp(-x)


def pow10(x: datetime | float) -> float:
    if isinstance(x, datetime):
        x = x.timestamp()
    return 10**x if math.isfinite(x) else 0 if x < 0 else x


def powp(base: Number) -> Callable[[float], float]:
    if base == 10:
        return pow10
    elif base == math.e:
        return math.exp
    else:
        return lambda x: math.pow(base, x)


def logp(base: Number) -> Callable[[float], float]:
    if base == math.e:
        return math.log
    elif base == 10:
        return math.log10
    elif base == 2:
        return math.log2
    else:
        return lambda x: math.log(x, base)


def reflect(f: Callable[[float], float]) -> Callable[[float], float]:
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

    def set_base(self, base: Number) -> TLogBase:
        """
        Sets the scale's base value

        Parameters
        ----------
        base : Number
            Base value

        Returns
        -------
        LogBase
            Itself
        """
        self._base = float(base)
        return self._log_rescale()

    def get_base(self) -> Number:
        return self._base

    def ticks(self, count: int | None = None) -> TLogBase:
        """
        Like :code:`ScaleLinear.ticks`, but customized for a log scale.

        Parameters
        ----------
        count : int | None
            Count. If specified, the scale may return more or fewer
            values depending on the domain

        Returns
        -------
        LogBase
            Itself
        """
        d = self.get_domain()
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
    ) -> TLogBase:
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
        LogBase
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

    def nice(self) -> TLogBase:
        """
        Like :code:`ScaleLinear.nice`, except extends the domain
        to integer powers of base.

        Returns
        -------
        LogBase
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

        return self.set_domain(nice(self.get_domain(), Interval))


class ScaleLog(Transformer[float], LogBase):
    """
    Logarithmic ("log") scales are like linear scales except that a logarithmic
    transform is applied to the input domain value before the output range value
    is computed. The mapping to the range value y can be expressed as a function
    of the domain value x: :math:`y = m \\log(x) + b`.
    """

    def __init__(self):
        Transformer.__init__(self, transform_log, transform_exp)
        LogBase.__init__(self)

    def _log_rescale(self):
        self._logs = logp(self._base)
        self._pows = powp(self._base)
        d = self.get_domain()[0]
        if isinstance(d, datetime):
            d = d.timestamp()
        if d < 0:
            self._logs = reflect(self._logs)
            self._pows = reflect(self._pows)
            self._transform = transform_logn
            self._untransform = transform_expn
            self._rescale()
        else:
            self._transform = transform_log
            self._untransform = transform_exp
            self._rescale()
        return self

    def set_domain(self, domain: list[float]) -> TScaleLog:
        """
        Sets the scale's domain to the specified array of values.

        Parameters
        ----------
        domain : list[float]
            Domain

        Returns
        -------
        TScaleLog
            Itself
        """
        super().set_domain(domain)
        return self._log_rescale()

    def copy(self):
        return copy(self, ScaleLog()).set_base(self.get_base())


@overload
def scale_log() -> ScaleLog: ...


@overload
def scale_log(range_vals: list[Number]) -> ScaleLog: ...


@overload
def scale_log(domain: list[Number], range_vals: list[Number]) -> ScaleLog: ...


def scale_log(*args):
    """
    Builds a new log scale with the specified domain and range,
    the base 10, the default interpolator and clamping disabled.

    Parameters
    ----------
    domain : list[Number]
        Array of numbers
    range_vals : list[Number]
        Array of values

    Returns
    -------
    ScaleLog
        Scale object

    Examples
    --------

    >>> scale = d3.scale_log([1, 10], [0, 960])
    >>> steps = 10
    >>> for x in range(steps + 1):
    ...     x = x / steps
    ...     x = 10 ** x
    ...     print(x, scale(x))
    ...
    ...
    1.0 0.0
    1.2589254117941673 96.0
    1.5848931924611136 192.0
    1.9952623149688795 287.99999999999994
    2.51188643150958 383.99999999999994
    3.1622776601683795 480.0
    3.9810717055349722 576.0
    5.011872336272722 671.9999999999999
    6.309573444801933 767.9999999999999
    7.943282347242816 864.0
    10.0 960.0
    """
    scale = ScaleLog().set_domain([1, 10])
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
