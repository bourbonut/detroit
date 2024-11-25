from collections.abc import Callable
from datetime import datetime

from ..coloration.color import Color, color
from .constant import constant
from .date import interpolate_date
from .number import interpolate_number
from .number_array import interpolate_number_array, is_number_array
from .rgb import interpolate_rgb
from .string import interpolate_string


def interpolate_object(a, b) -> Callable:
    """
    Returns an interpolator between the two objects a and b.

    Returns
    -------
    Callable
        Interpolator
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


def interpolate_array(a: list, b: list) -> Callable:
    """
    Returns an interpolator between the two arrays a and b.

    Parameters
    ----------
    a : list
        Array a
    b : list
        Array b

    Returns
    -------
    Callable
        Interpolator
    """
    return interpolate_number_array(a, b) if is_number_array(b) else generic_array(a, b)


def generic_array(a, b):
    nb = len(b) if b else 0
    na = min(nb, len(a)) if a else 0
    x = [interpolate(a[i], b[i]) for i in range(na)]
    c = list(b)

    def local_interpolate(t):
        for i in range(na):
            c[i] = x[i](t)
        return c

    return local_interpolate


def interpolate(a, b):
    """
    Returns an interpolator between the two arbitrary values a and b.
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
