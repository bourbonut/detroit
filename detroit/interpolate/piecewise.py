from .object_to_value import interpolate as interpolate_value


def piecewise(interpolate, values=None):
    if values is None:
        values = interpolate
        interpolate = interpolate_value

    n = len(values) - 1
    I = [interpolate_value(values[i], values[i + 1]) for i in range(n)]

    def local_interpolate(t):
        i = max(0, min(n - 1, int(t * n)))
        return I[i](t * n - i)

    return local_interpolate
