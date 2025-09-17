def tqmt(x: float) -> float:
    """
    Returns the two power minus ten times :code:`x` scaled to :math:`[0, 1]`.

    Parameters
    ----------
    x : float
        Input value

    Returns
    -------
    float
        Two power minus ten times the input value
    """
    return (pow(2, -10 * x) - 0.0009765625) * 1.0009775171065494
