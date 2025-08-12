import math
from collections.abc import Callable
from datetime import datetime
from typing import Any, TypeVar, overload

from ..interpolate import interpolate, interpolate_round, piecewise
from ..types import Number, T
from .continuous import identity
from .init import init_interpolator
from .linear import LinearBase
from .log import LogBase, logp, powp, reflect, transform_log, transform_logn
from .pow import transform_pow, transform_sqrt
from .sequential import copy
from .symlog import transform_symlog

TDiverging = TypeVar("Itself", bound="Diverging")
TDivergingLinear = TypeVar("Itself", bound="DivergingLinear")
TDivergingPow = TypeVar("Itself", bound="DivergingPow")
TDivergingLog = TypeVar("Itself", bound="DivergingLog")
TDivergingSymlog = TypeVar("Itself", bound="DivergingSymlog")


class Diverging:
    """
    Diverging scales are similar to linear scales in that they map
    a continuous, numeric input domain to a continuous output range.
    Unlike linear scales, the input domain and output range of a diverging
    scale always have exactly three elements, and the output range is
    typically specified as an interpolator rather than an array of values.
    Diverging scales are typically used for a color encoding; see also
    d3-scale-chromatic. These scales do not expose invert and interpolate
    methods. There are also log, pow, and symlog variants of diverging scales.

    Parameters
    ----------
    t : Callable[[float], float]
        Transform function
    """

    def __init__(self, t: Callable[[float], float]):
        self._transform = t
        self._x0 = 0
        self._x1 = 0.5
        self._x2 = 1
        self._t0 = t(self._x0)
        self._t1 = t(self._x1)
        self._t2 = t(self._x2)
        self._k10 = 0 if self._t0 == self._t1 else 0.5 / (self._t1 - self._t0)
        self._k21 = 0 if self._t1 == self._t2 else 0.5 / (self._t2 - self._t1)
        self._s = -1 if self._t1 < self._t0 else 1
        self._interpolator = identity
        self._clamp = False
        self._unknown = None

    def __call__(self, x: Number) -> float:
        """
        Given a value from the domain, returns the corresponding value from the range.

        Parameters
        ----------
        x : Number
            Input value

        Returns
        -------
        T
            Corresponding value from the range
        """
        if isinstance(x, float) and math.isnan(x):
            return self._unknown
        else:
            x = self._transform(x)
            k = self._k10 if self._s * x < self._s * self._t1 else self._k21
            x = 0.5 + (x - self._t1) * k
            return self._interpolator(max(0, min(1, x)) if self._clamp else x)

    def set_domain(self, domain: list[Number]) -> TDiverging:
        """
        Sets the scale's domain to the specified array of numbers

        Parameters
        ----------
        domain : list[Number]
            Domain

        Returns
        -------
        Diverging
            Itself
        """
        self._x0, self._x1, self._x2 = map(float, list(domain)[:3])
        self._t0 = self._transform(self._x0)
        self._t1 = self._transform(self._x1)
        self._t2 = self._transform(self._x2)
        self._k10 = 0 if self._t0 == self._t1 else 0.5 / (self._t1 - self._t0)
        self._k21 = 0 if self._t1 == self._t2 else 0.5 / (self._t2 - self._t1)
        self._s = -1 if self._t1 < self._t0 else 1
        return self

    def get_domain(self) -> list[Number]:
        return [self._x0, self._x1, self._x2]

    def set_clamp(self, clamp: bool) -> TDiverging:
        """
        Enables or disables clamping accordingly.

        Parameters
        ----------
        clamp : bool
            Clamp value

        Returns
        -------
        Diverging
            Itself
        """
        self._clamp = bool(clamp)
        return self

    def get_clamp(self) -> bool:
        return self._clamp

    def set_interpolator(self, interpolator: Callable) -> TDiverging:
        """
        Sets the scale’s interpolator to the specified function.

        Parameters
        ----------
        interpolator : Callable
            Interpolator function

        Returns
        -------
        Diverging
            Itself
        """
        self._interpolator = interpolator
        return self

    def get_interpolator(self) -> Callable:
        return self._interpolator

    def set_range(self, range_vals: list[T]) -> TDiverging:
        """
        The given two-element array is converted
        to an interpolator function using interpolate

        Parameters
        ----------
        range_vals : list[T]
            Two values

        Returns
        -------
        Diverging
            Itself
        """
        self._r0 = float(range_vals[0])
        self._r1 = float(range_vals[1])
        self._r2 = float(range_vals[2])
        self._interpolator = piecewise(interpolate, [self._r0, self._r1, self._r2])
        return self

    def set_range_round(self, range_vals: list[T]) -> TDiverging:
        """
        Sets the scale's range to the specified array of values
        and sets scale's interpolator to :code:`interpolate_round`.

        Parameters
        ----------
        range_vals : list[T]
            Range values

        Returns
        -------
        Diverging
            Itself
        """
        self._r0 = float(range_vals[0])
        self._r1 = float(range_vals[1])
        self._r2 = float(range_vals[2])
        self._interpolator = piecewise(
            interpolate_round, [self._r0, self._r1, self._r2]
        )
        return self

    def get_range(self) -> list[T]:
        return [self._interpolator(0), self._interpolator(0.5), self._interpolator(1)]

    def set_unknown(self, unknown: Any) -> TDiverging:
        """
        Sets the output value of the scale for undefined
        or NaN input values.

        Parameters
        ----------
        unknown : Any
            Unknown value

        Returns
        -------
        Diverging
            Itself
        """
        self._unknown = unknown
        return self

    def get_unknown(self) -> Any:
        return self._unknown

    def __str__(self) -> str:
        name = self.__class__.__name__
        attrbs = ["domain", "range"]
        attrbs = (f"{a}={getattr(self, f'get_{a}')()}" for a in attrbs)
        attrbs = ", ".join(attrbs)
        return f"{name}({attrbs})"

    def __repr__(self) -> str:
        name = self.__class__.__name__
        addr = id(self)
        return f"<{name} at {hex(addr)}>"


