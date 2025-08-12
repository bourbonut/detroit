from collections.abc import Callable
from datetime import datetime

from ..color.color import Color, color
from ..types import T, U, V
from .constant import constant
from .date import interpolate_date
from .number import interpolate_number
from .number_array import interpolate_number_array, is_number_array
from .rgb import interpolate_rgb
from .string import interpolate_string


def interpolate_object(a: dict[U, V], b: dict[U, V]) -> Callable[[float], dict[U, V]]:
    """
    Returns an interpolator between the two objects a and b.

    Parameters
    ----------
    a : dict[U, V]
        Object a
    b : dict[U, V]
        Object b

    Returns
    -------
    Callable[[float], dict[U, V]]
        Interpolator function

    Examples
    --------

    >>> interpolator = d3.interpolate_object({"a": [0, 10, 20]}, {"a": [30, 40, 50]})
    >>> interpolator(0)
    {'a': [0, 10, 20]}
    >>> interpolator(1)
    {'a': [30, 40, 50]}
    >>> interpolator(0.5)
    {'a': [15.0, 25.0, 35.0]}
    """
    i = {}
    c = {}

    if a is None or not isinstance(a, dict):
        a = {}
    if b is None or not isinstance(b, dict):
        b = {}

    for k in b:
        if k in a:
            i[k] = interpolate(a.get(k), b.get(k))
        else:
            c[k] = b.get(k)

    def local_interpolate(t):
        for k in i:
            c[k] = i[k](t)
        return c

    return local_interpolate


def interpolate_array(a: list[T], b: list[T]) -> Callable[[float], list[T]]:
    """
    Returns an interpolator between the two arrays a and b.

    Parameters
    ----------
    a : list[T]
        Array a
    b : list[T]
        Array b

    Returns
    -------
    Callable[[float], list[T]]
        Interpolator function

    Examples
    --------

    >>> interpolator = d3.interpolate_array([0, 10, 20], [30, 40, 50])
    >>> interpolator(0)
    [0, 10, 20]
    >>> interpolator(1)
    [30, 40, 50]
    >>> interpolator(0.5)
    [15.0, 25.0, 35.0]
    """
    return interpolate_number_array(a, b) if is_number_array(b) else generic_array(a, b)


def generic_array(a: list[T], b: list[T]) -> Callable[[float], T]:
    """
    Returns an interpolator between two sequences a and b where stored values
    are interpolated recursively.

    Parameters
    ----------
    a : list[T]
        a sequence
    b : list[T]
        b sequence

    Returns
    -------
    Callable[[float], T]
        Interpolator function

    Notes
    -----
    Use :func:`d3.interpolate_array <interpolate_array>` instead of this function.
    """
    nb = len(b) if b else 0
    na = min(nb, len(a)) if a else 0
    x = [interpolate(a[i], b[i]) for i in range(na)]
    c = list(b)

    def local_interpolate(t):
        for i in range(na):
            c[i] = x[i](t)
        return c

    return local_interpolate


def interpolate(a: T, b: T) -> Callable[[float], T]:
    """
    Returns an interpolator between the two arbitrary values a and b.

    .. list-table::
        :widths: 25 75

        *   - :code:`bool`
            - Returns a constant function based on b value
        *   - :code:`int` 
            - See :func:`d3.interpolate_number <interpolate_number>`
        *   - :code:`float`
            - See :func:`d3.interpolate_number <interpolate_number>`
        *   - :code:`str`
            - See :func:`d3.interpolate_rgb <interpolate_rgb>` if string can be \
              formatted as a color else for a generic string, see \
              :func:`d3.interpolate_string <interpolate_string>`
        *   - :class:`Color <detroit.color.color.Color>`
            - See :func:`d3.interpolate_rgb <interpolate_rgb>`
        *   - :code:`datetime`
            - See :func:`d3.interpolate_date <interpolate_date>`
        *   - :code:`list[int | float]`
            - See :func:`d3.interpolate_number_array <interpolate_number_array>`
        *   - :code:`list[T] | tuple[T]`
            - Returns an interpolator which recursively interpolates based on \
              :code:`T` values
        *   - :code:`dict[U, V]`
            - See :func:`d3.interpolate_object <interpolate_object>`
        *   - :code:`Any`
            - See :func:`d3.interpolate_number <interpolate_number>`

    Parameters
    ----------
    a : T
        Left bound of the interpolator
    b : T
        Right bound of the interpolator

    Returns
    -------
    Callable[[float], T]
        Interpolator function where input should be 0 and 1 and outputs a value
        between a and b:

        .. math::

            interpolator: [0, 1] & \\longrightarrow \\mathbb [a, b] \\\\
                               x & \\longmapsto y

    Examples
    --------

    >>> interpolator = d3.interpolate(10, 20)
    >>> interpolator(0)
    10.0
    >>> interpolator(1)
    20.0
    >>> interpolator(0.5)
    15.0
    """
    if b is None or isinstance(b, bool):
        return constant(b)
    if isinstance(b, (int, float)):
        return interpolate_number(a, b)
    if isinstance(b, str):
        c = color(b)
        if c:
            b = c
            return interpolate_rgb(a, b)
        else:
            return interpolate_string(a, b)
    if isinstance(b, Color):
        return interpolate_rgb(a, b)
    if isinstance(b, datetime):
        return interpolate_date(a, b)
    if is_number_array(b):
        return interpolate_number_array(a, b)
    if isinstance(b, (list, tuple)):
        return generic_array(a, b)
    if isinstance(b, dict):
        return interpolate_object(a, b)
    return interpolate_number(a, b)
