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
    "x": lambda x: hex(round(x))[2:],
}
