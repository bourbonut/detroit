from __future__ import annotations

import math
from collections.abc import Callable
from datetime import datetime
from typing import Any, TypeVar, overload

from ..interpolate import interpolate, interpolate_round
from .continuous import identity
from .init import init_interpolator
from .linear import LinearBase
from .log import LogBase, logp, powp, reflect, transform_log, transform_logn
from .pow import transform_pow, transform_sqrt
from .symlog import transform_symlog

T = TypeVar("T")


class Sequential:
    def __init__(self, t: Callable):
        self._x0 = 0
        self._x1 = 1
        self._transform = t
        self._t0 = t(self._x0)
        self._t1 = t(self._x1)
        self._k10 = 0 if self._t0 == self._t1 else 1 / (self._t1 - self._t0)
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
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return self._unknown
        if self._k10 == 0:
            x = 0.5
        else:
            x = (self._transform(x) - self._t0) * self._k10
            if self._clamp:
                x = max(0, min(1, x))
        return self._interpolator(x)

    def set_domain(self, domain: list[int | float]) -> Sequential:
        """
        Sets the scale's domain to the specified array of numbers

        Parameters
        ----------
        domain : list[int | float]
            Domain

        Returns
        -------
        Sequential
            Itself
        """
        self._x0, self._x1 = map(float, list(domain)[:2])
        self._t0 = self._transform(self._x0)
        self._t1 = self._transform(self._x1)
        self._k10 = 0 if self._t0 == self._t1 else 1 / (self._t1 - self._t0)
        return self

    @property
    def domain(self) -> list[int | float]:
        return [self._x0, self._x1]

    def set_clamp(self, clamp: bool) -> Sequential:
        """
        Enables or disables clamping accordingly.

        Parameters
        ----------
        clamp : bool
            Clamp value

        Returns
        -------
        Sequential
            Itself
        """
        self._clamp = bool(clamp)
        return self

    @property
    def clamp(self) -> bool:
        return self._clamp

    def set_interpolator(self, interpolator: Callable) -> Sequential:
        """
        Sets the scale’s interpolator to the specified function.

        Parameters
        ----------
        interpolator : Callable
            Interpolator function

        Returns
        -------
        Sequential
            Itself
        """
        self._interpolator = interpolator
        return self

    @property
    def interpolator(self) -> Callable:
        return self._interpolator

    def set_range(self, range_vals: list[T]) -> Sequential:
        """
        The given two-element array is converted
        to an interpolator function using interpolate

        Parameters
        ----------
        range_vals : list[T]
            Two values

        Returns
        -------
        Sequential
            Itself
        """
        self._r0, self._r1 = list(range_vals)[:2]
        self._interpolator = interpolate(self._r0, self._r1)
        return self

    @property
    def range(self) -> list[T]:
        return [self._interpolator(0), self._interpolator(1)]

    def set_range_round(self, range_vals: list[T]) -> Sequential:
        """
        Sets the scale's range to the specified array of values
        and sets scale's interpolator to :code:`interpolate_round`.

        Parameters
        ----------
        range_vals : list[T]
            Range values

        Returns
        -------
        Sequential
            Itself
        """
        self._r0, self._r1 = range_vals
        self._interpolator = interpolate_round(self._r0, self._r1)
        return self

    @property
    def range_round(self) -> list[T]:
        return [self._interpolator(0), self._interpolator(1)]

    def set_unknown(self, unknown: Any) -> Sequential:
        """
        Sets the output value of the scale for undefined
        or NaN input values.

        Parameters
        ----------
        unknown : Any
            Unknown value

        Returns
        -------
        Sequential
            Itself
        """
        self._unknown = unknown
        return self

    @property
    def unknown(self) -> Any:
        return self._unknown


def copy(source, target):
    return (
        target.set_domain(source.domain)
        .set_interpolator(source.interpolator)
        .set_clamp(source.clamp)
        .set_unknown(source.unknown)
    )


class SequentialLinear(Sequential, LinearBase):
    def __init__(self):
        Sequential.__init__(self, identity)

    def copy(self):
        return copy(self, SequentialLinear())


class SequentialLog(Sequential, LogBase):
    def __init__(self):
        Sequential.__init__(self)
        LogBase.__init__(self)
        self.transform = transform_log
        self.set_domain([1, 10])

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

    def set_domain(self, domain: list[int | float]) -> SequentialLog:
        """
        Sets the scale's domain to the specified array of numbers

        Parameters
        ----------
        domain : list[int | float]
            Domain

        Returns
        -------
        SequentialLog
            Itself
        """
        self._x0, self._x1 = map(float, list(domain)[:2])
        self._rescale()
        super().set_domain(domain)
        return self

    def copy(self):
        return copy(self, SequentialLog()).base(self.base)


