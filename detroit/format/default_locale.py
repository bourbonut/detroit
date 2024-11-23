from .locale import Locale
from .format_specifier import format_specifier, FormatSpecifier

locale = Locale({
    "thousands": ",",
    "grouping": [3],
    "currency": ["$", ""]
})

def locale_format(specifier: str):
    if not isinstance(specifier, FormatSpecifier):
        specifier = format_specifier(specifier)
    return locale.format(specifier)

format_prefix = locale.format_prefix
