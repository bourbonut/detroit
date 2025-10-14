class Polygon:
    def __init__(self):
        self._values = []

    def move_to(self, x: float, y: float):
        self._values.append([x, y])

    def close_path(self):
        self._values.append(self._values[0].copy())

    def line_to(self, x: float, y: float):
        self._values.append([x, y])

    def value(self) -> list[tuple[float, float]] | None:
        return self._values or None
