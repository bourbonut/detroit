from .exponent import exponent
from .format_group import format_group
from .format_numerals import format_numerals
from .format_specifier import format_specifier
from .format_trim import format_trim
from .format_types import format_types
from .format_prefix_auto import prefix_exponent
from .identity import identity

import math

prefixes = ["y", "z", "a", "f", "p", "n", "µ", "m", "", "k", "M", "G", "T", "P", "E", "Z", "Y"]

class Locale:
    def __init__(self, locale_def):
        self.group = (
            format_group(locale_def["grouping"], locale_def["thousands"])
            if "grouping" in locale_def and "thousands" in locale_def
            else identity
        )
        self.currency_prefix = locale_def.get("currency", "")
        self.currency_suffix = locale_def.get("currency", "")
        self.decimal = locale_def.get("decimal", ".")
        self.numerals = format_numerals(list(map(str, locale_def['numerals']))) if "numerals" in locale_def else identity
        self.percent = locale_def.get("percent", "%")
        self.minus = locale_def.get("minus", "-")
        self.nan = locale_def.get('nan', "NaN")

    def format(self, specifier):
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

        prefix = (self.currency_prefix if symbol == "$" 
                 else "0" + type_.lower() if symbol == "#" and type_.lower() in "box" 
                 else "")
        suffix = (self.currency_suffix if symbol == "$" 
                 else self.percent if type_ in "%p" 
                 else "")

        format_type = format_types[type_]
        maybe_suffix = type_ in "defgprs%"

        if precision is None:
            precision = 6
        elif type_ in "gprs":
            precision = max(1, min(21, precision))
        else:
            precision = max(0, min(20, precision))

        class Format:

            def __init__(self, prefix, suffix, group, numerals, minus, decimal):
                self.prefix = prefix
                self.suffix = suffix
                self.group = group
                self.numerals = numerals
                self.minus = minus
                self.decimal = decimal

            def __call__(self, value):
                if type_ == "c":
                    value_suffix = format_type(value) + self.suffix
                    value = ""
                else:
                    value = float(value)
                    value_negative = not(value != 0. and value >= 0. and 1 / value >= 0)

                    value = self.nan if math.isnan(value) else format_type(abs(value), precision)

                    if trim:
                        value = format_trim(value)

                    if value_negative and float(value) == 0 and sign != "+":
                        value_negative = False

                    value_prefix = ((sign if sign == "(" else self.minus) if value_negative 
                                  else ("" if sign in "-(" else sign)) + self.prefix
                    value_suffix = (prefixes[8 + prefix_exponent // 3] if type_ == "s" else "") + self.suffix
                    value_suffix += ")" if value_negative and sign == "(" else ""

                    if maybe_suffix:
                        for i, c in enumerate(value):
                            if not c.isdigit():
                                if c == ".":
                                    value_suffix = self.decimal + value[i + 1:] + value_suffix
                                else:
                                    value_suffix = value[i:] + value_suffix
                                value = value[:i]
                                break

                if comma and not zero:
                    value = self.group(value, math.inf)

                length = len(value_prefix) + len(value) + len(value_suffix)
                padding = fill * (width - length) if width and length < width else ""

                if comma and zero:
                    value = self.group(padding + value, 
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

                return self.numerals(value)

            def __str__(self):
                return str(specifier)

        return Format(prefix, suffix, self.group, self.numerals, self.minus, self.decimal)

    def format_prefix(self, specifier, value):
        specifier = format_specifier(specifier)
        specifier.type = "f"
        f = self.format(specifier)
        e = max(-8, min(8, exponent(value) // 3)) * 3
        k = 10 ** -e
        prefix = prefixes[8 + e // 3]
        
        def format_with_prefix(value):
            return f(k * value) + prefix
        
        return format_with_prefix