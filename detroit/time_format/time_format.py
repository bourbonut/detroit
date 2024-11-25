import locale
from collections.abc import Callable
from datetime import datetime


def time_format(specifier: str) -> Callable[[str], str]:
    """
    Returns a formatter function to change a datetime into string

    Parameters
    ----------
    specifier : str
        Specifier string

    Returns
    -------
    Callable[[str], str]
        Formatter function
    """

    def formatter(date: datetime):
        return date.strftime(specifier)

    return formatter


def time_parse(specifier: str) -> Callable[[str], datetime]:
    """
    Returns a formatter function to change a string into datetime

    Parameters
    ----------
    specifier : str
        Specifier string

    Returns
    -------
    Callable[[str], datetime]
        Formatter function
    """

    def formatter(string: str):
        return datetime.strptime(string, specifier)

    return formatter


def iso_format(date: datetime) -> str:
    """
    Formats the date into

    Parameters
    ----------
    date : datetime
        Input date

    Returns
    -------
    str
        Iso string
    """
    return date.isoformat()


def iso_parse(string: str) -> datetime:
    """
    Parses the iso string into datetime.

    Parameters
    ----------
    string : str
        Iso string

    Returns
    -------
    datetime
        Output date
    """
    return datetime.fromisoformat(string)


def time_format_locale(language: str) -> Callable[[str], Callable[[str], str]]:
    """
    Change the locale language and return a formatter function
    (see `time_format <detroit.time_format>`).

    Parameters
    ----------
    language : str
        Language

    Returns
    -------
    Callable[[str], Callable[[str], str]]

    Examples
    --------
    >>> f = time_format_locale("en_US.UTF-8")("%B %d, %Y")
    >>> f(datetime.now())
    'October 18, 2024'
    """
    locale.setlocale(locale.LC_TIME, language)

    def formatter(specifier: str):
        return time_format(specifier)

    return formatter
