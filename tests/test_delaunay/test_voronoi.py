from io import StringIO

import detroit as d3


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


def test_voronoi_1():
    voronoi = d3.Delaunay.from_points([[0, 0], [1, 0], [0, 1], [1, 0]]).voronoi(
        [-1, -1, 2, 2]
    )
    assert voronoi.render_cell(3, None) is None


def test_voronoi_2():
    voronoi = d3.Delaunay.from_points([[0, 0], [1, 0], [0, 1]]).voronoi([-1, -1, 2, 2])
    context = Context()
    voronoi.render_cell(0, context)
    assert str(context) == "M-1,-1L0.5,-1L0.5,0.5L-1,0.5Z"
    voronoi.render_cell(1, context)
    assert str(context) == "M2,-1L2.0,2L0.5,0.5L0.5,-1Z"
    voronoi.render_cell(2, context)
    assert str(context) == "M-1,2L-1,0.5L0.5,0.5L2.0,2Z"


def test_voronoi_3():
    voronoi = d3.Delaunay.from_points([[0, 0], [1, 0], [0, 1], [1, 0]]).voronoi(
        [-1, -1, 2, 2]
    )
    assert voronoi.contains(3, 1, 0) is False
    assert voronoi.contains(1, 1, 0) is True


def test_voronoi_4():
    delaunay = d3.Delaunay.from_points(
        [[0, 0], [300, 0], [0, 300], [300, 300], [100, 100]]
    )
    voronoi = delaunay.voronoi([-500, -500, 500, 500])
    for i in range(len(delaunay.points)):
        delaunay.points[i] = 10 - delaunay.points[i]
    p = voronoi.update().cell_polygon(1)
    assert p == [
        [-500, 500],
        [-500, -140],
        [-240, -140],
        [-140, 60],
        [-140, 500],
        [-500, 500],
    ]


def test_voronoi_5():
    pts = [10, 10, -290, 10, 10, -290, -290, -290, -90, -90]
    delaunay = d3.Delaunay([0 for _ in pts])
    voronoi = delaunay.voronoi([-500, -500, 500, 500])
    assert voronoi.cell_polygon(0) == [
        [500, -500],
        [500, 500],
        [-500, 500],
        [-500, -500],
        [500, -500],
    ]
    assert voronoi.cell_polygon(1) is None
    for i in range(len(delaunay.points)):
        delaunay.points[i] = pts[i]
    p = voronoi.update().cell_polygon(1)
    assert p == [
        [-500, 500],
        [-500, -140],
        [-240, -140],
        [-140, 60],
        [-140, 500],
        [-500, 500],
    ]


def test_voronoi_6():
    voronoi1 = d3.Delaunay.from_points(
        [[50, 10], [10, 50], [10, 10], [200, 100]]
    ).voronoi([40, 40, 440, 180])
    assert len(voronoi1.cell_polygon(0)) == 4
    voronoi2 = d3.Delaunay.from_points([[10, 10], [20, 10]]).voronoi([0, 0, 30, 20])
    assert voronoi2.cell_polygon(0) == [[0, 20], [0, 0], [15, 0], [15, 20], [0, 20]]


def test_voronoi_7():
    voronoi = d3.Delaunay.from_points(
        [[300, 10], [200, 100], [300, 100], [10, 10], [350, 200], [350, 400]]
    ).voronoi([0, 0, 500, 150])
    assert [sorted(voronoi.neighbors(i)) for i in range(6)] == [
        [1, 2],
        [0, 2, 3],
        [0, 1, 4],
        [1],
        [2],
        [],
    ]


def test_voronoi_8():
    for points, lengths in [
        [[[289, 25], [3, 22], [93, 165], [282, 184], [65, 89]], [6, 4, 6, 5, 6]],
        [[[189, 13], [197, 26], [47, 133], [125, 77], [288, 15]], [4, 6, 5, 6, 5]],
        [[[44, 42], [210, 193], [113, 103], [185, 43], [184, 37]], [5, 5, 7, 5, 6]],
    ]:
        voronoi = d3.Delaunay.from_points(points).voronoi([0, 0, 290, 190])
        assert list(map(len, voronoi.cell_polygons())) == lengths


