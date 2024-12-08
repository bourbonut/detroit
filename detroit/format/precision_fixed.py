from .exponent import exponent


def precision_fixed(step: int | float) -> int:
    """
    Returns a suggested decimal precision for fixed point
    notation given the specified numeric step value. The
    step represents the minimum absolute difference between
    values that will be formatted.

    Parameters
    ----------
    step : int | float


    Returns
    -------
    int
        Decimal precision

    Examples
    --------

    >>> p = d3.precision_fixed(0.5)
    >>> f = d3.format(f".{p}f")
    >>> f(1)
    '1.0'
    >>> f(1.5)
    '1.5'
    >>> f(2)
    '2.0'
    """
    return max(0, -exponent(abs(step)))
