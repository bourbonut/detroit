from math import pi, cos, sin

HALF_PI = pi * 0.5

def ease_sin_in(t: float) -> float:
    """
    Sinusoidal easing; returns :code:`sin(t)`.

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
    >>> d3.ease_sin_in(0.2)
    0.04894348370484647
    """
    if t == 1:
        return 1
    else:
        return 1 - cos(t * HALF_PI)

def ease_sin_out(t: float) -> float:
    """
    Reverse sinusoidal easing; equivalent to :code:`1 - d3.ease_sin_in(1 - t)`.

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
    >>> d3.ease_sin_out(0.2)
    0.3090169943749474
    """
    return sin(t * HALF_PI)

def ease_sin_in_out(t: float) -> float:
    """
    Symmetric sinusoidal easing; scales :func:`d3.ease_sin_in
    <detroit.ease_sin_in>` :math:`\\forall t \\in [0, 0.5]` and
    :func:`d3.ease_sin_out <detroit.ease_sin_out>` :math:`\\forall t \\in
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
    >>> d3.ease_sin_in_out(0.2)
    0.09549150281252627
    """
    return (1 - cos(pi * t)) * 0.5
