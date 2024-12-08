from __future__ import annotations

import math
from collections.abc import Callable
from datetime import datetime
from typing import Any, TypeVar, overload

from ..interpolate import interpolate, interpolate_round, piecewise
from .continuous import identity
from .init import init_interpolator
from .linear import LinearBase
from .log import LogBase, logp, powp, reflect, transform_log, transform_logn
from .pow import transform_pow, transform_sqrt
from .sequential import copy
from .symlog import transform_symlog

T = TypeVar("T")


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
    t : Callable
        Transform function
    """

    def __init__(self, t: Callable):
        self.transform = t
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

    def __call__(self, x: int | float) -> T:
        """
        Given a value from the domain, returns the corresponding value from the range.

        Parameters
        ----------
        x : int | float
            Input value

        Returns
        -------
        T
            Corresponding value from the range
        """
        if isinstance(x, float) and math.isnan(x):
            return self._unknown
        else:
            x = self.transform(x)
            k = self._k10 if self._s * x < self._s * self._t1 else self._k21
            x = 0.5 + (x - self._t1) * k
            return self._interpolator(max(0, min(1, x)) if self._clamp else x)

    def set_domain(self, domain: list[int | float]) -> Diverging:
        """
        Sets the scale's domain to the specified array of numbers

        Parameters
        ----------
        domain : list[int | float]
            Domain

        Returns
        -------
        Diverging
            Itself
        """
        self._x0, self._x1, self._x2 = map(float, list(domain)[:3])
        self._t0 = self.transform(self._x0)
        self._t1 = self.transform(self._x1)
        self._t2 = self.transform(self._x2)
        self._k10 = 0 if self._t0 == self._t1 else 0.5 / (self._t1 - self._t0)
        self._k21 = 0 if self._t1 == self._t2 else 0.5 / (self._t2 - self._t1)
        self._s = -1 if self._t1 < self._t0 else 1
        return self

    @property
    def domain(self) -> list[int | float]:
        return [self._x0, self._x1, self._x2]

    def set_clamp(self, clamp: bool) -> Diverging:
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

    @property
    def clamp(self) -> bool:
        return self._clamp

    def set_interpolator(self, interpolator: Callable) -> Diverging:
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

    @property
    def interpolator(self) -> Callable:
        return self._interpolator

    def set_range(self, range_vals: list[T]) -> Diverging:
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

    def set_range_round(self, range_vals: list[T]) -> Diverging:
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

    @property
    def range(self) -> list[T]:
        return [self._interpolator(0), self._interpolator(0.5), self._interpolator(1)]

    def set_unknown(self, unknown: Any) -> Diverging:
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

    @property
    def unknown(self) -> Any:
        return self._unknown


class DivergingLinear(Diverging, LinearBase):
    def __init__(self):
        Diverging.__init__(self, identity)

    def copy(self):
        return copy(self, DivergingLinear())


class DivergingLog(Diverging, LogBase):
    def __init__(self):
        Diverging.__init__(self, identity)
        LogBase.__init__(self)
        self.transform = transform_log
        self.set_domain([0.1, 1, 10])

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
        else:
            self.transform = transform_log
        return self

    def set_domain(self, domain: list[int | float]) -> DivergingLog:
        """
        Sets the scale's domain to the specified array of numbers

        Parameters
        ----------
        domain : list[int | float]
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
    def __init__(self, c: int | float = 1):
        self._c = c
        super().__init__(transform_symlog(self._c))

    def set_constant(self, c: int | float) -> DivergingSymlog:
        """
        Sets the symlog constant to the specified number and returns this scale.

        Parameters
        ----------
        c : int | float
            Constant value

        Returns
        -------
        DivergingSymlog
            Itself
        """
        self._c = float(c)
        self.transform = transform_symlog(self._c)
        self.rescale()
        return self

    def copy(self):
        return copy(self, DivergingSymlog()).set_constant(self.constant)


