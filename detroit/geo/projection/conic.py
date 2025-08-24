from math import degrees, pi, radians
from .projection import ProjectionMutator
from ...types import Point2D
from ..common import RawProjection
from collections.abc import Callable

class ConicProjection(ProjectionMutator):

    def __init__(self, project_func: Callable[..., RawProjection], phi0: float, phi1: float):
        ProjectionMutator.__init__(self, project_func(phi0, phi1))
        self._project_func = project_func
        self._phi0 = phi0
        self._phi1 = phi1

    def parallels(self, point: Point2D | None = None) -> Point2D:
        if point is None:
            return [degrees(self._phi0), degrees(self._phi1)]
        else:
            return self.set_project(self._project_func(radians(point[0]), radians(point[1])))


def conic_projection(project: Callable[..., RawProjection]) -> ConicProjection:
    return ConicProjection(project, 0, pi / 3)
