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

    def __init__(self, amplitude: float, period: float):
        self._amplitude = max(1, amplitude)
        self._period = period /  TAU
        self._s = asin(1 / self._amplitude) * self._period

    def __call__(self, t: float) -> float:
        t -= 1
        return self._amplitude * tqmt(-t) * sin((self._s - t) / self._period) 

    def amplitude(self, amplitude: float) -> TElasticIn:
        return ElasticIn(amplitude, self._period * TAU)

    def period(self, period: float) -> TElasticIn:
        return ElasticIn(self._amplitude, period)

ease_elastic_in = ElasticIn(AMPLITUDE, PERIOD)

class ElasticOut:

    def __init__(self, amplitude: float, period: float):
        self._amplitude = max(1, amplitude)
        self._period = period /  TAU
        self._s = asin(1 / self._amplitude) * self._period

    def __call__(self, t: float) -> float:
        return 1 - self._amplitude * tqmt(t) * sin((t + self._s) / self._period)

    def amplitude(self, amplitude: float) -> TElasticOut:
        return ElasticOut(amplitude, self._period * TAU)

    def period(self, period: float) -> TElasticOut:
        return ElasticOut(self._amplitude, period)

ease_elastic_out = ElasticOut(AMPLITUDE, PERIOD)

class ElasticInOut:

    def __init__(self, amplitude: float, period: float):
        self._amplitude = max(1, amplitude)
        self._period = period /  TAU
        self._s = asin(1 / self._amplitude) * self._period

    def __call__(self, t: float) -> float:
        t = t * 2 - 1
        if t < 0:
            return self._amplitude * tqmt(-t) * sin((self._s - t) / self._period) * 0.5
        else:
            return (2 - self._amplitude * tqmt(t) * sin((self._s + t) / self._period)) * 0.5

    def amplitude(self, amplitude: float) -> TElasticInOut:
        return ElasticInOut(amplitude, self._period * TAU)

    def period(self, period: float) -> TElasticInOut:
        return ElasticInOut(self._amplitude, period)

ease_elastic_in_out = ElasticInOut(AMPLITUDE, PERIOD)
