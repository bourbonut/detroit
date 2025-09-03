from ..types import Point2D
from .common import SpatialTransform


class Compose:
    def __init__(self, a: SpatialTransform, b: SpatialTransform):
        self._a = a
        self._b = b
        self._invert = self._default_invert
        if hasattr(self._a, "invert") and hasattr(self._b, "invert"):
            self._invert = self._valid_invert

    def __call__(self, x: float, y: float) -> Point2D:
        a, b = self._a(x, y)
        return self._b(a, b)

    def invert(self, x: float, y: float) -> Point2D:
        return self._invert(x, y)

    def _valid_invert(self, x: float, y: float) -> Point2D:
        x = self._b.invert(x, y)
        return None if x is None else self._a.invert(x[0], x[1])

    def _default_invert(self, x: float, y: float):
        return

    def __str__(self) -> str:
        return f"Compose({self._a}, {self._b})"
