from d3_color import color
from .rgb import rgb
from .array import genericArray
from .date import date
from .number import number
from .object import object_interpolator
from .string import string
from .constant import constant
from .numberArray import numberArray, isNumberArray

def value(a, b):
    if b is None or isinstance(b, bool):
        return constant(b)
    if isinstance(b, (int, float)):
        return number
    if isinstance(b, str):
        c = color(b)
        return rgb if c else string
    if isinstance(b, color):
        return rgb
    if isinstance(b, datetime.date):
        return date
    if isNumberArray(b):
        return numberArray
    if isinstance(b, (list, tuple)):
        return genericArray
    if not hasattr(b, 'valueOf') and not hasattr(b, '__str__') or math.isnan(b):
        return object_interpolator
    return number
