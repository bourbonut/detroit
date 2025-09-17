from typing import TypeVar

TBackIn = TypeVar("BackIn", bound="BackIn")
TBackOut = TypeVar("BackOut", bound="BackOut")
TBackInOut = TypeVar("BackInOut", bound="BackInOut")

OVERSHOOT = 1.70158

class BackIn:

    def __init__(self, overshoot: float):
        self._overshoot = overshoot

    def __call__(self, t: float) -> float:
        return t * t * (self._overshoot * (t - 1) + t)

    def overshoot(self, overshoot: float) -> TBackIn:
        return BackIn(overshoot)

ease_back_in = BackIn(OVERSHOOT)

class BackOut:

    def __init__(self, overshoot: float):
        self._overshoot = overshoot

    def __call__(self, t: float) -> float:
        t -= 1
        return t * t * ((t + 1) * self._overshoot + t) + 1

    def overshoot(self, overshoot: float) -> TBackOut:
        return BackOut(overshoot)

ease_back_out = BackOut(OVERSHOOT)

class BackInOut:

    def __init__(self, overshoot: float):
        self._overshoot = overshoot

    def __call__(self, t: float) -> float:
        t *= 2
        if t < 1:
            return t * t * ((self._overshoot + 1) * t - self._overshoot) * 0.5
        else:
            t -= 2
            return (t * t * ((self._overshoot + 1) * t + self._overshoot) + 2) * 0.5

    def overshoot(self, overshoot: float) -> TBackInOut:
        return BackInOut(overshoot)

ease_back_in_out = BackInOut(OVERSHOOT)
