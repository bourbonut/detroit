from .tqmt import tqmt

def ease_exp_in(t: float) -> float:
    """
    Exponential easing; raises 2 to the exponent :math:`10 \\times (t - 1)`.

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
    >>> d3.ease_exp_in(0.2)
    0.002932551319648094
    """
    return tqmt(1 - t)

def ease_exp_out(t: float) -> float:
    """
    Reverse exponential easing; equivalent to :code:`1 - d3.ease_exp_in(1 -
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
    >>> d3.ease_exp_out(0.2)
    0.750733137829912
    """
    return 1 - tqmt(t)

def ease_exp_in_out(t: float) -> float:
    """
    Symmetric exponential easing; scales :func:`d3.ease_exp_in
    <detroit.ease_exp_in>` :math:`\\forall t \\in [0, 0.5]` and
    :func:`d3.ease_exp_out <detroit.ease_exp_out>` :math:`\\forall t \\in [0.5,
    1]`. Also equivalent to :code:`d3.ease_poly.exponent(3)`.

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
    >>> d3.ease_exp_in_out(0.2)
    0.007331378299120235
    """
    t *= 2
    if t <= 1:
        return tqmt(1 - t) * 0.5
    else:
        return (2 - tqmt(t - 1)) * 0.5