class DivergingPow(Diverging, LinearBase):
    def __init__(self, t: Callable = identity):
        super().__init__(t)
        self._exponent = 1

    def _rescale(self):
        if self._exponent == 1:
            self.transform = identity
            self.rescale()
            return self
        elif self._exponent == 0.5:
            self.transform = transform_sqrt
            self.rescale()
            return self
        else:
            self.transform = transform_pow(self._exponent)
            self.rescale()
            return self

    def set_exponent(self, exponent: int | float) -> DivergingPow:
        """
        Sets the scale's exponent value.

        Parameters
        ----------
        exponent : int | float
            Exponent value

        Returns
        -------
        DivergingPow
            Itself
        """
        self._exponent = float(exponent)
        return self._rescale()

    @property
    def exponent(self):
        return self._exponent

    def copy(self):
        return copy(self, DivergingPow()).set_exponent(self.exponent)


@overload
def scale_diverging() -> DivergingLinear: ...


@overload
def scale_diverging(interpolator: Callable) -> DivergingLinear: ...


@overload
def scale_diverging(
    domain: list[int | float], interpolator: Callable
) -> DivergingLinear: ...


def scale_diverging(*args):
    """
    Builds a new diverging scale with the specified
    domain and interpolator function or array.

    Parameters
    ----------
    domain : list[int | float]
        Array of numbers
    interpolator : Callable
        Interpolator function

    Returns
    -------
    DivergingLinear
        Diverging object

    Examples
    --------

    >>> d3.scale_diverging([-1, 0, 1], d3.interpolate_RdBu)
    """
    scale = DivergingLinear()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_diverging_log() -> DivergingLinear: ...


@overload
def scale_diverging_log(interpolator: Callable) -> DivergingLinear: ...


@overload
def scale_diverging_log(
    domain: list[int | float], interpolator: Callable
) -> DivergingLinear: ...


def scale_diverging_log(*args):
    """
    Builds a new diverging scale with a logarithmic
    transform, analogous to a log scale.

    Parameters
    ----------
    domain : list[int | float]
        Array of numbers
    interpolator : Callable
        Interpolator function

    Returns
    -------
    DivergingLog
        Diverging object

    Examples
    --------

    >>> d3.scale_diverging_log([1, 10, 100], d3.interpolate_RdBu)
    """
    scale = DivergingLog()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_diverging_symlog() -> DivergingLinear: ...


@overload
def scale_diverging_symlog(interpolator: Callable) -> DivergingLinear: ...


@overload
def scale_diverging_symlog(
    domain: list[int | float], interpolator: Callable
) -> DivergingLinear: ...


def scale_diverging_symlog(*args):
    """
    Builds a new diverging scale with a symmetric
    logarithmic transform, analogous to a symlog scale.

    Parameters
    ----------
    domain : list[int | float]
        Array of numbers
    interpolator : Callable
        Interpolator function

    Returns
    -------
    DivergingSymlog
        Diverging object

    Examples
    --------

    >>> d3.scale_diverging_symlog([1, 10, 100], d3.interpolate_RdBu)
    """
    scale = DivergingSymlog()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_diverging_pow() -> DivergingLinear: ...


@overload
def scale_diverging_pow(interpolator: Callable) -> DivergingLinear: ...


@overload
def scale_diverging_pow(
    domain: list[int | float], interpolator: Callable
) -> DivergingLinear: ...


def scale_diverging_pow(*args):
    """
    Builds a new diverging scale with an exponential
    transform, analogous to a power scale.


    Parameters
    ----------
    domain : list[int | float]
        Array of numbers
    interpolator : Callable
        Interpolator function

    Returns
    -------
    DivergingPow
        Diverging object

    Examples
    --------

    >>> d3.scale_diverging_pow([0, 1, 10], d3.interpolate_RdBu)
    """
    scale = DivergingPow()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_diverging_sqrt() -> DivergingLinear: ...


@overload
def scale_diverging_sqrt(interpolator: Callable) -> DivergingLinear: ...


@overload
def scale_diverging_sqrt(
    domain: list[int | float], interpolator: Callable
) -> DivergingLinear: ...


def scale_diverging_sqrt(*args):
    """
    Builds a new diverging scale with a square-root
    transform, analogous to a sqrt scale.

    Parameters
    ----------
    domain : list[int | float]
        Array of numbers
    interpolator : Callable
        Interpolator function

    Returns
    -------
    DivergingSqrt
        Diverging object

    Examples
    --------

    >>> d3.scale_diverging_sqrt([0, 1, 10], d3.interpolate_RdBu)
    """
    return scale_diverging_pow(*args).exponent(0.5)
