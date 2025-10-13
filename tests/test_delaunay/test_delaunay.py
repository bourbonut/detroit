from io import StringIO
from math import sin

import detroit as d3
from detroit.delaunay.path import Path


class Context:
    def __init__(self):
        self._string = StringIO()

    def move_to(self, x, y):
        self._string.write(f"M{x},{y}")

    def line_to(self, x, y):
        self._string.write(f"L{x},{y}")

    def close_path(self):
        self._string.write("Z")

    def __str__(self):
        string = self._string.getvalue()
        self._string = StringIO()
        return string


def test_delaunay_1():
    delaunay = d3.Delaunay.from_points([[0, 0], [1, 0], [0, 1], [1, 1]])
    assert delaunay.points == [0, 0, 1, 0, 0, 1, 1, 1]
    assert delaunay.triangles == [0, 2, 1, 2, 3, 1]
    assert delaunay.halfedges == [-1, 5, -1, -1, -1, 1]
    assert delaunay.inedges == [2, 4, 0, 3]
    assert list(delaunay.neighbors(0)) == [1, 2]
    assert list(delaunay.neighbors(1)) == [3, 2, 0]
    assert list(delaunay.neighbors(2)) == [0, 1, 3]
    assert list(delaunay.neighbors(3)) == [2, 1]


def test_delaunay_2():
    delaunay = d3.Delaunay.from_points([[0, 0], [1, 0], [0, 1], [1, 0]])
    assert delaunay.inedges == [2, 1, 0, -1]
    assert list(delaunay.neighbors(0)) == [1, 2]
    assert list(delaunay.neighbors(1)) == [2, 0]
    assert list(delaunay.neighbors(2)) == [0, 1]
    assert list(delaunay.neighbors(3)) == []


def test_delaunay_3():
    def gen():
        yield [0, 0]
        yield [1, 0]
        yield [0, 1]
        yield [1, 1]

    delaunay = d3.Delaunay.from_points(list(gen()))
    assert delaunay.points == [0, 0, 1, 0, 0, 1, 1, 1]
    assert delaunay.triangles == [0, 2, 1, 2, 3, 1]
    assert delaunay.halfedges == [-1, 5, -1, -1, -1, 1]


def test_delaunay_4():
    def gen():
        yield {"x": 0, "y": 0}
        yield {"x": 1, "y": 0}
        yield {"x": 0, "y": 1}
        yield {"x": 1, "y": 1}

    delaunay = d3.Delaunay.from_points(list(gen()), lambda d: d["x"], lambda d: d["y"])
    assert delaunay.points == [0, 0, 1, 0, 0, 1, 1, 1]
    assert delaunay.triangles == [0, 2, 1, 2, 3, 1]
    assert delaunay.halfedges == [-1, 5, -1, -1, -1, 1]


def test_delaunay_5():
    delaunay = d3.Delaunay.from_points(
        [None] * 4, lambda d, i: i & 1, lambda d, i: (i >> 1) & 1
    )
    assert delaunay.points == [0, 0, 1, 0, 0, 1, 1, 1]
    assert delaunay.triangles == [0, 2, 1, 2, 3, 1]
    assert delaunay.halfedges == [-1, 5, -1, -1, -1, 1]


def test_delaunay_6():
    voronoi = d3.Delaunay.from_points([[0, 0], [1, 0], [0, 1], [1, 1]]).voronoi()
    assert voronoi.xmin == 0
    assert voronoi.ymin == 0
    assert voronoi.xmax == 960
    assert voronoi.ymax == 500


def test_delaunay_7():
    voronoi = d3.Delaunay.from_points([[0, 0], [1, 0], [0, 1], [1, 1]]).voronoi(
        [-1, -1, 2, 2]
    )
    assert voronoi.xmin == -1
    assert voronoi.ymin == -1
    assert voronoi.xmax == 2
    assert voronoi.ymax == 2


