from collections.abc import Callable
from functools import cmp_to_key
from typing import TypeVar

from ..common import LineStream, Point2D
from ..point_equal import EPSILON, point_equal

TIntersection = TypeVar("Intersection", bound="Intersection")


class Intersection:
    __slots__ = ("x", "z", "o", "e", "v", "n", "p")

    def __init__(
        self, point: Point2D, points: list[Point2D], other: TIntersection, entry: bool
    ):
        self.x = point
        self.z = points
        self.o = other
        self.e = entry
        self.v = False
        self.n = None
        self.p = None


def clip_rejoin(
    segments: list[list[tuple[float, float, float | None]]],
    compare_intersection: Callable[[Intersection, Intersection], float],
    start_inside: int,
    interpolate: Callable[[float | None, float | None, float, LineStream], None],
    stream: LineStream,
):
    subject = []
    clip = []

    if segments:
        for segment in segments:
            n = len(segment) - 1
            if n <= 0:
                continue
            p0 = segment[0]
            p1 = segment[n]

            if point_equal(p0, p1):
                if not p0[2] and not p1[2]:
                    stream.line_start()
                    for i in range(n):
                        p0 = segment[i]
                        stream.point(p0[0], p0[1])
                    stream.line_end()
                    continue
                p1[0] += 2 * EPSILON

            x = Intersection(p0, segment, None, True)
            subject.append(x)
            x.o = Intersection(p0, None, x, False)
            clip.append(x.o)

            x = Intersection(p1, segment, None, False)
            subject.append(x)
            x.o = Intersection(p1, None, x, True)
            clip.append(x.o)

    if not subject:
        return

    clip.sort(key=cmp_to_key(compare_intersection))
    link(subject)
    link(clip)

    for intersection in clip:
        start_inside = not (start_inside)
        intersection.e = start_inside

    start = subject[0]

    while True:
        current = start
        is_subject = True
        while current.v:
            current = current.n
            if current == start:
                return
        points = current.z
        stream.line_start()

        while True:
            current.v = current.o.v = True
            if current.e:
                if is_subject:
                    for point in points:
                        x, y, _ = point
                        stream.point(x, y)
                else:
                    interpolate(current.x, current.n.x, 1, stream)
                current = current.n
            else:
                if is_subject:
                    points = current.p.z
                    for point in reversed(points):
                        x, y, _ = point
                        stream.point(x, y)
                else:
                    interpolate(current.x, current.p.x, -1, stream)
                current = current.p
            current = current.o
            points = current.z
            is_subject = not is_subject
            if current.v:
                break
        stream.line_end()


def link(array: list[Intersection]):
    n = len(array)
    if n == 0:
        return

    a = array[0]
    for i in range(n):
        b = array[i]
        a.n = b
        b.p = a
        a = b

    b = array[0]
    a.n = b
    b.p = a
