from collections.abc import Callable
from math import floor


def blur(values: list[float], r: float) -> list[float]:
    """
    Blurs an array of data in-place by applying three iterations of a moving
    average transform (box filter) for a fast approximation of a Gaussian
    kernel of the given radius, a non-negative number. Returns the given data.

    Parameters
    ----------
    values : list[float]
       Data
    r : float
        Radius

    Returns
    -------
    list[float]
        Blurred data

    Examples
    --------
    >>> d3.blur([0, 0, 1, 0, 0], 1)
    [0.14814814814814814, 0.2222222222222222, 0.25925925925925924, 0.22222222222222224, 0.1481481481481482]
    """
    if r < 0:
        raise ValueError("r cannot be negative")
    length = len(values)
    if not length or not r:
        return values
    blur = blurf(r)
    tmp = values[:]
    blur(values, tmp, 0, length, 1)
    blur(tmp, values, 0, length, 1)
    blur(values, tmp, 0, length, 1)
    return values


def blurf(
    radius: float,
) -> Callable[[list[float], list[float], int, int, int], None]:
    radius0 = floor(radius)
    if radius0 == radius:
        return bluri(radius)
    t = radius - radius0
    w = 2 * radius + 1

    def local_blur(T, S, start, stop, step):
        stop -= step
        if stop < start:
            return
        sum = radius0 * S[start]
        s0 = step * radius0
        s1 = s0 + step
        for i in range(start, start + s0, step):
            sum += S[min(stop, i)]
        for i in range(start, stop + step, step):
            sum += S[min(stop, i + s0)]
            T[i] = (sum + t * (S[max(start, i - s1)] + S[min(stop, i + s1)])) / w
            sum -= S[max(start, i - s0)]

    return local_blur


def blur2d(
    blur: Callable[[float], Callable[[list[float], list[float], int, int, int], None]],
) -> Callable[[dict, float, float | None], dict]:
    def local_blur2(data: dict, rx: float, ry: float | None = None):
        ry = rx if ry is None else ry
        if rx < 0.0:
            raise ValueError("rx cannot be negative")
        if ry < 0.0:
            raise ValueError("ry cannot be negative")
        values = data["data"]
        width = floor(data["width"])
        height = floor(data.get("height", len(values) / width))
        if width < 0:
            raise ValueError("Invalid width")
        if height < 0:
            raise ValueError("Invalid height")
        if not width or not height or (not rx and not ry):
            return data
        blurx = blur(rx) if rx else None
        blury = blur(ry) if ry else None
        tmp = values[:]
        if blurx and blury:
            blurh(blurx, tmp, values, width, height)
            blurh(blurx, values, tmp, width, height)
            blurh(blurx, tmp, values, width, height)
            blurv(blury, values, tmp, width, height)
            blurv(blury, tmp, values, width, height)
            blurv(blury, values, tmp, width, height)
        elif blurx:
            blurh(blurx, values, tmp, width, height)
            blurh(blurx, tmp, values, width, height)
            blurh(blurx, values, tmp, width, height)
        else:
            blurv(blury, values, tmp, width, height)
            blurv(blury, tmp, values, width, height)
            blurv(blury, values, tmp, width, height)
        return {"data": values, "width": width, "height": height}

    return local_blur2


def blurh(
    blur: Callable[[list[float], list[float], int, int, int], None],
    T: list[float],
    S: list[float],
    w: float,
    h: float,
):
    for y in range(0, w * h, w):
        blur(T, S, y, y + w, 1)


def blurv(
    blur: Callable[[list[float], list[float], int, int, int], None],
    T: list[float],
    S: list[float],
    w: float,
    h: float,
):
    n = w * h
    for x in range(w):
        blur(T, S, x, x + n, w)


def blurf_image(
    radius: float,
) -> Callable[[list[float], list[float], int, int, int], None]:
    blur = blurf(radius)

    def local_blur(
        T: list[float],
        S: list[float],
        start: int,
        stop: int,
        step: int,
    ):
        start <<= 2
        stop <<= 2
        step <<= 2
        blur(T, S, start, stop, step)
        blur(T, S, start + 1, stop + 1, step)
        blur(T, S, start + 2, stop + 2, step)
        blur(T, S, start + 3, stop + 3, step)

    return local_blur


def bluri(
    radius: float,
) -> Callable[[list[float], list[float], int, int, int], None]:
    w = 2 * radius + 1

    def local_blur(
        T: list[float],
        S: list[float],
        start: int,
        stop: int,
        step: int,
    ):
        stop -= step
        if stop < start:
            return
        sum = radius * S[start]
        s = step * radius
        for i in range(start, int(start + s), step):
            sum += S[min(stop, i)]
        for i in range(start, stop + step, step):
            sum += S[min(stop, int(i + s))]
            T[i] = sum / w
            sum -= S[max(start, int(i - s))]

    return local_blur


blur2 = blur2d(blurf)
blur2.__doc__ = """
Blurs a matrix of the given width and height in-place by applying a horizontal
blur of radius rx and a vertical blur of radius ry (which defaults to rx). The
matrix values data are stored in a flat (one-dimensional) array.

Parameters
----------
data : dict
    Dictionary with three keys: :code:`"data"`, :code:`"width"` and
    :code:`"height"`. If :code:`"height"` is not specified, it is inferred from
    the given width and length of data.
rx : float
    Radius x
ry : float | None
    Radius y

Returns
-------
dict
    Returns the blurred matrix

Examples
--------
>>> data = [
... 0, 0, 0, 0, 0,
... 0, 0, 1, 0, 0,
... 0, 1, 1, 1, 0,
... 0, 0, 1, 0, 0,
... 0, 0, 0, 0, 0,
... ]
>>> d3.blur2({"data": data, "width": 5, "height": 5}, 1)
{'data': [0.1316872427983539, 0.1755829903978052, 0.20027434842249658, 0.17558299039780523, 0.13168724279835398, 0.1755829903978052, 0.23045267489711932, 0.262002743484225, 0.23045267489711938, 0.1755829903978053, 0.20027434842249656, 0.262002743484225, 0.29766803840877915, 0.262002743484225, 0.20027434842249667, 0.1755829903978052, 0.23045267489711932, 0.262002743484225, 0.23045267489711938, 0.1755829903978053, 0.1316872427983539, 0.1755829903978052, 0.20027434842249656, 0.17558299039780523, 0.13168724279835398], 'width': 5, 'height': 5}
"""
blur_image = blur2d(blurf_image)
blur_image.__doc__ = """
Blurs the given image in-place, blurring each of the RGBA layers
independently by applying an horizontal blur of radius rx and a vertical blur
of radius ry (which defaults to rx).

Parameters
----------
data : dict
    Dictionary with three keys: :code:`"data"`, :code:`"width"` and
    :code:`"height"`. If :code:`"height"` is not specified, it is inferred from
    the given width and length of data.
rx : float
    Radius x
ry : float | None
    Radius y

Returns
-------
dict
    Returns the blurred image
"""
