from .locale import Locale

locale = Locale({
    "thousands": ",",
    "grouping": [3],
    "currency": ["$", ""]
})
locale_format = locale.format
format_prefix = locale.format_prefix