class Polygon:
    
    def __init__(self):
        self._values = []

    def move_to(self, x, y):
        self._values.append({"x": x, "y": y})

    def close_path(self):
        self._values.append(self._values[0].copy())

    def line_to(self, x, y):
        self._values.append({"x": x, "y": y})

    def value():
        return self._values or None