def test_delaunay_8():
    voronoi = d3.Delaunay.from_points([[0, 0], [1, 0], [0, 1], [1, 0]]).voronoi(
        [-1, -1, 2, 2]
    )
    assert voronoi.circumcenters == [0.5, 0.5]
    assert voronoi.vectors == [0, -1, -1, 0, 1, 1, 0, -1, -1, 0, 1, 1, 0, 0, 0, 0]


def test_delaunay_9():
    delaunay = d3.Delaunay.from_points([[0, 0]])
    assert delaunay.render_points() == "M2,0A2,2,0,1,1,-2,0A2,2,0,1,1,2,0"
    assert delaunay.render_points(5) == "M5,0A5,5,0,1,1,-5,0A5,5,0,1,1,5,0"
    assert delaunay.render_points(None, 5) == "M5,0A5,5,0,1,1,-5,0A5,5,0,1,1,5,0"
    assert delaunay.render_points(None) == "M2,0A2,2,0,1,1,-2,0A2,2,0,1,1,2,0"
    assert delaunay.render_points(None) == "M2,0A2,2,0,1,1,-2,0A2,2,0,1,1,2,0"
    assert delaunay.render_points(None, None) == "M2,0A2,2,0,1,1,-2,0A2,2,0,1,1,2,0"
    path = Path()
    delaunay.render_points(path, 3)
    assert str(path) == "M3,0A3,3,0,1,1,-3,0A3,3,0,1,1,3,0"


def test_delaunay_10():
    voronoi = d3.Delaunay.from_points([[0, 0], [1, 0], [-1, 0]]).voronoi([-1, -1, 2, 2])
    assert sorted(voronoi.delaunay.neighbors(0)) == [1, 2]
    assert list(voronoi.delaunay.neighbors(1)) == [0]
    assert list(voronoi.delaunay.neighbors(2)) == [0]


def test_delaunay_11():
    delaunay = d3.Delaunay.from_points(
        [[0, 0], [300, 0], [0, 300], [300, 300], [100, 100]]
    )
    assert delaunay.find(49, 49) == 0
    assert delaunay.find(51, 51) == 4


def test_delaunay_12():
    delaunay = d3.Delaunay.from_points([[0, 1]])
    assert delaunay.find(0, -1) == 0
    assert delaunay.find(0, 2.2) == 0
    delaunay.points = [0 for _ in delaunay.points]
    delaunay.update()
    assert delaunay.find(0, -1) == 0
    assert delaunay.find(0, 1.2) == 0


def test_delaunay_13():
    delaunay = d3.Delaunay([0, 1, 0, 2])
    assert delaunay.find(0, -1) == 0
    assert delaunay.find(0, 2.2) == 1
    delaunay.points = [0 for _ in delaunay.points]
    delaunay.update()
    assert delaunay.find(0, -1) == 0
    assert delaunay.find(0, 1.2) == 0


def test_delaunay_14():
    points = [[0, 1], [0, 2], [0, 4], [0, 0], [0, 3], [0, 4], [0, 4]]
    delaunay = d3.Delaunay.from_points(points)
    assert points[delaunay.find(0, -1)][1] == 0
    assert points[delaunay.find(0, 1.2)][1] == 1
    assert points[delaunay.find(1, 1.9)][1] == 2
    assert points[delaunay.find(-1, 3.3)][1] == 3
    assert points[delaunay.find(10, 10)][1] == 4
    assert points[delaunay.find(10, 10, 0)][1] == 4


def test_delaunay_15():
    points = [[i * 4, i / 3 + 100] for i in range(120)]
    delaunay = d3.Delaunay.from_points(points)
    assert list(delaunay.neighbors(2)) == [1, 3]


