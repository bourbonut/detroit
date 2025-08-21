from types import MethodType

def noop():
    return

class Transform:

    def __init__(self, methods):
        self._methods = methods

    def stream(self):
        return Transformer(self._methods)

class Transformer:
    
    def __init__(self, methods):
        self._methods = methods

    def __call__(self, stream):
        s = TransformStream(stream)
        for key in self._methods:
            setattr(s, key, MethodType(self._methods[key], s))
        return s

    def __str__(self):
        return f"Transformer({self._methods})"

class TransformStream:

    def __init__(self, stream):
        self._stream = stream

    def point(self, x, y):
        return self._stream.point(x, y)

    def sphere(self):
        return self._stream.sphere()

    def line_start(self):
        return self._stream.line_start()

    def line_end(self):
        return self._stream.line_end()

    def polygon_start(self):
        return self._stream.polygon_start()

    def polygon_end(self):
        return self._stream.polygon_end()

    def __str__(self):
        return f"TransformStream({self._stream})"
