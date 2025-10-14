from io import StringIO

EPSILON = 1e-6


class Path:
    def __init__(self):
        self._x0 = None
        self._y0 = None
        self._x1 = None
        self._y1 = None
        self._string = StringIO()

    def move_to(self, x: float, y: float):
        self._x0 = x
        self._x1 = x
        self._y0 = y
        self._y1 = y
        self._string.write(f"M{x},{y}")

    def close_path(self):
        if self._x1 is not None:
            self._x1 = self._x0
            self._y1 = self._y0
            self._string.write("Z")

    def line_to(self, x: float, y: float):
        self._x1 = x
        self._y1 = y
        self._string.write(f"L{x},{y}")

    def arc(self, x: float, y: float, r: float, *args):
        x0 = x + r
        y0 = y

        if r < 0:
            raise ValueError("Negative radius")

        if self._x1 is None:
            self._string.write(f"M{x0},{y0}")
        elif abs(self._x1 - x0) > EPSILON or abs(self._y1 - y0) > EPSILON:
            self._string.write(f"L{x0},{y0}")
        if not r:
            return
        self._x1 = x0
        self._y1 = y0
        self._string.write(f"A{r},{r},0,1,1,{x - r},{y}A{r},{r},0,1,1,{x0},{y0}")

    def rect(self, x: float, y: float, w: float, h: float):
        self._x0 = x
        self._x1 = x
        self._y0 = y
        self._y1 = y
        self._string.write(f"M{x},{y}h{w}v{h}h{-w}Z")

    def __str__(self):
        return self._string.getvalue() or None