def test_delaunay_16():
    points = [[i**2, i**2] for i in range(2000)]
    delaunay = d3.Delaunay.from_points(points)
    assert points[delaunay.find(0, -1)][1] == 0
    assert points[delaunay.find(0, 1.2)][1] == 1
    # assert points[delaunay.find(3.9, 3.9)][1] == 4 # TODO
    assert points[delaunay.find(10, 9.5)][1] == 9
    assert points[delaunay.find(10, 9.5, 0)][1] == 9
    # assert points[delaunay.find(1e6, 1e6)][1] == 1e6 # TODO


def test_delaunay_17():
    delaunay = d3.Delaunay.from_points(
        [[0, 0], [300, 0], [0, 300], [300, 300], [100, 100]]
    )
    circumcenters1 = delaunay.voronoi([-500, -500, 500, 500]).circumcenters
    for i in range(len(delaunay.points)):
        delaunay.points[i] = -delaunay.points[i]
    delaunay.update()
    circumcenters2 = delaunay.voronoi([-500, -500, 500, 500]).circumcenters
    assert circumcenters1 == [150, -50, -50, 150, 250, 150, 150, 250]
    assert circumcenters2 == [-150, 50, -250, -150, 50, -150, -150, -250]


def test_delaunay_18():
    delaunay = d3.Delaunay([0 for _ in range(250)])
    assert delaunay.collinear is None
    for i in range(len(delaunay.points)):
        delaunay.points[i] = i if i % 2 else 0
    delaunay.update()
    assert len(delaunay.collinear) == 125

    for i in range(len(delaunay.points)):
        delaunay.points[i] = sin(i)

    delaunay.update()
    assert delaunay.collinear is None
    for i in range(len(delaunay.points)):
        delaunay.points[i] = i if i % 2 else 0

    delaunay.update()
    assert len(delaunay.collinear) == 125

    for i in range(len(delaunay.points)):
        delaunay.points[i] = 0

    delaunay.update()
    assert delaunay.collinear is None


def test_delaunay_19():
    delaunay = d3.Delaunay.from_points([[0, 0], [0, 0], [10, 10], [10, -10]])
    assert delaunay.find(100, 100) == 2
    assert delaunay.find(0, 0, 1) > -1

    delaunay = d3.Delaunay.from_points(
        [[0, 0] for _ in range(1000)] + [[10, 10], [10, -10]]
    )
    assert delaunay.find(0, 0, 1) > -1


def test_delaunay_20():
    delaunay = d3.Delaunay(
        [509, 253, 426, 240, 426, 292, 567, 272, 355, 356, 413, 392]
        + [319, 408, 374, 285, 327, 303, 381, 215, 475, 319, 301, 352]
        + [247, 426, 532, 334, 234, 366, 479, 375, 251, 302, 340, 170]
        + [160, 377, 626, 317, 177, 296, 322, 243, 195, 422, 241, 232]
        + [585, 358, 666, 406, 689, 343, 172, 198, 527, 401, 766, 350]
        + [444, 432, 117, 316, 267, 170, 580, 412, 754, 425, 117, 231]
        + [725, 300, 700, 222, 438, 165, 703, 168, 558, 221, 475, 211]
        + [491, 125, 216, 166, 240, 108, 783, 266, 640, 258, 184, 77]
        + [387, 90, 162, 125, 621, 162, 296, 78, 532, 154, 763, 199]
        + [132, 165, 422, 343, 312, 128, 125, 77, 450, 95, 635, 106]
        + [803, 415, 714, 63, 529, 87, 388, 152, 575, 126, 573, 64]
        + [726, 381, 773, 143, 787, 67, 690, 117, 813, 203, 811, 319]
    )
    assert delaunay.find(49, 311) == 31
    assert delaunay.find(49, 311, 22) == 31


def test_delaunay_21():
    delaunay = d3.Delaunay.from_points([[0, 0], [1, 0], [0, 1], [1, 1]])
    context = Context()
    delaunay.render_hull(context)
    assert str(context) == "M0,1L1,1L1,0L0,0Z"