class DivergingLinear(Diverging, LinearBase):
    def __init__(self):
        Diverging.__init__(self, identity)

    def copy(self):
        return copy(self, DivergingLinear())


class DivergingLog(Diverging, LogBase):
    def __init__(self):
        Diverging.__init__(self, identity)
        LogBase.__init__(self)
        self._transform = transform_log
        self.set_domain([0.1, 1, 10])

    def _rescale(self):
        self._logs = logp(self._base)
        self._pows = powp(self._base)
        d = self.get_domain()[0]
        if isinstance(d, datetime):
            d = d.timestamp()
        if d < 0:
            self._logs = reflect(self._logs)
            self._pows = reflect(self._pows)
            self._transform = transform_logn
        else:
            self._transform = transform_log
        return self

    def set_domain(self, domain: list[Number]) -> TDivergingLog:
        """
        Sets the scale's domain to the specified array of numbers

        Parameters
        ----------
        domain : list[Number]
            Domain

        Returns
        -------
        DivergingLog
            Itself
        """
        self._x0, self._x1, self._x2 = map(float, list(domain)[:3])
        self._rescale()
        super().set_domain(domain)
        return self

    def copy(self):
        return copy(self, DivergingLog()).base(self.base)


class DivergingSymlog(Diverging):
    def __init__(self, c: Number = 1):
        self._c = c
        super().__init__(transform_symlog(self._c))

    def set_constant(self, c: Number) -> TDivergingSymlog:
        """
        Sets the symlog constant to the specified number and returns this scale.

        Parameters
        ----------
        c : Number
            Constant value

        Returns
        -------
        DivergingSymlog
            Itself
        """
        self._c = float(c)
        self._transform = transform_symlog(self._c)
        return self

    def copy(self):
        return copy(self, DivergingSymlog()).set_constant(self.constant)


class DivergingPow(Diverging, LinearBase):
    def __init__(self, t: Callable = identity):
        super().__init__(t)
        self._exponent = 1

    def _rescale(self):
        if self._exponent == 1:
            self._transform = identity
            return self
        elif self._exponent == 0.5:
            self._transform = transform_sqrt
            return self
        else:
            self._transform = transform_pow(self._exponent)
            return self

    def set_exponent(self, exponent: Number) -> TDivergingPow:
        """
        Sets the scale's exponent value.

        Parameters
        ----------
        exponent : Number
            Exponent value

        Returns
        -------
        DivergingPow
            Itself
        """
        self._exponent = float(exponent)
        return self._rescale()

    def get_exponent(self):
        return self._exponent

    def copy(self):
        return copy(self, DivergingPow()).set_exponent(self.get_exponent())


