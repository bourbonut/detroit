def ease_linear(t: float) -> float:
    """
    Linear easing; the identity function; :code:`d3.ease_linear(t)` returns
    :code:`t`.

    Parameters
    ----------
    t : float
        :math:`t \\in [0, 1]`

    Returns
    -------
    float
        Output value of the easing function

    Examples
    --------
    >>> d3.ease_linear(0.2)
    0.2
    """
    return t
