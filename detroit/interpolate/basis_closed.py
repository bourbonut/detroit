from .basis import basis

def basis_closed(values):
    n = len(values)
    
    def interpolate(t):
        i = int((t % 1) * n)
        v0 = values[(i + n - 1) % n]
        v1 = values[i % n]
        v2 = values[(i + 1) % n]
        v3 = values[(i + 2) % n]
        return basis((t - i / n) * n, v0, v1, v2, v3)
    
    return interpolate