def test_voronoi_9():
    pts = [
        [424.75, 253.75],
        [424.75, 253.74999999999997],
        [407.17640687119285, 296.17640687119285],
        [364.75, 313.75],
        [322.32359312880715, 296.17640687119285],
        [304.75, 253.75],
        [322.32359312880715, 211.32359312880715],
        [364.75, 193.75],
        [407.17640687119285, 211.32359312880715],
        [624.75, 253.75],
        [607.1764068711929, 296.17640687119285],
        [564.75, 313.75],
        [522.3235931288071, 296.17640687119285],
        [504.75, 253.75],
        [564.75, 193.75],
    ]
    voronoi = d3.Delaunay.from_points(pts).voronoi([10, 10, 960, 500])
    assert len(voronoi.cell_polygon(0)) == 4


def test_voronoi_10():
    pts = [[0, 0], [3, 3], [1, 1], [-3, -2]]
    voronoi = d3.Delaunay.from_points(pts).voronoi([0, 0, 2, 2])
    assert list(voronoi.cell_polygons()) == [
        [[0, 0], [1, 0], [0, 1], [0, 0]],
        [[2, 2], [0, 2], [0, 1], [1, 0], [2, 0], [2, 2]],
    ]


def test_voronoi_11():
    points = [[10, 10], [36, 27], [90, 19], [50, 75]]
    voronoi = d3.Delaunay.from_points(points).voronoi([0, 0, 100, 90])
    assert [sorted(voronoi.neighbors(i)) for i in range(4)] == [
        [1],
        [0, 2, 3],
        [1, 3],
        [1, 2],
    ]


def test_voronoi_12():
    points = [[10, -10], [36, -27], [90, -19], [50, -75]]
    voronoi = d3.Delaunay.from_points(points).voronoi([0, -90, 100, 0])
    assert [sorted(voronoi.neighbors(i)) for i in range(4)] == [
        [1],
        [0, 2, 3],
        [1, 3],
        [1, 2],
    ]


def test_voronoi_13():
    points = [[-10, 10], [-36, 27], [-90, 19], [-50, 75]]
    voronoi = d3.Delaunay.from_points(points).voronoi([-100, 0, 0, 90])
    assert [sorted(voronoi.neighbors(i)) for i in range(4)] == [
        [1],
        [0, 2, 3],
        [1, 3],
        [1, 2],
    ]


def test_voronoi_14():
    points = [[-10, -10], [-36, -27], [-90, -19], [-50, -75]]
    voronoi = d3.Delaunay.from_points(points).voronoi([-100, -90, 0, 0])
    assert [sorted(voronoi.neighbors(i)) for i in range(4)] == [
        [1],
        [0, 2, 3],
        [1, 3],
        [1, 2],
    ]


def test_voronoi_15():
    points = [
        [447.27981036477433, 698.9400262172304],
        [485.27830313288746, 668.9946483670656],
        [611.9525697080425, 397.71056371206487],
        [491.44637766366105, 692.071157339428],
        [697.553622336339, 692.071157339428],
        [497.00778156318086, 667.1990851383492],
        [691.9922184368191, 667.1990851383492],
        [544.9897579870977, 407.0828550310619],
        [543.1738215956482, 437.35879519252677],
    ]
    voronoi = d3.Delaunay.from_points(points).voronoi([0, 0, 1000, 1000])
    assert len(voronoi.cell_polygon(3)) == 6


def test_voronoi_16():
    points = [[10, 190]] + [[i * 80, (i * 50) / 7] for i in range(8)]
    voronoi = d3.Delaunay.from_points(points).voronoi([1, 1, 499, 199])
    assert list(map(len, voronoi.cell_polygons())) == [7, 5, 5, 5, 6, 5, 5, 5]


def test_voronoi_17():
    points = [[25, 20], [75, 20], [125, 20], [175, 20], [225, 20]]
    voronoi = d3.Delaunay.from_points(points).voronoi([0, 0, 250, 40])
    assert [[[round(x) for x in d] for d in p] for p in voronoi.cell_polygons()] == [
        [[0, 40], [0, 0], [50, 0], [50, 40], [0, 40]],
        [[100, 0], [100, 40], [50, 40], [50, 0], [100, 0]],
        [[150, 0], [150, 40], [100, 40], [100, 0], [150, 0]],
        [[150, 40], [150, 0], [200, 0], [200, 40], [150, 40]],
        [[250, 0], [250, 40], [200, 40], [200, 0], [250, 0]],
    ]
