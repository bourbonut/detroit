def ease_quad_in(t: float) -> float:
    """
    Quadratic easing; equivalent to :code:`d3.ease_poly_in.exponent(2)`.

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
    >>> d3.ease_quad_in(0.2)
    0.04000000000000001
    """
    return t * t

def ease_quad_out(t: float) -> float:
    """
    Reverse quadratic easing; equivalent to :code:`1 - d3.ease_quad_in(1 - t)`.
    Also equivalent to :code:`d3.ease_poly_out.exponent(2)`.

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
    >>> d3.ease_quad_out(0.2)
    0.36000000000000004
    """
    return t * (2 - t)

def ease_quad_in_out(t: float) -> float:
    """
    Symmetric quadratic easing; scales :func:`d3.ease_quad_in
    <detroit.ease_quad_in>` :math:`\\forall t \\in [0, 0.5]` and
    :func:`d3.ease_quad_out <detroit.ease_quad_out>` :math:`\\forall t \\in
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
    >>> d3.ease_quad_in_out(0.2)
    0.08000000000000002
    """
    t *= 2
    if t <= 1:
        return t * t * 0.5
    else:
        t -= 1
        return (t * (2 - t) + 1) * 0.5
