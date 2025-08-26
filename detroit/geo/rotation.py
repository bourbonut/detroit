from math import asin, atan2, cos, degrees, pi, radians, sin

from ..types import Point2D
from .compose import Compose

TAU = 2 * pi


class RotationIdentity:
    def __call__(self, lambda_: float, phi: float) -> Point2D:
        if abs(lambda_) > pi:
            lambda_ -= round(lambda_ / TAU) * TAU
        return [lambda_, phi]

    def invert(self, lambda_: float, phi: float) -> Point2D:
        return self(lambda_, phi)


class RotateRadians:
    def __init__(self, delta_lambda: float, delta_phi: float, delta_gamma: float):
        delta_lambda %= TAU
        self._rotate = RotationIdentity()
        if delta_lambda:
            if delta_phi or delta_gamma:
                self._rotate = Compose(
                    RotationLambda(delta_lambda),
                    RotationPhiGamma(delta_phi, delta_gamma),
                )
            else:
                self._rotate = RotationLambda(delta_lambda)
        elif delta_phi or delta_gamma:
            self._rotate = RotationPhiGamma(delta_phi, delta_gamma)

    def __call__(self, lambda_: float, phi: float) -> Point2D:
        return self._rotate(lambda_, phi)

    def invert(self, lambda_: float, phi: float) -> Point2D:
        return self._rotate.invert(lambda_, phi)


class ForwardRotationLambda:
    def __init__(self, delta_lambda: float):
        self._delta_lambda = delta_lambda

    def __call__(self, lambda_: float, phi: float) -> Point2D:
        lambda_ += self._delta_lambda
        if abs(lambda_) > pi:
            lambda_ -= round(lambda_ / TAU) * TAU
        return [lambda_, phi]


class RotationLambda:
    def __init__(self, delta_lambda: float):
        self._call = ForwardRotationLambda(delta_lambda)
        self._invert = ForwardRotationLambda(-delta_lambda)

    def __call__(self, lambda_: float, phi: float) -> Point2D:
        return self._call(lambda_, phi)

    def invert(self, lambda_: float, phi: float) -> Point2D:
        return self._invert(lambda_, phi)


class RotationPhiGamma:
    def __init__(self, delta_phi: float, delta_gamma: float):
        self._cos_delta_phi = cos(delta_phi)
        self._sin_delta_phi = sin(delta_phi)
        self._cos_delta_gamma = cos(delta_gamma)
        self._sin_delta_gamma = sin(delta_gamma)

    def __call__(self, lambda_: float, phi: float) -> Point2D:
        cos_phi = cos(phi)
        x = cos(lambda_) * cos_phi
        y = sin(lambda_) * cos_phi
        z = sin(phi)
        k = z * self._cos_delta_phi + x * self._sin_delta_phi
        return [
            atan2(
                y * self._cos_delta_gamma - k * self._sin_delta_gamma,
                x * self._cos_delta_phi - z * self._sin_delta_phi,
            ),
            asin(k * self._cos_delta_gamma + y * self._sin_delta_gamma),
        ]

    def invert(self, lambda_: float, phi: float) -> Point2D:
        cos_phi = cos(phi)
        x = cos(lambda_) * cos_phi
        y = sin(lambda_) * cos_phi
        z = sin(phi)
        k = z * self._cos_delta_gamma - y * self._sin_delta_gamma
        return [
            atan2(
                y * self._cos_delta_gamma + z * self._sin_delta_gamma,
                x * self._cos_delta_phi + k * self._sin_delta_phi,
            ),
            asin(k * self._cos_delta_phi - x * self._sin_delta_phi),
        ]


class Rotation:
    """
    Rotation class
    """

    def __init__(self, rotate: tuple[float, float] | tuple[float, float, float]):
        self._rotate = RotateRadians(
            radians(rotate[0]),
            radians(rotate[1]),
            radians(rotate[2]) if len(rotate) > 2 else 0,
        )

    def __call__(self, coordinates: Point2D) -> Point2D:
        """
        Rotates a 2D point

        Parameters
        ----------
        coordinates : Point2D
            2D point

        Returns
        -------
        Point2D
            Rotated 2D point
        """
        coordinates = self._rotate(radians(coordinates[0]), radians(coordinates[1]))
        coordinates[0] = degrees(coordinates[0])
        coordinates[1] = degrees(coordinates[1])
        return coordinates

    def invert(self, coordinates: Point2D) -> Point2D:
        """
        Invert transformation.

        Parameters
        ----------
        coordinates : Point2D
            2D point

        Returns
        -------
        Point2D
            Inverted 2D point
        """
        coordinates = self._rotate.invert(
            radians(coordinates[0]), radians(coordinates[1])
        )
        coordinates[0] = degrees(coordinates[0])
        coordinates[1] = degrees(coordinates[1])
        return coordinates


def geo_rotation(rotate: tuple[float, float] | tuple[float, float, float]) -> Rotation:
    """
    Returns a rotation function for the given angles, which must be a two- or
    three-element array of numbers :math:`[\\lambda, \\phi, \\gamma]`
    specifying the rotation angles in degrees about each spherical axis. (These
    correspond to yaw, pitch and roll). If the rotation angle :math:`\\gamma`
    is omitted, it defaults to 0.


    Parameters
    ----------
    rotate : tuple[float, float] | tuple[float, float, float]
        Rotation parameters :math:`[\\lambda, \\phi, \\gamma]`

    Returns
    -------
    Rotation
        Rotation callable object
    """
    return Rotation(rotate)
