from math import sqrt

def ease_circle_in(t: float) -> float:
    """
    Circular easing.

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
    >>> d3.ease_circle_in(0.2)
    0.020204102886728803
    """
    return 1 - sqrt(1 - t * t)

def ease_circle_out(t: float) -> float:
    """
    Reverse circular easing; equivalent to :code:`1 - d3.ease_circle_out(1 -
    t)`.

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
    >>> d3.ease_circle_out(0.2)
    0.5999999999999999
    """
    t -= 1
    return sqrt(1 - t * t)

def ease_circle_in_out(t: float) -> float:
    """
    Symmetric circle easing; scales :func:`d3.ease_circle_in
    <detroit.ease_circle_in>` :math:`\\forall t \\in [0, 0.5]` and
    :func:`d3.ease_circle_out <detroit.ease_circle_out>` :math:`\\forall t \\in
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
    >>> d3.ease_circle_in_out(0.2)
    0.041742430504416006
    """
    t *= 2
    if t <= 1:
        return (1 - sqrt(1 - t * t)) * 0.5
    else:
        t -= 2
        return (sqrt(1 - t * t) + 1) * 0.5
