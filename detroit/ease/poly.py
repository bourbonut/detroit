from typing import TypeVar

TPolyIn = TypeVar("PolyIn", bound="PolyIn")
TPolyOut = TypeVar("PolyOut", bound="PolyOut")
TPolyInOut = TypeVar("PolyInOut", bound="PolyInOut")

EXPONENT = 3

class PolyIn:

    def __init__(self, exponent: float):
        self._exponent = exponent

    def __call__(self, t: float) -> float:
        return pow(t, self._exponent)

    def exponent(self, exponent: float) -> TPolyIn:
        return PolyIn(exponent)

ease_poly_in = PolyIn(EXPONENT)

class PolyOut:

    def __init__(self, exponent: float):
        self._exponent = exponent

    def __call__(self, t: float) -> float:
        return 1 - pow(1 - t, self._exponent)

    def exponent(self, exponent: float) -> TPolyOut:
        return PolyOut(exponent)

ease_poly_out = PolyOut(EXPONENT)

class PolyInOut:

    def __init__(self, exponent: float):
        self._exponent = exponent

    def __call__(self, t: float) -> float:
        t *= 2
        if t <= 1:
            return pow(t, self._exponent) * 0.5
        else:
            return (2 - pow(2 - t, self._exponent)) * 0.5

    def exponent(self, exponent: float) -> TPolyInOut:
        return PolyInOut(exponent)

ease_poly_in_out = PolyInOut(EXPONENT)
