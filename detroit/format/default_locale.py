from .locale import Locale

locale = Locale({"thousands": ",", "grouping": [3], "currency": ["$", ""]})

locale_format = locale.format
format_prefix = locale.format_prefix


def format_default_locale(definition: dict) -> Locale:
    """
    Equivalent to :code:`d3.format`, except it returns a new
    :code:`Locale` with :code:`locale.format` and
    :code:`locale.format_prefix`

    Parameters
    ----------
    definition : dict
        Definition (todo : add more explanations)

    Returns
    -------
    Locale
        Locale with definition parameters
    """
    return Locale(definition)
