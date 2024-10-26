import math

epsilon2 = 1e-12

def cosh(x):
    return (math.exp(x) + 1 / math.exp(x)) / 2

def sinh(x):
    return (math.exp(x) - 1 / math.exp(x)) / 2

def tanh(x):
    return (math.exp(2 * x) - 1) / (math.exp(2 * x) + 1)

def zoomRho(rho, rho2, rho4):
    def zoom(p0, p1):
        ux0, uy0, w0 = p0
        ux1, uy1, w1 = p1
        dx = ux1 - ux0
        dy = uy1 - uy0
        d2 = dx * dx + dy * dy

        if d2 < epsilon2:
            S = math.log(w1 / w0) / rho
            def interpolator(t):
                return [
                    ux0 + t * dx,
                    uy0 + t * dy,
                    w0 * math.exp(rho * t * S)
                ]
        else:
            d1 = math.sqrt(d2)
            b0 = (w1 * w1 - w0 * w0 + rho4 * d2) / (2 * w0 * rho2 * d1)
            b1 = (w1 * w1 - w0 * w0 - rho4 * d2) / (2 * w1 * rho2 * d1)
            r0 = math.log(math.sqrt(b0 * b0 + 1) - b0)
            r1 = math.log(math.sqrt(b1 * b1 + 1) - b1)
            S = (r1 - r0) / rho
            def interpolator(t):
                s = t * S
                coshr0 = cosh(r0)
                u = w0 / (rho2 * d1) * (coshr0 * tanh(rho * s + r0) - sinh(r0))
                return [
                    ux0 + u * dx,
                    uy0 + u * dy,
                    w0 * coshr0 / cosh(rho * s + r0)
                ]

        interpolator.duration = S * 1000 * rho / math.sqrt(2)
        return interpolator

    def set_rho(new_rho):
        new_rho = max(1e-3, float(new_rho))
        return zoomRho(new_rho, new_rho * new_rho, new_rho ** 4)

    zoom.rho = set_rho
    return zoom

zoom = zoomRho(math.sqrt(2), 2, 4)
