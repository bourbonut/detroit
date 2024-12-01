from .exponent import exponent


def precision_round(step: int | float, max_val: int | float) -> int:
    """
    Returns a suggested decimal precision for format types that
    round to significant digits given the specified numeric step
    and max values. The step represents the minimum absolute difference
    between values that will be formatted, and the max represents the
    largest absolute value that will be formatted.

    Parameters
    ----------
    step : int | float
        Specific numeric value
    max_val : int | float
        The largest absolute value that will be formatted

    Returns
    -------
    int
        Decimal precision

    Examples
    --------

    >>> p = d3.precision_round(0.01, 1.01)
    >>> f = d3.format(f".{p}r")
    >>> f(0.99)
    '0.990'
    >>> f(1.0)
    '1.00'
    >>> f(1.01)
    '1.01'
    """
    step = abs(step)
    max_val = abs(max_val) - step
    return max(0, exponent(max_val) - exponent(step)) + 1
