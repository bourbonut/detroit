from typing import TypeVar

TPolyIn = TypeVar("PolyIn", bound="PolyIn")
TPolyOut = TypeVar("PolyOut", bound="PolyOut")
TPolyInOut = TypeVar("PolyInOut", bound="PolyInOut")

EXPONENT = 3

class PolyIn:
    """
    Polynomial easing; raises t to the specified exponent. If the
    :code:`exponent` is not specified, it defaults to :code:`3`, equivalent to
    :func:`d3.ease_cubic_in <detroit.ease_cubic_in>`.

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
    >>> d3.ease_poly_in(0.2)
    0.008000000000000002
    >>> d3.ease_poly_in.exponent(5)(0.2)
    0.0003200000000000001
    """
    def __init__(self, exponent: float):
        self._exponent = exponent

    def __call__(self, t: float) -> float:
        """
        Polynomial easing; raises t to the specified exponent. If the
        :code:`exponent` is not specified, it defaults to :code:`3`, equivalent
        to :func:`d3.ease_cubic_in <detroit.ease_cubic_in>`.

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
        >>> d3.ease_poly_in(0.2)
        0.008000000000000002
        >>> d3.ease_poly_in.exponent(5)(0.2)
        0.0003200000000000001
        """
        return pow(t, self._exponent)

    def exponent(self, exponent: float) -> TPolyIn:
        """
        Returns a new easing function with :code:`exponent` value as parameter.

        Parameters
        ----------
        exponent : float
            Exponent value

        Returns
        -------
        PolyIn
            New easing function
        """
        return PolyIn(exponent)

ease_poly_in = PolyIn(EXPONENT)

class PolyOut:
    """
    Reverse polynomial easing; equivalent to :code:`1 - d3.ease_poly_in(1 -
    t)`. If the :code:`exponent` is not specified, it defaults to :code:`3`,
    equivalent to :func:`d3.ease_cubic_out <detroit.ease_cubic_out>`.

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
    >>> d3.ease_poly_out(0.2)
    0.4879999999999999
    >>> d3.ease_poly_out.exponent(5)(0.2)
    0.6723199999999999
    """
    def __init__(self, exponent: float):
        self._exponent = exponent

    def __call__(self, t: float) -> float:
        """
        Reverse polynomial easing; equivalent to :code:`1 - d3.ease_poly_in(1 -
        t)`. If the :code:`exponent` is not specified, it defaults to
        :code:`3`, equivalent to :func:`d3.ease_cubic_out
        <detroit.ease_cubic_out>`.

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
        >>> d3.ease_poly_out(0.2)
        0.4879999999999999
        >>> d3.ease_poly_out.exponent(5)(0.2)
        0.6723199999999999
        """
        return 1 - pow(1 - t, self._exponent)

    def exponent(self, exponent: float) -> TPolyOut:
        """
        Returns a new easing function with :code:`exponent` value as parameter.

        Parameters
        ----------
        exponent : float
            Exponent value

        Returns
        -------
        PolyOut
            New easing function
        """
        return PolyOut(exponent)

ease_poly_out = PolyOut(EXPONENT)

class PolyInOut:
    """
    Symmetric polynomial easing; scales :func:`d3.ease_poly_in
    <detroit.ease_poly_in>` :math:`\\forall t \\in [0, 0.5]` and
    :func:`d3.ease_poly_out <detroit.ease_poly_out>` :math:`\\forall t \\in
    [0.5, 1]`. If the :code:`exponent` is not specified, it defaults to
    :code:`3`, equivalent to :func:`d3.ease_cubic <detroit.ease_cubic>`.

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
    >>> d3.ease_poly_in_out(0.2)
    0.03200000000000001
    >>> d3.ease_poly_in_out.exponent(5)(0.2)
    0.005120000000000001
    """
    def __init__(self, exponent: float):
        self._exponent = exponent

    def __call__(self, t: float) -> float:
        """
        Symmetric polynomial easing; scales :func:`d3.ease_poly_in
        <detroit.ease_poly_in>` :math:`\\forall t \\in [0, 0.5]` and
        :func:`d3.ease_poly_out <detroit.ease_poly_out>` :math:`\\forall t \\in
        [0.5, 1]`. If the :code:`exponent` is not specified, it defaults to
        :code:`3`, equivalent to :func:`d3.ease_cubic <detroit.ease_cubic>`.

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
        >>> d3.ease_poly_in_out(0.2)
        0.03200000000000001
        >>> d3.ease_poly_in_out.exponent(5)(0.2)
        0.005120000000000001
        """
        t *= 2
        if t <= 1:
            return pow(t, self._exponent) * 0.5
        else:
            return (2 - pow(2 - t, self._exponent)) * 0.5

    def exponent(self, exponent: float) -> TPolyInOut:
        """
        Returns a new easing function with :code:`exponent` value as parameter.

        Parameters
        ----------
        exponent : float
            Exponent value

        Returns
        -------
        PolyInOut
            New easing function
        """
        return PolyInOut(exponent)

ease_poly_in_out = PolyInOut(EXPONENT)
