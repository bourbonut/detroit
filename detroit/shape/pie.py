from __future__ import annotations
from dataclasses import dataclass, asdict
from inspect import signature
from math import pi
from typing import Any
from collections.abc import Iterable, Callable

from .constant import constant

def identity(x):
    return x


@dataclass
class Arc:
    data: float
    index: int
    value: float
    start_angle: float
    end_angle: float
    pad_angle: float


class Pie:
    """
    The pie generator computes the necessary angles to represent a tabular
    dataset as a pie or donut chart; these angles can then be passed to an
    arc generator. (The pie generator does not produce a shape directly.)
    """
    def __init__(self):
        self._value = identity
        self._sort_values = lambda x: -x
        self._sort = None
        self._start_angle = constant(0)
        self._end_angle = constant(2 * pi)
        self._pad_angle = constant(0)

    def __call__(self, data: Iterable, *args: Any) -> list[dict]:
        """
        Generates a pie for the given array of data, returning an array of
        objects representing each datum's arc angles.

        Parameters
        ----------
        data : Iterable
            Data input
        *args : Any
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

        nargs_sa = len(signature(self._start_angle).parameters)
        nargs_ea = len(signature(self._end_angle).parameters)
        nargs_pa = len(signature(self._pad_angle).parameters)
        nargs_v = len(signature(self._value).parameters)

        args_sa = args[:nargs_sa]
        args_ea = args[:nargs_ea]
        args_pa = args[:nargs_pa]

        sum = 0
        index = [None] * n
        arcs = [None] * n
        a0 = self._start_angle(*args_sa)
        da = min(2 * pi, max(-2 * pi, self._end_angle(*args_ea) - a0))
        p = min(abs(da) / n, self._pad_angle(*args_pa))
        pa = p * (-1 if da < 0 else 1)

        for i in range(n):
            d = data[i]
            args = [d, i, data][:nargs_v]
            v = self._value(*args)
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

    def value(self, value: Callable | int | float) -> Pie:
        """
        If value is specified, sets the value accessor to the
        specified function or number and returns this pie generator.

        Parameters
        ----------
        value : Callable | int | float
            Value input

        Returns
        -------
        Pie
            Itself
        """
        if callable(value):
            self._value = value
        else:
            self._value = constant(value)
        return self

    def sort_values(self, sort_values: Callable) -> Pie:
        """
        If sort_values is specified, sets the value comparator to
        the specified function and returns this pie generator.

        Parameters
        ----------
        sort_values : Callable | int | float
            Value input

        Returns
        -------
        Pie
            Itself
        """
        self._sort_values = sort_values
        self._sort = None
        return self

    def sort(self, sort: Callable) -> Pie:
        """
        If sort is specified, sets the data comparator to
        the specified function and returns this pie generator.

        Parameters
        ----------
        sort : Callable
            Sort function

        Returns
        -------
        Pie
            Itself
        """
        self._sort = sort
        self._sort_values = None
        return self

    def start_angle(self, start_angle: Callable | int | float) -> Pie:
        """
        If start_angle is specified, sets the overall start angle of the
        pie to the specified function or number and returns this pie generator.

        Parameters
        ----------
        start_value : Callable | int | float
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
        return self

    def end_angle(self, end_angle: Callable | int | float) -> Pie:
        """
        If end_angle is specified, sets the overall end angle
        of the pie to the specified function or number and
        returns this pie generator.

        Parameters
        ----------
        end_angle : Callable | int | float
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
        return self

    def pad_angle(self, pad_angle: Callable | int | float) -> Pie:
        """
        If pad_angle is specified, sets the pad angle to
        the specified function or number and returns this
        pie generator.

        Parameters
        ----------
        pad_angle : Callable | int | float
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
        return self
