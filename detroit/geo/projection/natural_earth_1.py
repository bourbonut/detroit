from ...types import Point2D
from ..common import Projection
from .projection import geo_projection

EPSILON = 1e-6


class NaturalEarth1Raw:
    def __call__(self, lambda_: float, phi: float) -> Point2D:
        phi2 = phi * phi
        phi4 = phi2 * phi2
        return [
            lambda_
            * (
                0.8707
                - 0.131979 * phi2
                + phi4 * (-0.013791 + phi4 * (0.003971 * phi2 - 0.001529 * phi4))
            ),
            phi
            * (
                1.007226
                + phi2
                * (0.015085 + phi4 * (-0.044475 + 0.028874 * phi2 - 0.005916 * phi4))
            ),
        ]

    def invert(self, x: float, y: float) -> Point2D:
        phi = y
        i = 25

        while True:
            phi2 = phi * phi
            phi4 = phi2 * phi2
            delta = (
                phi
                * (
                    1.007226
                    + phi2
                    * (
                        0.015085
                        + phi4 * (-0.044475 + 0.028874 * phi2 - 0.005916 * phi4)
                    )
                )
                - y
            ) / (
                1.007226
                + phi2
                * (
                    0.015085 * 3
                    + phi4
                    * (-0.044475 * 7 + 0.028874 * 9 * phi2 - 0.005916 * 11 * phi4)
                )
            )
            phi -= delta
            i -= 1
            if abs(delta) <= EPSILON or i <= 0:
                break

        phi2 = phi * phi
        return [
            x
            / (
                0.8707
                + phi2
                * (
                    -0.131979
                    + phi2
                    * (-0.013791 + phi2 * phi2 * phi2 * (0.003971 - 0.001529 * phi2))
                )
            ),
            phi,
        ]


def geo_natural_earth_1() -> Projection:
    """
    The Natural Earth projection is a pseudocylindrical projection designed by
    Tom Patterson. It is neither conformal nor equal-area, but appealing to the
    eye for small-scale maps of the whole world.

    Returns
    -------
    Projection
        Projection object
    """
    return geo_projection(NaturalEarth1Raw()).scale(175.295)
