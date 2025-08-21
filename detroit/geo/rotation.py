from .compose import Compose
from math import asin, atan2, cos, degrees, pi, radians, sin

TAU = 2 * pi

class RotationIdentity:
    def __call__(self, lambda_, phi):
        if abs(lambda_) > pi:
            lambda_ -= round(lambda_ / TAU) * TAU
        return [lambda_, phi]

    def invert(self, lambda_, phi):
        return self(lambda_, phi)

class RotateRadians:
    def __init__(self, delta_lambda, delta_phi, delta_gamma):
        delta_lambda %= TAU
        self._rotate = RotationIdentity()
        if delta_lambda:
            if delta_phi or delta_gamma:
                self._rotate = Compose(RotationLambda(delta_lambda), RotationPhiGamma(delta_phi, delta_gamma))
            else:
                self._rotate = RotationLambda(delta_lambda)
        elif delta_phi or delta_gamma:
            self._rotate = RotationPhiGamma(delta_phi, delta_gamma)

    def __call__(self, lambda_, phi):
        return self._rotate(lambda_, phi)

    def invert(self, lambda_, phi):
        return self._rotate.invert(lambda_, phi)

class ForwardRotationLambda:
    def __init__(self, delta_lambda):
        self._delta_lambda = delta_lambda

    def __call__(self, lambda_, phi):
        lambda_ += self._delta_lambda
        if abs(lambda_) > pi:
            lambda_ -= round(lambda_ / TAU) * TAU
        return [lambda_, phi]

class RotationLambda:
    def __init__(self, delta_lambda):
        self._call = ForwardRotationLambda(delta_lambda)
        self._invert = ForwardRotationLambda(-delta_lambda)

    def __call__(self, lambda_, phi):
        return self._call(lambda_, phi)

    def invert(self, lambda_, phi):
        return self._invert(lambda_, phi)


class RotationPhiGamma:

    def __init__(self, delta_phi, delta_gamma):
        self._cos_delta_phi = cos(delta_phi)
        self._sin_delta_phi = sin(delta_phi)
        self._cos_delta_gamma = cos(delta_gamma)
        self._sin_delta_gamma = sin(delta_gamma)

    def __call__(self, lambda_, phi):
        cos_phi = cos(phi)
        x = cos(lambda_) * cos_phi
        y = sin(lambda_) * cos_phi
        z = sin(phi)
        k = z * self._cos_delta_phi + x * self._sin_delta_phi
        return [
            atan2(y * self._cos_delta_gamma - k * self._sin_delta_gamma, x * self._cos_delta_phi - z * self._sin_delta_phi),
            asin(k * self._cos_delta_gamma + y * self._sin_delta_gamma)
        ]

    def invert(self, lambda_, phi):
        cos_phi = cos(phi)
        x = cos(lambda_) * cos_phi
        y = sin(lambda_) * cos_phi
        z = sin(phi)
        k = z * self._cos_delta_gamma - y * self._sin_delta_gamma
        return [
            atan2(y * self._cos_delta_gamma + z * self._sin_delta_gamma, x * self._cos_delta_phi + k * self._sin_delta_phi),
            asin(k * self._cos_delta_phi - x * self._sin_delta_phi)
        ]

class Rotation:
    def __init__(self, rotate):
        self._rotate = RotateRadians(radians(rotate[0]), radians(rotate[1]), radians(rotate[2]) if len(rotate) > 2 else 0)

    def __call__(self, coordinates):
        coordinates = self._rotate(radians(coordinates[0]), radians(coordinates[1]))
        coordinates[0] = degrees(coordinates[0])
        coordinates[1] = degrees(coordinates[1])
        return coordinates

    def invert(self, coordinates):
        coordinates = self._rotate.invert(radians(coordinates[0]), radians(coordinates[1]))
        coordinates[0] = degrees(coordinates[0])
        coordinates[1] = degrees(coordinates[1])
        return coordinates

def geo_rotation(rotate) -> Rotation:
    return Rotation(rotate)
