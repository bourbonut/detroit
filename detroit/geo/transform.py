from collections.abc import Callable
from types import MethodType

from .common import PolygonStream


class TransformStream(PolygonStream):
    """
    Default class where methods don't affect the behavior of the passed stream
    object if they are not updated.

    Parameters
    ----------
    stream : PolygonStream
        Stream object
    """

    def __init__(self, stream: PolygonStream):
        self._stream = stream

    def point(self, x: float, y: float):
        """
        Calls the stream :code:`point` method

        Parameters
        ----------
        x : float
            x value
        y : float
            y value
        """
        return self._stream.point(x, y)

    def sphere(self):
        """
        Calls the stream :code:`sphere` method
        """
        return self._stream.sphere()

    def line_start(self):
        """
        Calls the stream :code:`line_start` method
        """
        return self._stream.line_start()

    def line_end(self):
        """
        Calls the stream :code:`line_end` method
        """
        return self._stream.line_end()

    def polygon_start(self):
        """
        Calls the stream :code:`polygon_start` method
        """
        return self._stream.polygon_start()

    def polygon_end(self):
        """
        Calls the stream :code:`polygon_end` method
        """
        return self._stream.polygon_end()

    def __str__(self):
        return f"TransformStream({self._stream})"


class GeoTransformer:
    """
    Transform a stream object given :code:`methods`

    Parameters
    ----------
    methods : dict[str, Callable[..., ...]]
        Methods applied on a stream object
    """

    def __init__(self, methods: dict[str, Callable[..., ...]]):
        self._methods = methods

    def __call__(self, stream: PolygonStream) -> TransformStream:
        """
        Creates a new :code:`TransformStream` with the argument :code:`stream`
        and updates its methods.

        Parameters
        ----------
        stream : PolygonStream
            Stream object

        Returns
        -------
        TransformStream
            Transformed stream
        """
        s = TransformStream(stream)
        for key in self._methods:
            setattr(s, key, MethodType(self._methods[key], s))
        return s

    def __str__(self):
        return f"GeoTransformer({self._methods})"


class GeoTransform:
    """
    Defines an arbitrary transform using the methods defined on the specified
    methods object. Any undefined methods will use pass-through methods that
    propagate inputs to the output stream.

    Parameters
    ----------
    methods : dict[str, Callable[..., ...]]
        Methods applied on a stream object
    """

    def __init__(self, methods: dict[str, Callable[..., ...]]):
        self._methods = methods

    def stream(self) -> GeoTransformer:
        """
        Passes :code:`methods` to a new class which transforms the methods of a
        stream object given the methods and returns it.

        Returns
        -------
        GeoTransformer
            Callable object which modifies the behavior of a stream object
        """
        return GeoTransformer(self._methods)


def geo_transform(methods: dict[str, Callable[..., ...]]) -> GeoTransform:
    """
    Defines an arbitrary transform using the methods defined on the specified
    methods object. Any undefined methods will use pass-through methods that
    propagate inputs to the output stream.

    Parameters
    ----------
    methods : dict[str, Callable[..., ...]]
        Methods applied on a stream object

    Returns
    -------
    GeoTransform
        Class which holds the passed methods
    """
    return GeoTransform(methods)