class SequentialSymlog(Sequential):
    def __init__(self, c: int | float = 1):
        self._c = c
        super().__init__(transform_symlog(self._c))

    def set_constant(self, c: int | float) -> SequentialLog:
        """
        Sets the symlog constant to the specified number and returns this scale.

        Parameters
        ----------
        c : int | float
            Constant value

        Returns
        -------
        SequentialLog
            Itself
        """
        self._c = float(c)
        self.transform = transform_symlog(self._c)
        self.rescale()
        return self

    def copy(self):
        return copy(self, SequentialSymlog()).set_constant(self.constant)


class SequentialPow(Sequential, LinearBase):
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

    def set_exponent(self, exponent: int | float) -> SequentialPow:
        """
        Sets the scale's exponent value.

        Parameters
        ----------
        exponent : int | float
            Exponent value

        Returns
        -------
        SequentialPow
            Itself
        """
        self._exponent = float(exponent)
        return self._rescale()

    @property
    def exponent(self):
        return self._exponent

    def copy(self):
        return copy(self, SequentialPow()).set_exponent(self.exponent)


@overload
def scale_sequential() -> SequentialLinear: ...


@overload
def scale_sequential(interpolator: Callable) -> SequentialLinear: ...


@overload
def scale_sequential(
    domain: list[int | float], interpolator: Callable
) -> SequentialLinear: ...


def scale_sequential(*args):
    """
    Builds a new sequential scale with the specified
    domain and interpolator function or array.

    Parameters
    ----------
    domain : list[int | float]
        Domain
    interpolator : Callable
        Interpolator

    Returns
    -------
    SequentialLinear
        Sequential object

    Examples
    --------

    >>> d3.scale_sequential([0, 100], d3.interpolate_blues)
    """
    scale = SequentialLinear()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_sequential_log() -> SequentialLog: ...


@overload
def scale_sequential_log(interpolator: Callable) -> SequentialLog: ...


@overload
def scale_sequential_log(
    domain: list[int | float], interpolator: Callable
) -> SequentialLog: ...


def scale_sequential_log(*args):
    """
    Builds a new sequential scale with a logarithmic
    transform, analogous to a log scale.

    Parameters
    ----------
    domain : list[int | float]
        Domain
    interpolator : Callable
        Interpolator

    Returns
    -------
    SequentialLog
        Sequential object

    Examples
    --------

    >>> d3.scale_sequential_log([0, 100], d3.interpolate_blues)
    """
    scale = SequentialLog()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_sequential_symlog() -> SequentialSymlog: ...


@overload
def scale_sequential_symlog(interpolator: Callable) -> SequentialSymlog: ...


@overload
def scale_sequential_symlog(
    domain: list[int | float], interpolator: Callable
) -> SequentialSymlog: ...


def scale_sequential_symlog(*args):
    """
    Builds a new sequential scale with a symmetric
    logarithmic transform, analogous to a symlog scale.

    Parameters
    ----------
    domain : list[int | float]
        Domain
    interpolator : Callable
        Interpolator

    Returns
    -------
    SequentialSymlog
        Sequential object

    Examples
    --------

    >>> d3.scale_sequential_symlog([0, 100], d3.interpolate_blues)
    """
    scale = SequentialSymlog()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_sequential_pow() -> SequentialPow: ...


@overload
def scale_sequential_pow(interpolator: Callable) -> SequentialPow: ...


@overload
def scale_sequential_pow(
    domain: list[int | float], interpolator: Callable
) -> SequentialPow: ...


def scale_sequential_pow(*args):
    """
    Builds a new sequential scale with an exponential
    transform, analogous to a power scale.


    Parameters
    ----------
    domain : list[int | float]
        Domain
    interpolator : Callable
        Interpolator

    Returns
    -------
    SequentialPow
        Sequential object

    Examples
    --------

    >>> d3.scale_sequential_pow([0, 100], d3.interpolate_blues)
    """
    scale = SequentialPow()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_sequential_sqrt() -> SequentialPow: ...


@overload
def scale_sequential_sqrt(interpolator: Callable) -> SequentialPow: ...


@overload
def scale_sequential_sqrt(
    domain: list[int | float], interpolator: Callable
) -> SequentialPow: ...


def scale_sequential_sqrt(*args):
    """
    Builds a new sequential scale with a square-root
    transform, analogous to a sqrt scale


    Parameters
    ----------
    domain : list[int | float]
        Domain
    interpolator : Callable
        Interpolator

    Returns
    -------
    SequentialSqrt
        Sequential object

    Examples
    --------

    >>> d3.scale_sequential_sqrt([0, 100], d3.interpolate_blues)
    """
    return scale_sequential_pow(*args).set_exponent(0.5)
