from typing import TypeVar
from math import pi, sin, asin
from .tqmt import tqmt

TElasticIn = TypeVar("ElasticIn", bound="ElasticIn")
TElasticOut = TypeVar("ElasticOut", bound="ElasticOut")
TElasticInOut = TypeVar("ElasticInOut", bound="ElasticInOut")

TAU = 2 * pi
AMPLITUDE = 1
PERIOD = 0.3

class ElasticIn:
    """
    Elastic easing, like a rubber band.

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
    >>> d3.ease_elastic_in(0.2)
    -0.0014662756598240474
    >>> d3.ease_elastic_in.amplitude(2)(0.2)
    -0.005865102639296188
    >>> d3.ease_elastic_in.period(0.5)(0.2)
    -0.0023724838544719874
    >>> d3.ease_elastic_in.amplitude(2).period(0.5)(0.2)
    -0.00535803787473666
    """
    def __init__(self, amplitude: float, period: float):
        self._amplitude = max(1, amplitude)
        self._period = period /  TAU
        self._s = asin(1 / self._amplitude) * self._period

    def __call__(self, t: float) -> float:
        """
        Elastic easing, like a rubber band.

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
        >>> d3.ease_elastic_in(0.2)
        -0.0014662756598240474
        >>> d3.ease_elastic_in.amplitude(2)(0.2)
        -0.005865102639296188
        >>> d3.ease_elastic_in.period(0.5)(0.2)
        -0.0023724838544719874
        >>> d3.ease_elastic_in.amplitude(2).period(0.5)(0.2)
        -0.00535803787473666
        """
        t -= 1
        return self._amplitude * tqmt(-t) * sin((self._s - t) / self._period) 

    def amplitude(self, amplitude: float) -> TElasticIn:
        """
        Returns a new easing function with :code:`amplitude` value as
        parameter.

        Parameters
        ----------
        amplitude : float
            Amplitude value

        Returns
        -------
        ElasticIn
            New easing function
        """
        return ElasticIn(amplitude, self._period * TAU)

    def period(self, period: float) -> TElasticIn:
        """
        Returns a new easing function with :code:`period` value as parameter.

        Parameters
        ----------
        period : float
            Amplitude value

        Returns
        -------
        ElasticIn
            New easing function
        """
        return ElasticIn(self._amplitude, period)

ease_elastic_in = ElasticIn(AMPLITUDE, PERIOD)

class ElasticOut:
    """
    Reverse elastic easing; equivalent to :code:`1 - d3.elastic_in(1 - t)`.

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
    >>> d3.ease_elastic_out(0.2)
    1.1246334310850439
    >>> d3.ease_elastic_out.amplitude(2)(0.2)
    1.498533724340176
    >>> d3.ease_elastic_out.period(0.5)(0.2)
    1.2016611276301188
    >>> d3.ease_elastic_out.amplitude(2).period(0.5)(0.2)
    0.9478890359076215
    """
    def __init__(self, amplitude: float, period: float):
        self._amplitude = max(1, amplitude)
        self._period = period /  TAU
        self._s = asin(1 / self._amplitude) * self._period

    def __call__(self, t: float) -> float:
        """
        Reverse elastic easing; equivalent to :code:`1 - d3.elastic_in(1 - t)`.

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
        >>> d3.ease_elastic_out(0.2)
        1.1246334310850439
        >>> d3.ease_elastic_out.amplitude(2)(0.2)
        1.498533724340176
        >>> d3.ease_elastic_out.period(0.5)(0.2)
        1.2016611276301188
        >>> d3.ease_elastic_out.amplitude(2).period(0.5)(0.2)
        0.9478890359076215
        """
        return 1 - self._amplitude * tqmt(t) * sin((t + self._s) / self._period)

    def amplitude(self, amplitude: float) -> TElasticOut:
        """
        Returns a new easing function with :code:`amplitude` value as
        parameter.

        Parameters
        ----------
        amplitude : float
            Amplitude value

        Returns
        -------
        ElasticOut
            New easing function
        """
        return ElasticOut(amplitude, self._period * TAU)

    def period(self, period: float) -> TElasticOut:
        """
        Returns a new easing function with :code:`period` value as parameter.

        Parameters
        ----------
        period : float
            Amplitude value

        Returns
        -------
        ElasticOut
            New easing function
        """
        return ElasticOut(self._amplitude, period)

ease_elastic_out = ElasticOut(AMPLITUDE, PERIOD)

class ElasticInOut:
    """
    Symmetric elastic easing; scales :func:`d3.ease_elastic_in
    <detroit.ease_elastic_in>` :math:`\\forall t \\in [0, 0.5]` and
    :func:`d3.ease_elastic_out <detroit.ease_elastic_out>` :math:`\\forall t
    \\in [0.5, 1]`.

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
    >>> d3.ease_elastic_in_out(0.2)
    0.007331378299120235
    >>> d3.ease_elastic_in_out.amplitude(2)(0.2)
    0.007331378299120243
    >>> d3.ease_elastic_in_out.period(0.5)(0.2)
    0.002265520486619852
    >>> d3.ease_elastic_in_out.amplitude(2).period(0.5)(0.2)
    0.014342340186712696
    """
    def __init__(self, amplitude: float, period: float):
        self._amplitude = max(1, amplitude)
        self._period = period /  TAU
        self._s = asin(1 / self._amplitude) * self._period

    def __call__(self, t: float) -> float:
        """
        Symmetric elastic easing; scales :func:`d3.ease_elastic_in
        <detroit.ease_elastic_in>` :math:`\\forall t \\in [0, 0.5]` and
        :func:`d3.ease_elastic_out <detroit.ease_elastic_out>` :math:`\\forall
        t \\in [0.5, 1]`.

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
        >>> d3.ease_elastic_in_out(0.2)
        0.007331378299120235
        >>> d3.ease_elastic_in_out.amplitude(2)(0.2)
        0.007331378299120243
        >>> d3.ease_elastic_in_out.period(0.5)(0.2)
        0.002265520486619852
        >>> d3.ease_elastic_in_out.amplitude(2).period(0.5)(0.2)
        0.014342340186712696
        """
        t = t * 2 - 1
        if t < 0:
            return self._amplitude * tqmt(-t) * sin((self._s - t) / self._period) * 0.5
        else:
            return (2 - self._amplitude * tqmt(t) * sin((self._s + t) / self._period)) * 0.5

    def amplitude(self, amplitude: float) -> TElasticInOut:
        """
        Returns a new easing function with :code:`amplitude` value as
        parameter.

        Parameters
        ----------
        amplitude : float
            Amplitude value

        Returns
        -------
        ElasticInOut
            New easing function
        """
        return ElasticInOut(amplitude, self._period * TAU)

    def period(self, period: float) -> TElasticInOut:
        """
        Returns a new easing function with :code:`period` value as parameter.

        Parameters
        ----------
        period : float
            Amplitude value

        Returns
        -------
        ElasticInOut
            New easing function
        """
        return ElasticInOut(self._amplitude, period)

ease_elastic_in_out = ElasticInOut(AMPLITUDE, PERIOD)
