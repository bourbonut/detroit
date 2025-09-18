B1 = 4 / 11
B2 = 6 / 11
B3 = 8 / 11
B4 = 3 / 4
B5 = 9 / 11
B6 = 10 / 11
B7 = 15 / 16
B8 = 21 / 22
B9 = 63 / 64
B0 = 1 / B1 / B1

def ease_bounce_in(t: float) -> float:
    """
    Bounce easing, like a rubber ball.

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
    >>> d3.ease_bounce_in(0.2)
    0.06000000000000005
    """
    return 1 - ease_bounce_out(1 - t)

def ease_bounce_out(t: float) -> float:
    """
    Reverse bounce easing; equivalent to :code:`1 - ease_bounce_in(1 - t)`.

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
    >>> d3.ease_bounce_out(0.2)
    0.30250000000000005
    """
    if t < B1:
        return B0 * t * t
    elif t < B3:
        t -= B2
        return B0 * t * t + B4
    elif t < B6:
        t -= B5
        return B0 * t * t + B7
    else:
        t -= B8
        return B0 * t * t + B9

def ease_bounce_in_out(t: float) -> float:
    """
    Symmetric bounce easing; scales :func:`d3.ease_bounce_in
    <detroit.ease_bounce_in>` :math:`\\forall t \\in [0, 0.5]` and
    :func:`d3.ease_bounce_out <detroit.ease_bounce_out>` :math:`\\forall t \\in
    [0.5, 1]`.

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
    >>> d3.ease_bounce_in_out(0.2)
    0.11375000000000002
    """
    t *= 2
    if t <= 1:
        return (1 - ease_bounce_out(1 - t)) * 0.5
    else:
        return (ease_bounce_out(t - 1) + 1) * 0.5
