from .exponent import exponent


def precision_prefix(step: int | float, value: int | float) -> int:
    """
    Returns a suggested decimal precision for use with :code:`d3.format_prefix`
    given the specified numeric step and reference value. The step represents
    the minimum absolute difference between values that will be formatted,
    and value determines which SI prefix will be used.

    Parameters
    ----------
    step : int | float
        Specific numeric value
    value : int | float
        Reference value

    Returns
    -------
    int
        Decimal precision

    Examples
    --------

    >>> p = d3.precision_prefix(1e5, 1.3e6)
    >>> f = d3.format_prefix(f".{p}", 1.3e6)
    >>> f(1.1e6)
    '1.1M'
    >>> f(1.2e6)
    '1.2M'
    >>> f(1.3e6)
    '1.3M'
    """
    return max(0, max(-8, min(8, exponent(value) // 3)) * 3 - exponent(abs(step)))
