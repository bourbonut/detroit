from dataclasses import dataclass


@dataclass(slots=True)
class Quad:
    node: str
    x0: float
    y0: float
    x1: float
    y1: float
