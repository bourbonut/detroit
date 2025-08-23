from math import degrees, pi, radians
from .projection import geo_projection_mutator, ProjectionMutator
from ...types import Point2D
from ..common import RawProjection
from collections.abc import Callable

class ConicProjectionState:
    def __init__(self, project: Callable[..., RawProjection]):
        self._phi0 = 0
        self._phi1 = pi / 3
        self._m = geo_projection_mutator(project)

    def projection(self):
        return self._m(self._phi0, self._phi1)

    def set_point(self, point: Point2D):
        self._phi0 = radians(point[0])
        self._phi1 = radians(point[1])

    def get_point(self) -> Point2D:
        return [degrees(self._phi0), degrees(self._phi1)]


class ConicProjection(ProjectionMutator):

    def __init__(self, project_func, phi0, phi1):
        ProjectionMutator.__init__(self, project_func(phi0, phi1))
        self._project_func = project_func
        self._phi0 = phi0
        self._phi1 = phi1

    def parallels(self, point: Point2D | None = None) -> Point2D:
        if point is None:
            return [degrees(self._phi0), degrees(self._phi1)]
        else:
            return ConicProjection(self._project_func, radians(point[0]), radians(point[1]))


def conic_projection(project: Callable[..., RawProjection]) -> ConicProjection:
    return ConicProjection(project, 0, pi / 3)
