from typing import TypeVar

TBackIn = TypeVar("BackIn", bound="BackIn")
TBackOut = TypeVar("BackOut", bound="BackOut")
TBackInOut = TypeVar("BackInOut", bound="BackInOut")

OVERSHOOT = 1.70158

class BackIn:
    """
    Anticipatory easing like a dancer bending her knees before jumping off the
    floor.

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
    >>> d3.ease_back_in(0.2)
    -0.04645056000000002
    >>> d3.ease_back_in.overshoot(1.5)(0.2)
    -0.040000000000000015
    """
    def __init__(self, overshoot: float):
        self._overshoot = overshoot

    def __call__(self, t: float) -> float:
        """
        Anticipatory easing like a dancer bending her knees before jumping off
        the floor.

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
        >>> d3.ease_back_in(0.2)
        -0.04645056000000002
        >>> d3.ease_back_in.overshoot(1.5)(0.2)
        -0.040000000000000015
        """
        return t * t * (self._overshoot * (t - 1) + t)

    def overshoot(self, overshoot: float) -> TBackIn:
        """
        Returns a new easing function with :code:`overshoot` value as
        parameter.

        Parameters
        ----------
        overshoot : float
            Overshoot value

        Returns
        -------
        BackIn
            New easing function
        """
        return BackIn(overshoot)

ease_back_in = BackIn(OVERSHOOT)

class BackOut:
    """
    Reverse anticipatory easing; equivalent to :code:`1 - d3.ease_back_in(1
    - t)`.

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
    >>> d3.ease_back_out(0.2)
    0.7058022399999999
    >>> d3.ease_back_out.overshoot(1.5)(0.2)
    0.6799999999999999
    """
    def __init__(self, overshoot: float):
        self._overshoot = overshoot

    def __call__(self, t: float) -> float:
        """
        Reverse anticipatory easing; equivalent to :code:`1 - d3.ease_back_in(1
        - t)`.

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
        >>> d3.ease_back_out(0.2)
        0.7058022399999999
        >>> d3.ease_back_out.overshoot(1.5)(0.2)
        0.6799999999999999
        """
        t -= 1
        return t * t * ((t + 1) * self._overshoot + t) + 1

    def overshoot(self, overshoot: float) -> TBackOut:
        """
        Returns a new easing function with :code:`overshoot` value as
        parameter.

        Parameters
        ----------
        overshoot : float
            Overshoot value

        Returns
        -------
        BackOut
            New easing function
        """
        return BackOut(overshoot)

ease_back_out = BackOut(OVERSHOOT)

class BackInOut:
    """
    Symmetric anticipatory easing; scales :func:`d3.ease_back_in
    <detroit.ease_back_in>` :math:`\\forall t \\in [0, 0.5]` and
    :func:`d3.ease_back_out <detroit.ease_back_out>` :math:`\\forall t \\in
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
    >>> d3.ease_back_in_out(0.2)
    -0.04967584000000001
    >>> d3.ease_back_in_out.overshoot(1.5)(0.2)
    -0.04000000000000001
    """
    def __init__(self, overshoot: float):
        self._overshoot = overshoot

    def __call__(self, t: float) -> float:
        """
        Symmetric anticipatory easing; scales :func:`d3.ease_back_in
        <detroit.ease_back_in>` :math:`\\forall t \\in [0, 0.5]` and
        :func:`d3.ease_back_out <detroit.ease_back_out>` :math:`\\forall t \\in
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
        >>> d3.ease_back_in_out(0.2)
        -0.04967584000000001
        >>> d3.ease_back_in_out.overshoot(1.5)(0.2)
        -0.04000000000000001
        """
        t *= 2
        if t < 1:
            return t * t * ((self._overshoot + 1) * t - self._overshoot) * 0.5
        else:
            t -= 2
            return (t * t * ((self._overshoot + 1) * t + self._overshoot) + 2) * 0.5

    def overshoot(self, overshoot: float) -> TBackInOut:
        """
        Returns a new easing function with :code:`overshoot` value as
        parameter.

        Parameters
        ----------
        overshoot : float
            Overshoot value

        Returns
        -------
        BackInOut
            New easing function
        """
        return BackInOut(overshoot)

ease_back_in_out = BackInOut(OVERSHOOT)