@overload
def scale_diverging() -> DivergingLinear: ...


@overload
def scale_diverging(interpolator: Callable) -> DivergingLinear: ...


@overload
def scale_diverging(
    domain: list[Number], interpolator: Callable
) -> DivergingLinear: ...


def scale_diverging(*args):
    """
    Builds a new diverging scale with the specified
    domain and interpolator function or array.

    Parameters
    ----------
    domain : list[Number]
        Array of numbers
    interpolator : Callable
        Interpolator function

    Returns
    -------
    DivergingLinear
        Diverging object

    Examples
    --------

    >>> scale = d3.scale_diverging([-1, 0, 1], d3.interpolate_rdbu)
    >>> steps = 8
    >>> for x in range(steps + 1):
    ...     x = -1 + 2 * x / steps
    ...     print(x, scale(x))
    ...
    ...
    -1.0 rgb(103, 0, 31)
    -0.75 rgb(184, 45, 53)
    -0.5 rgb(228, 130, 104)
    -0.25 rgb(250, 204, 180)
    0.0 rgb(242, 239, 238)
    0.25 rgb(191, 220, 235)
    0.5 rgb(107, 172, 208)
    0.75 rgb(42, 113, 174)
    1.0 rgb(5, 48, 97)
    >>> d3.interpolate_rdbu(0)
    'rgb(103, 0, 31)'
    >>> d3.interpolate_rdbu(1)
    'rgb(5, 48, 97)'
    """
    scale = DivergingLinear()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_diverging_log() -> DivergingLog: ...


@overload
def scale_diverging_log(interpolator: Callable) -> DivergingLog: ...


@overload
def scale_diverging_log(
    domain: list[Number], interpolator: Callable
) -> DivergingLog: ...


def scale_diverging_log(*args):
    """
    Builds a new diverging scale with a logarithmic
    transform, analogous to a log scale.

    Parameters
    ----------
    domain : list[Number]
        Array of numbers
    interpolator : Callable
        Interpolator function

    Returns
    -------
    DivergingLog
        Diverging object

    Examples
    --------

    >>> scale = d3.scale_diverging_log([1, 10, 100], d3.interpolate_rdbu)
    >>> steps = 10
    >>> for x in range(steps + 1):
    ...     x = 2 * x / steps
    ...     x = 10 ** x
    ...     print(x, scale(x))
    ...
    ...
    1.0 rgb(103, 0, 31)
    1.5848931924611136 rgb(172, 32, 47)
    2.51188643150958 rgb(213, 96, 80)
    3.9810717055349722 rgb(240, 162, 133)
    6.309573444801933 rgb(250, 215, 196)
    10.0 rgb(242, 239, 238)
    15.848931924611133 rgb(205, 227, 238)
    25.118864315095795 rgb(143, 194, 220)
    39.810717055349734 rgb(74, 148, 196)
    63.09573444801933 rgb(34, 101, 163)
    100.0 rgb(5, 48, 97)
    >>> d3.interpolate_rdbu(0)
    'rgb(103, 0, 31)'
    >>> d3.interpolate_rdbu(1)
    'rgb(5, 48, 97)'
    """
    scale = DivergingLog()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_diverging_symlog() -> DivergingSymlog: ...


@overload
def scale_diverging_symlog(interpolator: Callable) -> DivergingSymlog: ...


@overload
def scale_diverging_symlog(
    domain: list[Number], interpolator: Callable
) -> DivergingSymlog: ...


