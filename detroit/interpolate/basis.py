def basis(t1, v0, v1, v2, v3):
    t2 = t1 * t1
    t3 = t2 * t1
    return (
        (1 - 3 * t1 + 3 * t2 - t3) * v0
        + (4 - 6 * t2 + 3 * t3) * v1
        + (1 + 3 * t1 + 3 * t2 - 3 * t3) * v2
        + t3 * v3
    ) / 6


def basis_interpolator(values):
    n = len(values) - 1

    def interpolate(t):
        i = 0 if t <= 0 else (n - 1 if t >= 1 else int(t * n))
        v1 = values[i]
        v2 = values[i + 1]
        v0 = values[i - 1] if i > 0 else 2 * v1 - v2
        v3 = values[i + 2] if i < n - 1 else 2 * v2 - v1
        return basis((t - i / n) * n, v0, v1, v2, v3)

    return interpolate
