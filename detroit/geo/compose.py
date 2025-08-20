class Compose:

    def __init__(self, a, b):
        self._a = a
        self._b = b
        self._invert = self._default_invert
        if hasattr(self._a, "invert") and hasattr(self._b, "invert"):
            self._invert = self._valid_invert

    def __call__(self, x, y):
        x = self._a(x, y)
        return self._b(x[0], x[1])

    def invert(self, x, y):
        return self._invert(x, y)

    def _valid_invert(self, x, y):
        x = self._b.invert(x, y)
        return x and self._a.invert(x[0], x[1])

    def _default_invert(self, x, y):
        return