def scale_diverging_symlog(*args):
    """
    Builds a new diverging scale with a symmetric
    logarithmic transform, analogous to a symlog scale.

    Parameters
    ----------
    domain : list[Number]
        Array of numbers
    interpolator : Callable
        Interpolator function

    Returns
    -------
    DivergingSymlog
        Diverging object

    Examples
    --------

    >>> scale = d3.scale_diverging_symlog([1, 10, 100], d3.interpolate_rdbu)
    >>> scale = scale.set_constant(2)
    >>> steps = 10
    >>> for x in range(steps + 1):
    ...     x = 2 * x / steps
    ...     x = 10 ** x
    ...     print(x, scale(x))
    ...
    ...
    1.0 rgb(44, 0, 19)
    1.5848931924611136 rgb(79, 0, 27)
    2.51188643150958 rgb(129, 9, 35)
    3.9810717055349722 rgb(181, 41, 51)
    6.309573444801933 rgb(218, 106, 87)
    10.0 rgb(244, 176, 147)
    15.848931924611133 rgb(250, 228, 216)
    25.118864315095795 rgb(228, 237, 242)
    39.810717055349734 rgb(180, 214, 231)
    63.09573444801933 rgb(111, 174, 210)
    100.0 rgb(53, 126, 184)
    >>> d3.interpolate_rdbu(0)
    'rgb(103, 0, 31)'
    >>> d3.interpolate_rdbu(1)
    'rgb(5, 48, 97)'
    """
    scale = DivergingSymlog()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_diverging_pow() -> DivergingPow: ...


@overload
def scale_diverging_pow(interpolator: Callable) -> DivergingPow: ...


@overload
def scale_diverging_pow(
    domain: list[Number], interpolator: Callable
) -> DivergingPow: ...


def scale_diverging_pow(*args):
    """
    Builds a new diverging scale with an exponential
    transform, analogous to a power scale.


    Parameters
    ----------
    domain : list[Number]
        Array of numbers
    interpolator : Callable
        Interpolator function

    Returns
    -------
    DivergingPow
        Diverging object

    Examples
    --------

    >>> from math import sqrt
    >>> scale = d3.scale_diverging_pow([0, 1, 10], d3.interpolate_rdbu)
    >>> scale = scale.set_exponent(2)
    >>> steps = 10
    >>> for x in range(steps + 1):
    ...     x = sqrt(10) * x / steps
    ...     print(x, scale(x))
    ...
    ...
    0.0 rgb(103, 0, 31)
    0.31622776601683794 rgb(140, 13, 37)
    0.6324555320336759 rgb(213, 96, 80)
    0.9486832980505138 rgb(249, 232, 221)
    1.2649110640673518 rgb(233, 239, 242)
    1.5811388300841898 rgb(213, 231, 240)
    1.8973665961010275 rgb(180, 214, 232)
    2.213594362117866 rgb(131, 187, 217)
    2.5298221281347035 rgb(74, 148, 196)
    2.8460498941515415 rgb(36, 103, 166)
    3.1622776601683795 rgb(5, 48, 97)
    >>> d3.interpolate_rdbu(0)
    'rgb(103, 0, 31)'
    >>> d3.interpolate_rdbu(1)
    'rgb(5, 48, 97)'
    """
    scale = DivergingPow()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_diverging_sqrt() -> DivergingPow: ...


@overload
def scale_diverging_sqrt(interpolator: Callable) -> DivergingPow: ...


@overload
def scale_diverging_sqrt(
    domain: list[Number], interpolator: Callable
) -> DivergingPow: ...


def scale_diverging_sqrt(*args):
    """
    Builds a new diverging scale with a square-root
    transform, analogous to a sqrt scale.

    Parameters
    ----------
    domain : list[Number]
        Array of numbers
    interpolator : Callable
        Interpolator function

    Returns
    -------
    DivergingPow
        Diverging object

    Examples
    --------

    >>> scale = d3.scale_diverging_sqrt([0, 1, 10], d3.interpolate_rdbu)
    >>> steps = 10
    >>> for x in range(steps + 1):
    ...     x = 100 * x / steps
    ...     print(x, scale(x))
    ...
    ...
    0.0 rgb(103, 0, 31)
    10.0 rgb(194, 221, 235)
    20.0 rgb(148, 197, 222)
    30.0 rgb(108, 172, 209)
    40.0 rgb(77, 150, 197)
    50.0 rgb(56, 130, 186)
    60.0 rgb(42, 113, 174)
    70.0 rgb(31, 96, 159)
    80.0 rgb(22, 79, 139)
    90.0 rgb(13, 63, 118)
    100.0 rgb(5, 48, 97)
    >>> d3.interpolate_rdbu(0)
    'rgb(103, 0, 31)'
    >>> d3.interpolate_rdbu(1)
    'rgb(5, 48, 97)'
    """
    return scale_diverging_pow(*args).set_exponent(0.5)
