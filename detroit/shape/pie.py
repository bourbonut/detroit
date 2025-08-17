from collections.abc import Callable, Iterable
from dataclasses import asdict, dataclass
from math import pi
from typing import Generic, TypeVar

from ..array import argpass
from ..types import Accessor, Number, T
from .constant import constant


def identity(x):
    return x


TPie = TypeVar("Pie", bound="Pie")


@dataclass
class Arc:
    data: float
    index: int
    value: float
    start_angle: float
    end_angle: float
    pad_angle: float


class Pie(Generic[T]):
    """
    The pie generator computes the necessary angles to represent a tabular
    dataset as a pie or donut chart; these angles can then be passed to an
    arc generator. (The pie generator does not produce a shape directly.)
    """

    def __init__(self):
        self._value = argpass(identity)
        self._sort_values = lambda x: -x
        self._sort = None
        self._start_angle = argpass(constant(0))
        self._end_angle = argpass(constant(2 * pi))
        self._pad_angle = argpass(constant(0))

    def __call__(self, data: Iterable[T], *args) -> list[dict]:
        """
        Generates a pie for the given array of data, returning an array of
        objects representing each datum's arc angles.

        Parameters
        ----------
        data : Iterable[T]
            Data input
        args : Any
            Additional arguments propagated to the pie's accessor functions

        Returns
        -------
        list[dict]
            List of arcs

        Examples
        --------

        For example, given a set of numbers, here is how to compute the
        angles for a pie chart:

        >>> data = [1, 1, 2, 3, 5, 8, 13, 21]
        >>> pie = d3.pie()
        >>> pie(data)

        Each object in the returned array has the following properties:

        - :code:`data` - the input datum; the corresponding element in the input data array.
        - :code:`value` - the numeric value of the arc.
        - :code:`index` - the zero-based sorted index of the arc.
        - :code:`start_angle` - the start angle of the arc.
        - :code:`end_angle` - the end angle of the arc.
        - :code:`pad_angle` - the pad angle of the arc.
        """
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
        for i in range(n):
            j = index[i]
            v = arcs[j]
            a1 = a0 + (v * k if v > 0 else 0) + pa
            arcs[j] = asdict(Arc(data[j], i, v, a0, a1, p))
            a0 = a1

        return arcs

    def set_value(self, value: Accessor[T, float] | Number) -> TPie:
        """
        If value is specified, sets the value accessor to the
        specified function or number and returns this pie generator.

        Parameters
        ----------
        value : Accessor[T, float] | Number
            Number or accessor function

        Returns
        -------
        Pie
            Itself
        """
        if callable(value):
            self._value = value
        else:
            self._value = constant(value)
        self._value = argpass(self._value)
        return self

    def set_sort_values(self, sort_values: Callable[[float], float]) -> TPie:
        """
        If sort_values is specified, sets the value comparator to
        the specified function and returns this pie generator.

        Parameters
        ----------
        sort_values : Callable[[float], float]
            Value input

        Returns
        -------
        Pie
            Itself
        """
        self._sort_values = sort_values
        self._sort = None
        return self

    def set_sort(self, sort: Callable[[float], float]) -> TPie:
        """
        If sort is specified, sets the data comparator to
        the specified function and returns this pie generator.

        Parameters
        ----------
        sort : Callable[[float], float]
            Sort function

        Returns
        -------
        Pie
            Itself
        """
        self._sort = sort
        self._sort_values = None
        return self

    def set_start_angle(self, start_angle: Callable[..., float] | Number) -> TPie:
        """
        If start_angle is specified, sets the overall start angle of the
        pie to the specified function or number and returns this pie generator.

        Parameters
        ----------
        start_value : Callable[[..., float]] | Number
            Start angle input

        Returns
        -------
        Pie
            Itself
        """
        if callable(start_angle):
            self._start_angle = start_angle
        else:
            self._start_angle = constant(start_angle)
        self._start_angle = argpass(self._start_angle)
        return self

    def set_end_angle(self, end_angle: Callable[..., float] | Number) -> TPie:
        """
        If end_angle is specified, sets the overall end angle
        of the pie to the specified function or number and
        returns this pie generator.

        Parameters
        ----------
        end_angle : Callable[..., float] | Number
            End angle input

        Returns
        -------
        Pie
            Itself
        """
        if callable(end_angle):
            self._end_angle = end_angle
        else:
            self._end_angle = constant(end_angle)
        self._end_angle = argpass(self._end_angle)
        return self

    def set_pad_angle(self, pad_angle: Callable[..., float] | Number) -> TPie:
        """
        If pad_angle is specified, sets the pad angle to
        the specified function or number and returns this
        pie generator.

        Parameters
        ----------
        pad_angle : Callable[..., float] | Number
            Pad angle input

        Returns
        -------
        Pie
            Itself
        """
        if callable(pad_angle):
            self._pad_angle = pad_angle
        else:
            self._pad_angle = constant(pad_angle)
        self._pad_angle = argpass(self._pad_angle)
        return self

    def get_value(self) -> Accessor[T, float]:
        return self._value

    def get_sort(self) -> Callable[[float], float]:
        return self._sort

    def get_sort_values(self) -> Callable[[float], float]:
        return self._sort_values

    def get_start_angle(self) -> Callable[..., float]:
        return self._start_angle

    def get_end_angle(self) -> Callable[..., float]:
        return self._end_angle

    def get_pad_angle(self) -> Callable[..., float]:
        return self._pad_angle
