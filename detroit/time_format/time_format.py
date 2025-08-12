import locale
from collections.abc import Callable
from datetime import datetime

from ..types import Formatter


def time_format(specifier: str) -> Formatter[str]:
    """
    Returns a formatter function to change a datetime into string

    Parameters
    ----------
    specifier : str
        Specifier string

    Returns
    -------
    Formatter[str]
        Formatter function which returns a string

    Examples
    --------

    >>> from datetime import datetime
    >>> d = datetime(2004, 6, 8, 12, 10)
    >>> d3.time_format("%Y")(d)
    '2004'
    """

    def formatter(date: datetime):
        return date.strftime(specifier)

    return formatter


def time_parse(specifier: str) -> Formatter[datetime]:
    """
    Returns a formatter function to change a string into datetime

    Parameters
    ----------
    specifier : str
        Specifier string

    Returns
    -------
    Formatter[datetime]
        Formatter function which returns a datetime

    Examples
    --------

    >>> d3.time_parse("%Y")("2004")
    datetime.datetime(2004, 1, 1, 0, 0)
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

    Examples
    --------

    >>> from datetime import datetime
    >>> d = datetime(2004, 6, 8, 12, 10)
    >>> d3.iso_format(d)
    '2004-06-08T12:10:00'
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

    Examples
    --------

    >>> d3.iso_parse('2004-06-08T12:10:00')
    datetime.datetime(2004, 6, 8, 12, 10)
    """
    return datetime.fromisoformat(string)


def time_format_locale(language: str) -> Callable[[str], Formatter[str]]:
    """
    Change the locale language and return a formatter function
    (see :func:`d3.time_format <time_format>`).

    Parameters
    ----------
    language : str
        Language

    Returns
    -------
    Callable[[str], Formatter[str]]
        Function which takes a specifier string and returns a formatter function
        which itself returns a string

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
