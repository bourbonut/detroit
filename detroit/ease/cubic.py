def ease_cubic_in(t: float) -> float:
    """
    Cubic easing; equivalent to :code:`d3.ease_poly_in.exponent(3)`.

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
    >>> d3.ease_cubic_in(0.2)
    0.008000000000000002
    """
    return t * t * t

def ease_cubic_out(t: float) -> float:
    """
    Reverse cubic easing; equivalent to :code:`1 - d3.ease_cubic_in(1 - t)`.
    Also equivalent to :code:`d3.ease_poly_out.exponent(3)`.

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
    >>> d3.ease_cubic_out(0.2)
    0.4879999999999999
    """
    t -= 1
    return t * t * t + 1

def ease_cubic_in_out(t: float) -> float:
    """
    Symmetric cubic easing; scales :func:`d3.ease_cubic_in
    <detroit.ease_cubic_in>` :math:`\\forall t \\in [0, 0.5]` and
    :func:`d3.ease_cubic_out <detroit.ease_cubic_out>` :math:`\\forall t \\in
    [0.5, 1]`. Also equivalent to :code:`d3.ease_poly.exponent(3)`.

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
    >>> d3.ease_cubic_in_out(0.2)
    0.03200000000000001
    """
    t *= 2
    if t <= 1:
        return (t * t * t) * 0.5
    else:
        t -= 2
        return (t * t * t + 2) * 0.5
