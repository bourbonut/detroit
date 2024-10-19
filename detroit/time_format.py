import locale
from datetime import datetime

def time_format(specifier: str):

    def formatter(date: datetime):
        return date.strftime(specifier)

    return formatter

def time_parse(specifier: str):

    def formatter(string: str):
        return datetime.strptime(string, specifier)

    return formatter

def iso_format(date: datetime):
    return date.isoformat()

def iso_parse(string: str):
    return datetime.fromisoformat(string)

def time_format_locale(language: str):
    """
    >>> f = time_format_locale("en_US.UTF-8")("%B %d, %Y")
    >>> f(datetime.now())
    'October 18, 2024'
    """
    locale.setlocale(locale.LC_TIME, language)

    def formatter(specifier: str):
        return time_format(specifier)

    return formatter
