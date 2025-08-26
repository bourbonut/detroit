import math
from collections.abc import Callable

from ..array import argpass
from .exponent import exponent
from .format_group import format_group
from .format_numerals import format_numerals
from .format_prefix_auto import prefix_auto
from .format_specifier import FormatSpecifier, format_specifier
from .format_trim import format_trim
from .format_types import format_types
from .identity import identity

prefixes = [
    "y",
    "z",
    "a",
    "f",
    "p",
    "n",
    "µ",
    "m",
    "",
    "k",
    "M",
    "G",
    "T",
    "P",
    "E",
    "Z",
    "Y",
]


class Locale:
    def __init__(self, locale_def: dict):
        self.group = (
            format_group(locale_def["grouping"], locale_def["thousands"])
            if "grouping" in locale_def and "thousands" in locale_def
            else identity
        )
        self.currency_prefix = locale_def.get("currency", ["", ""])[0]
        self.currency_suffix = locale_def.get("currency", ["", ""])[1]
        self.decimal = locale_def.get("decimal", ".")
        self.numerals = (
            format_numerals(list(map(str, locale_def["numerals"])))
            if "numerals" in locale_def
            else identity
        )
        self.percent = locale_def.get("percent", "%")
        self.minus = locale_def.get("minus", "-")
        self.nan = locale_def.get("nan", "NaN")

    def format(self, specifier: str) -> Callable[[int | float], str]:
        """
        Returns a new format function for the given string specifier.
        The returned function takes a number as the only argument, and
        returns a string representing the formatted number.
        The general form of a specifier is:

        .. code::
            
            [[fill]align][sign][symbol][0][width][,][.precision][~][type]

        The :code:`fill` can be any character.
        The presence of a fill character is signaled by the
        align character following it, which must be one of the following:

        * :code:`>` - Forces the field to be right-aligned within the available space. (Default behavior).
        * :code:`<` - Forces the field to be left-aligned within the available space.
        * :code:`^` - Forces the field to be centered within the available space.
        * :code:`=` - like :code:`>`, but with any sign and symbol to the left of any padding.

        The :code:`sign` can be:

        * :code:`-` - nothing for zero or positive and a minus sign for negative. (Default behavior.)
        * :code:`+` - a plus sign for zero or positive and a minus sign for negative.
        * :code:`(` - nothing for zero or positive and parentheses for negative.
        * (space) - a space for zero or positive and a minus sign for negative.

        The :code:`symbol` can be:

        * :code:`$` - apply currency symbols per the locale definition.
        * :code:`#` - for binary, octal, or hexadecimal notation, \
        prefix by :code:`0b`, :code:`0o`, or :code:`0x`, respectively.

        The zero (:code:`0`) option enables zero-padding; this implicitly sets :code:`fill`
        to :code:`0` and align to :code:`=`. The width defines the minimum field width; if
        not specified, then the width will be determined by the content.
        The comma (:code:`,`) option enables the use of a group separator, such
        as a comma for thousands.


        The available :code:`type` values are:

        * :code:`e` - exponent notation.
        * :code:`f` - fixed point notation.
        * :code:`g` - either decimal or exponent notation, rounded to significant digits.
        * :code:`r` - decimal notation, rounded to significant digits.
        * :code:`s` - decimal notation with an SI prefix, rounded to significant digits.
        * :code:`%` - multiply by 100, and then decimal notation with a percent sign.
        * :code:`p` - multiply by 100, round to significant digits, and then decimal notation with a percent sign.
        * :code:`b` - binary notation, rounded to integer.
        * :code:`o` - octal notation, rounded to integer.
        * :code:`d` - decimal notation, rounded to integer.
        * :code:`x` - hexadecimal notation, using lower-case letters, rounded to integer.
        * :code:`X` - hexadecimal notation, using upper-case letters, rounded to integer.
        * :code:`c` - character data, for a string of text.

        Depending on the type, the precision either indicates the number of digits
        that follow the decimal point (types f and %), or the number of significant digits
        (types (space), :code:`e`, :code:`g`, :code:`r`, :code:`s` and :code:`p`). If the
        precision is not specified, it defaults to 6 for all types except (space) (none),
        which defaults to 12. Precision is ignored for integer formats (types :code:`b`,
        :code:`o`, :code:`d`, :code:`x`, and :code:`X`) and character data (type :code:`c`)

        The :code:`~` option trims insignificant trailing zeros across all format types.
        This is most commonly used in conjunction with types :code:`r`, :code:`e`, :code:`s` and :code:`%`.

        Parameters
        ----------
        specifier : str
            Specifier

        Returns
        -------
        Callable[[int | float], str]
            Format function

        Examples
        --------

        >>> d3.format(".0%")(0.123) # rounded percentage
        '12%'
        >>> d3.format("+20")(42) # space-filled and signed
        '                 +42'
        >>> d3.format(".^20")(42) # dot-filled and centered
        '.........42.........'
        >>> d3.format(".2s")(42e6) # SI-prefix with two significant digits
        '42M'
        >>> d3.format("#x")(48879) # prefixed lowercase hexadecimal
        '0xbeef'
        >>> d3.format(",.2r")(4223) # grouped thousands with two significant digits
        '4,200'
        >>> d3.format("s")(1500)
        '1.50000k'
        >>> d3.format("~s")(1500)
        '1.5k'
        >>> d3.format(".2")(42)
        '42'
        >>> d3.format(".2")(4.2)
        '4.2'
        >>> d3.format(".1")(42)
        '4e+01'
        >>> d3.format(".1")(4.2)
        '4'
        """
        if not isinstance(specifier, FormatSpecifier):
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

        prefix = (
            self.currency_prefix
            if symbol == "$"
            else "0" + type_.lower()
            if symbol == "#" and type_.lower() in "box"
            else ""
        )
        suffix = (
            self.currency_suffix
            if symbol == "$"
            else self.percent
            if type_ in "%p"
            else ""
        )

        format_type = argpass(format_types[type_])
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
                value_prefix = self.prefix
                value_suffix = self.suffix

                if type_ == "c":
                    value_suffix = format_type(value, None) + self.suffix
                    value = ""
                else:
                    value = float(value)
                    value_negative = value < 0 or (value != 0 and 1 / value < 0)

                    value = (
                        self.nan
                        if math.isnan(value)
                        else format_type(abs(value), precision)
                    )

                    if trim:
                        value = format_trim(value)

                    if value_negative and sign != "+" and str(value) in ("0", "0."):
                        value_negative = False

                    if value_negative:
                        value_prefix = sign if sign == "(" else self.minus
                    elif sign == "-" or sign == "(":
                        value_prefix = ""
                    else:
                        value_prefix = sign

                    value_prefix += self.prefix

                    if type_ == "s":
                        value_suffix = prefixes[8 + prefix_auto.prefix_exponent // 3]
                    else:
                        value_suffix = ""

                    value_suffix += self.suffix
                    value_suffix += ")" if value_negative and sign == "(" else ""

                    if maybe_suffix:
                        for i, c in enumerate(value):
                            if not c.isdigit():
                                if c == ".":
                                    value_suffix = (
                                        self.decimal + value[i + 1 :] + value_suffix
                                    )
                                else:
                                    value_suffix = value[i:] + value_suffix
                                value = value[:i]
                                break

                if comma and not zero:
                    value = self.group(value, math.inf)

                length = len(value_prefix) + len(value) + len(value_suffix)
                padding = fill * (width - length) if width and length < width else ""

                if comma and zero:
                    value = self.group(
                        padding + value,
                        width - len(value_suffix) if len(padding) else math.inf,
                    )
                    padding = ""

                if align == "<":
                    value = value_prefix + value + value_suffix + padding
                elif align == "=":
                    value = value_prefix + padding + value + value_suffix
                elif align == "^":
                    length = len(padding) >> 1
                    value = (
                        padding[:length]
                        + value_prefix
                        + value
                        + value_suffix
                        + padding[length:]
                    )
                else:
                    value = padding + value_prefix + value + value_suffix

                return self.numerals(value)

            def __str__(self):
                return str(specifier)

        return Format(
            prefix, suffix, self.group, self.numerals, self.minus, self.decimal
        )

    def format_prefix(
        self, specifier: str, value: int | float
    ) -> Callable[[int | float], str]:
        """
        Equivalent to :code:`d3.format`, except the returned function will
        convert values to the units of the appropriate SI prefix for the
        specified numeric reference value before formatting in fixed point notation.
        The following prefixes are supported:

        * :code:`y` - yocto, :math:`10^{-24}`
        * :code:`z` - zepto, :math:`10^{-21}`
        * :code:`a` - atto, :math:`10^{-18}`
        * :code:`f` - femto, :math:`10^{-15}`
        * :code:`p` - pico, :math:`10^{-12}`
        * :code:`n` - nano, :math:`10^{-9}`
        * :code:`µ` - micro, :math:`10^{-6}`
        * :code:`m` - milli, :math:`10^{-3}`
        * (none) - :math:`1`
        * :code:`k` - kilo, :math:`10^{3}`
        * :code:`M` - mega, :math:`10^{6}`
        * :code:`G` - giga, :math:`10^{9}`
        * :code:`T` - tera, :math:`10^{12}`
        * :code:`P` - peta, :math:`10^{15}`
        * :code:`E` - exa, :math:`10^{18}`
        * :code:`Z` - zetta, :math:`10^{21}`
        * :code:`Y` - yotta, :math:`10^{24}`

        Parameters
        ----------
        specifier : str
            Specifier
        value : int | float
            Numeric reference

        Returns
        -------
        Callable[[int | float], str]
            Format function

        Examples
        --------
        >>> f = d3.format_prefix(",.0", 1e-6)
        >>> f(0.00042)
        '420µ'
        >>> f(0.0042)
        '4,200µ'
        """
        if not isinstance(specifier, FormatSpecifier):
            specifier = format_specifier(specifier)
        specifier.type = "f"
        f = self.format(specifier)
        e = max(-8, min(8, exponent(value) // 3)) * 3
        k = 10**-e
        prefix = prefixes[8 + e // 3]

        def format_with_prefix(value):
            return f(k * value) + prefix

        return format_with_prefix
