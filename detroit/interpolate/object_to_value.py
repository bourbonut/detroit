# from d3_color import color
# from .rgb import rgb
from .constant import constant
from .date import interpolate_date
from .number import interpolate_number
from .string import interpolate_string
from .number_array import interpolate_number_array, is_number_array

from datetime import datetime

rgb = None

def interpolate_object(a, b):
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

def interpolate_array(a, b):
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
    if b is None or isinstance(b, bool):
        return constant(b)
    if isinstance(b, (int, float)):
        return interpolate_number(a, b)
    if isinstance(b, str):
        # c = color(b)
        # return rgb if c else string
        return interpolate_string(a, b)
    # if isinstance(b, color):
    #     return rgb
    if isinstance(b, datetime):
        return interpolate_date(a, b)
    if is_number_array(b):
        return interpolate_number_array(a, b)
    if isinstance(b, (list, tuple)):
        return generic_array(a, b)
    if isinstance(b, dict):
        return interpolate_object(a, b)
    return interpolate_number(a, b)