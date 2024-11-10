# src/format_prefix_auto.py
from .format_decimal import format_decimal_parts

prefix_exponent = None

def format_prefix_auto(x, p):
    global prefix_exponent
    d = format_decimal_parts(x, p)
    if not d:
        return str(x)
    coefficient, exponent = d
    prefix_exponent = max(-8, min(8, exponent // 3)) * 3
    i = exponent - prefix_exponent + 1
    n = len(coefficient)
    if i == n:
        return coefficient
    elif i > n:
        return coefficient + "0" * (i - n)
    elif i > 0:
        return coefficient[:i] + "." + coefficient[i:]
    else:
        return "0." + "0" * (-i) + format_decimal_parts(x, max(0, p + i - 1))[0]

# src/format_trim.py
def format_trim(s):
    n = len(s)
    i0 = -1
    i1 = 0
    for i in range(1, n):
        c = s[i]
        if c == ".":
            i0 = i1 = i
        elif c == "0":
            if i0 == 0:
                i0 = i
            i1 = i
        else:
            if not c.isdigit():
                break
            if i0 > 0:
                i0 = 0
    return s[:i0] + s[i1 + 1:] if i0 > 0 else s

# src/locale.py
from .exponent import exponent
from .format_group import format_group
from .format_numerals import format_numerals
from .format_specifier import format_specifier
from .format_trim import format_trim
from .format_types import format_types
from .format_prefix_auto import prefix_exponent
from .identity import identity

prefixes = ["y","z","a","f","p","n","µ","m","","k","M","G","T","P","E","Z","Y"]

def create_locale(locale_def):
    group = (identity if locale_def.get('grouping') is None or locale_def.get('thousands') is None 
            else format_group([float(x) for x in locale_def['grouping']], locale_def['thousands']))
    
    currency_prefix = "" if locale_def.get('currency') is None else locale_def['currency'][0]
    currency_suffix = "" if locale_def.get('currency') is None else locale_def['currency'][1]
    decimal = "." if locale_def.get('decimal') is None else locale_def['decimal']
    numerals = (identity if locale_def.get('numerals') is None 
               else format_numerals([str(x) for x in locale_def['numerals']]))
    percent = "%" if locale_def.get('percent') is None else locale_def['percent']
    minus = "−" if locale_def.get('minus') is None else locale_def['minus']
    nan = "NaN" if locale_def.get('nan') is None else locale_def['nan']

    def new_format(specifier):
        specifier = format_specifier(specifier)
        
        fill = specifier.fill
        align = specifier.align
        sign = specifier.sign
        symbol = specifier.symbol
        zero = specifier.zero
        width = specifier.width
        comma = specifier.comma
        precision = specifier.precision
        trim = specifier.trim
        type_ = specifier.type

        if type_ == "n":
            comma = True
            type_ = "g"
        elif type_ not in format_types:
            if precision is None:
                precision = 12
            trim = True
            type_ = "g"

        if zero or (fill == "0" and align == "="):
            zero = True
            fill = "0"
            align = "="

        prefix = (currency_prefix if symbol == "$" 
                 else "0" + type_.lower() if symbol == "#" and type_.lower() in "box" 
                 else "")
        suffix = (currency_suffix if symbol == "$" 
                 else percent if type_ in "%p" 
                 else "")

        format_type = format_types[type_]
        maybe_suffix = type_ in "defgprs%"

        if precision is None:
            precision = 6
        elif type_ in "gprs":
            precision = max(1, min(21, precision))
        else:
            precision = max(0, min(20, precision))

        def format_(value):
            value_prefix = prefix
            value_suffix = suffix

            if type_ == "c":
                value_suffix = format_type(value) + value_suffix
                value = ""
            else:
                value = float(value)
                value_negative = value < 0 or 1 / value < 0

                value = nan if value != value else format_type(abs(value), precision)

                if trim:
                    value = format_trim(value)

                if value_negative and float(value) == 0 and sign != "+":
                    value_negative = False

                value_prefix = ((sign if sign == "(" else minus) if value_negative 
                              else ("" if sign in "-(" else sign)) + value_prefix
                value_suffix = (prefixes[8 + prefix_exponent // 3] if type_ == "s" else "") + value_suffix
                value_suffix += ")" if value_negative and sign == "(" else ""

                if maybe_suffix:
                    for i, c in enumerate(value):
                        if not c.isdigit():
                            if c == ".":
                                value_suffix = decimal + value[i + 1:] + value_suffix
                            else:
                                value_suffix = value[i:] + value_suffix
                            value = value[:i]
                            break

            if comma and not zero:
                value = group(value, float('inf'))

            length = len(value_prefix) + len(value) + len(value_suffix)
            padding = fill * (width - length) if length < width else ""

            if comma and zero:
                value = group(padding + value, 
                            len(padding) and width - len(value_suffix) or float('inf'))
                padding = ""

            if align == "<":
                value = value_prefix + value + value_suffix + padding
            elif align == "=":
                value = value_prefix + padding + value + value_suffix
            elif align == "^":
                length = len(padding) >> 1
                value = padding[:length] + value_prefix + value + value_suffix + padding[length:]
            else:
                value = padding + value_prefix + value + value_suffix

            return numerals(value)

        format_.toString = lambda: str(specifier)
        return format_

    def format_prefix(specifier, value):
        specifier = format_specifier(specifier)
        specifier.type = "f"
        f = new_format(specifier)
        e = max(-8, min(8, exponent(value) // 3)) * 3
        k = 10 ** -e
        prefix = prefixes[8 + e // 3]
        
        def format_with_prefix(value):
            return f(k * value) + prefix
        
        return format_with_prefix

    return {
        "format": new_format,
        "formatPrefix": format_prefix
    }

# src/format_types.py
from .format_decimal import format_decimal
from .format_prefix_auto import format_prefix_auto
from .format_rounded import format_rounded

format_types = {
    "%": lambda x, p: f"{x * 100:.{p}f}",
    "b": lambda x: bin(round(x))[2:],
    "c": lambda x: str(x),
    "d": format_decimal,
    "e": lambda x, p: f"{x:.{p}e}",
    "f": lambda x, p: f"{x:.{p}f}",
    "g": lambda x, p: f"{x:.{p}g}",
    "o": lambda x: oct(round(x))[2:],
    "p": lambda x, p: format_rounded(x * 100, p),
    "r": format_rounded,
    "s": format_prefix_auto,
    "X": lambda x: hex(round(x))[2:].upper(),
    "x": lambda x: hex(round(x))[2:]
}

# src/format_numerals.py
def format_numerals(numerals):
    def replace(value):
        return ''.join(numerals[int(c)] if c.isdigit() else c for c in value)
    return replace

# src/format_rounded.py
from .format_decimal import format_decimal_parts

def format_rounded(x, p):
    d = format_decimal_parts(x, p)
    if not d:
        return str(x)
    coefficient, exponent = d
    if exponent < 0:
        return "0." + "0" * (-exponent) + coefficient
    elif len(coefficient) > exponent + 1:
        return coefficient[:exponent + 1] + "." + coefficient[exponent + 1:]
    else:
        return coefficient + "0" * (exponent - len(coefficient) + 1)

# src/format_decimal.py
def format_decimal(x):
    x = round(x)
    if abs(x) >= 1e21:
        return str(x).replace(",", "")
    return str(x)

def format_decimal_parts(x, p):
    try:
        if p is not None:
            x_str = f"{x:.{p-1}e}"
        else:
            x_str = f"{x:e}"
        
        i = x_str.find('e')
        if i < 0:
            return None  # NaN, ±Infinity
        
        coefficient = x_str[:i]
        if len(coefficient) > 1:
            coefficient = coefficient[0] + coefficient[2:]  # Remove decimal point
        
        return [coefficient, int(x_str[i+1:])]
    except (ValueError, TypeError):
        return None

# src/identity.py
def identity(x):
    return x

# src/precision_fixed.py
from .exponent import exponent

def precision_fixed(step):
    return max(0, -exponent(abs(step)))

# src/precision_prefix.py
from .exponent import exponent

def precision_prefix(step, value):
    return max(0, max(-8, min(8, exponent(value) // 3)) * 3 - exponent(abs(step)))

# src/precision_round.py
from .exponent import exponent

def precision_round(step, max_val):
    step = abs(step)
    max_val = abs(max_val) - step
    return max(0, exponent(max_val) - exponent(step)) + 1

# src/exponent.py
from .format_decimal import format_decimal_parts

def exponent(x):
    result = format_decimal_parts(abs(x), None)
    return float('nan') if result is None else result[1]

# src/format_specifier.py
import re

# [[fill]align][sign][symbol][0][width][,][.precision][~][type]
FORMAT_RE = re.compile(r'^(?:(.)?([<>=^]))?([+\-( ])?([$#])?(0)?(\d+)?(,)?(\.\d+)?(~)?([a-z%])?$', re.I)

class FormatSpecifier:
    def __init__(self, specifier):
        self.fill = " " if specifier.get('fill') is None else str(specifier['fill'])
        self.align = ">" if specifier.get('align') is None else str(specifier['align'])
        self.sign = "-" if specifier.get('sign') is None else str(specifier['sign'])
        self.symbol = "" if specifier.get('symbol') is None else str(specifier['symbol'])
        self.zero = bool(specifier.get('zero'))
        self.width = None if specifier.get('width') is None else int(specifier['width'])
        self.comma = bool(specifier.get('comma'))
        self.precision = None if specifier.get('precision') is None else int(specifier['precision'])
        self.trim = bool(specifier.get('trim'))
        self.type = "" if specifier.get('type') is None else str(specifier['type'])

    def __str__(self):
        parts = [
            self.fill,
            self.align,
            self.sign,
            self.symbol,
            "0" if self.zero else "",
            str(self.width) if self.width is not None else "",
            "," if self.comma else "",
            f".{self.precision}" if self.precision is not None else "",
            "~" if self.trim else "",
            self.type
        ]
        return "".join(parts)

def format_specifier(specifier):
    match = FORMAT_RE.match(specifier)
    if not match:
        raise ValueError(f"invalid format: {specifier}")
    
    groups = match.groups()
    return FormatSpecifier({
        'fill': groups[0],
        'align': groups[1],
        'sign': groups[2],
        'symbol': groups[3],
        'zero': groups[4],
        'width': groups[5],
        'comma': groups[6],
        'precision': groups[7][1:] if groups[7] else None,
        'trim': groups[8],
        'type': groups[9]
    })

# src/format_group.py
def format_group(grouping, thousands):
    def group(value, width):
        i = len(value)
        t = []
        j = 0
        g = grouping[0]
        length = 0

        while i > 0 and g > 0:
            if length + g + 1 > width:
                g = max(1, width - length)
            t.append(value[i-g:i])
            i -= g
            length += g + 1
            if length > width:
                break
            j = (j + 1) % len(grouping)
            g = grouping[j]

        return thousands.join(reversed(t))
    return group

# src/default_locale.py
from .locale import create_locale

locale = None
format = None
format_prefix = None

def default_locale(definition):
    global locale, format, format_prefix
    locale = create_locale(definition)
    format = locale["format"]
    format_prefix = locale["formatPrefix"]
    return locale

# Initialize with defaults
default_locale({
    "thousands": ",",
    "grouping": [3],
    "currency": ["$", ""]
})

