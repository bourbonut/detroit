def quantize(interpolator, n):
    samples = [interpolator(i / (n - 1)) for i in range(n)]
    return samples
