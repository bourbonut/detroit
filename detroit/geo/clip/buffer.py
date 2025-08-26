from ..common import LineStream


class ClipBuffer(LineStream):
    def __init__(self):
        self._lines = []
        self._line = None

    def line_start(self):
        self._line = []
        self._lines.append(self._line)

    def line_end(self):
        return

    def point(self, x: float, y: float, m: float | None = None):
        self._line.append([x, y, m])

    def rejoin(self):
        if len(self._lines) > 1:
            self._lines.append(self._lines.pop() + self._lines.pop(0))

    def result(self) -> float:
        result = self._lines
        self._lines = []
        self._line = None
        return result

    def __str__(self) -> str:
        return f"ClipBuffer({self._lines})"
