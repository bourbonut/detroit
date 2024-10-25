from ..array import tick_step
from ..format import format, format_prefix, format_specifier, precision_fixed, precision_prefix, precision_round

def tick_format(start, stop, count, specifier):
    step = tick_step(start, stop, count)
    precision = None
    specifier = format_specifier(specifier if specifier is not None else ",f")

    if specifier.type == "s":
        value = max(abs(start), abs(stop))
        if specifier.precision is None and not math.isnan(precision := precision_prefix(step, value)):
            specifier.precision = precision
        return format_prefix(specifier, value)
    elif specifier.type in ("", "e", "g", "p", "r"):
        if specifier.precision is None and not math.isnan(precision := precision_round(step, max(abs(start), abs(stop)))):
            specifier.precision = precision - (specifier.type == "e")
    elif specifier.type in ("f", "%"):
        if specifier.precision is None and not math.isnan(precision := precision_fixed(step)):
            specifier.precision = precision - (specifier.type == "%") * 2

    return format(specifier)
